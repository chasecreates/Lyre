from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator


@detect_batch_decorator
def twitter_engagement(text, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given input text, returns an engagment score between 0 and 1

    Example usage:

    .. code-block:: python

       >>> import indicoio
       >>> import numpy as np
       >>> text = 'Monday: Delightful with mostly sunny skies. Highs in the low 70s.'
       >>> engagement = indicoio.twitter_engagement(text)

    :param text: The text to be analyzed.
    :type text: str or unicode
    :rtype: Float of engagement between 0 and 1
    """
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    return api_handler(text, cloud=cloud, api="twitterengagement", url_params=url_params, **kwargs)
