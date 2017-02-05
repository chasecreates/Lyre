"""
Handles making requests to the IndicoApi Server
"""
import sys
import json
import requests
import warnings
from itertools import islice, chain
import os.path
import datetime

try:
    from urllib import urlencode
    from urlparse import urlparse
except: # For Python 3:
    from urllib.parse import urlencode, urlparse

from indicoio.utils.errors import IndicoError
from indicoio import JSON_HEADERS
from indicoio import config


def batched(iterable, size):
    """
    Split an iterable into constant sized chunks
    Recipe from http://stackoverflow.com/a/8290514
    """
    length = len(iterable)
    for batch_start in range(0, length, size):
        yield iterable[batch_start:batch_start+size]


def standardize_input_data(data):
    """
    Ensure utf-8 encoded strings are passed to the indico API
    """
    if type(data) == bytes:
        data = data.decode('utf-8')
    if type(data) == list:
        data = [
            el.decode('utf-8') if type(data) == bytes else el
            for el in data
        ]
    return data


def api_handler(input_data, cloud, api, url_params=None, batch_size=None, **kwargs):
    """
    Sends finalized request data to ML server and receives response.
    If a batch_size is specified, breaks down a request into smaller
    component requests and aggregates the results.
    """
    url_params = url_params or {}
    input_data = standardize_input_data(input_data)

    cloud = cloud or config.cloud
    host = "%s.indico.domains" % cloud if cloud else config.host

    # LOCAL DEPLOYMENTS
    if not (host.endswith('indico.domains') or host.endswith('indico.io')):
        url_protocol = "http"
    else:
        url_protocol = config.url_protocol

    headers = dict(JSON_HEADERS)
    headers["X-ApiKey"] = url_params.get("api_key") or config.api_key
    url = create_url(url_protocol, host, api, dict(kwargs, **url_params))
    return collect_api_results(input_data, url, headers, api, batch_size, kwargs)


def collect_api_results(input_data, url, headers, api, batch_size, kwargs):
    """
    Optionally split up a single request into a series of requests
    to ensure timely HTTP responses.

    Could eventually speed up the time required to receive a response by
    sending batches to the indico API concurrently
    """
    if batch_size:
        results = []
        for batch in batched(input_data, size=batch_size):
            try:
                results.extend(send_request(batch, api, url, headers, kwargs))
            except IndicoError as e:
                # Log results so far to file
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                filename = "indico-{api}-{timestamp}.json".format(
                    api=api,
                    timestamp=timestamp
                )
                if sys.version_info > (3, 0):
                    json.dump(results, open(filename, mode='w', encoding='utf-8'))
                else:
                    json.dump(results, open(filename, mode='w'))
                raise IndicoError(
                    "The following error occurred while processing your data: `{err}` "
                    "Partial results have been saved to {filename}".format(
                        err=e,
                        filename=os.path.abspath(filename)
                    )
                )
        return results
    else:
        return send_request(input_data, api, url, headers, kwargs)


def send_request(input_data, api, url, headers, kwargs):
    """
    Use the requests library to send of an HTTP call to the indico servers
    """
    data = {}
    if input_data != None:
        data['data'] = input_data

    data.update(**kwargs)
    json_data = json.dumps(data)

    response = requests.post(url, data=json_data, headers=headers)

    warning = response.headers.get('x-warning')
    if warning:
        warnings.warn(warning)

    cloud = urlparse(url).hostname
    if response.status_code == 503 and not cloud.endswith('.indico.io'):
        raise IndicoError("Private cloud '%s' does not include api '%s'" % (cloud, api))

    json_results = response.json()
    results = json_results.get('results', False)
    if results is False:
        error = json_results.get('error')
        raise IndicoError(error)
    return results


def create_url(url_protocol, host, api, url_params):
    """
    Generate the proper url for sending off data for analysis
    """
    is_batch = url_params.pop("batch", None)
    apis = url_params.pop("apis", None)
    version = url_params.pop("version", None) or url_params.pop("v", None)
    method = url_params.pop('method', None)

    host_url_seg = url_protocol + "://%s" % host
    api_url_seg = "/%s" % api
    batch_url_seg = "/batch" if is_batch else ""
    method_url_seg = "/%s" % method if method else ""

    params = {}
    if apis:
        params["apis"] = ",".join(apis)
    if version:
        params["version"] = version

    url = host_url_seg + api_url_seg + batch_url_seg + method_url_seg
    if params:
        url += "?" + urlencode(params)

    return url
