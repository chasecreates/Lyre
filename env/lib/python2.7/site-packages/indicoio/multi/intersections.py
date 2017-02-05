from .utils import MULTIAPI_NOT_SUPPORTED
from ..text import TEXT_APIS
from ..image import IMAGE_APIS
from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator
from ..utils.errors import IndicoError


API_TYPES = {}
API_TYPES.update({api: "text" for api in TEXT_APIS.keys()})
API_TYPES.update({api: "image" for api in IMAGE_APIS.keys()})

@detect_batch_decorator
def intersections(data, apis = None, **kwargs):
    """
    Helper to make multi requests of different types.

    :param data: Data to be sent in API request
    :param type: String type of API request
    :rtype: Dictionary of api responses
    """
    # Client side api name checking
    for api in apis:
        assert api not in MULTIAPI_NOT_SUPPORTED

    # remove auto-inserted batch param
    kwargs.pop('batch', None)

    if not isinstance(apis, list) or len(apis) != 2:
        raise IndicoError("Argument 'apis' must be of length 2")
    if isinstance(data, list) and len(data) < 3:
        raise IndicoError(
            "At least 3 examples are required to use the intersections API"
        )

    api_types = list(map(API_TYPES.get, apis))
    if api_types[0] != api_types[1]:
        raise IndicoError(
            "Both `apis` must accept the same kind of input to use the intersections API"
        )

    cloud = kwargs.pop("cloud", None)

    url_params = {
        'batch': False,
        'api_key': kwargs.pop('api_key', None),
        'apis': apis
    }

    return api_handler(data, cloud=cloud, api="apis/intersections", url_params=url_params, **kwargs)
