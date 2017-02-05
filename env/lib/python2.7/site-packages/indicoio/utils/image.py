"""
Image Utils
Handles preprocessing images before they are sent to the server
"""
import os.path, base64, re, warnings
from six import BytesIO, string_types, PY3

from PIL import Image

from indicoio.utils.errors import IndicoError

B64_PATTERN = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)")

def image_preprocess(image, size=None, min_axis=None, batch=False):
    """
    Takes an image and prepares it for sending to the api including
    resizing and image data/structure standardizing.
    """
    if batch:
        return [image_preprocess(img, size=size, min_axis=min_axis, batch=False) for img in image]

    if isinstance(image, string_types):
        b64_or_url = re.sub('^data:image/.+;base64,', '', image)
        if os.path.isfile(image.encode("utf-8", "ignore")):
            # check type of element
            out_image = Image.open(image)
        else:
            return b64_or_url

    elif isinstance(image, Image.Image):
        out_image = image
    elif type(image).__name__ == "ndarray": # image is from numpy/scipy
        if "float" in str(image.dtype) and image.min() >= 0 and image.max() <= 1:
            image *= 255.
        try:
            out_image = Image.fromarray(image.astype("uint8"))
        except TypeError as e:
            raise IndicoError("Please ensure the numpy array is acceptable by PIL. Values must be between 0 and 1 or between 0 and 255 in greyscale, rgb, or rgba format.")

    else:
        raise IndicoError("Image must be a filepath, url, base64 encoded string, or a numpy array")

    if size or min_axis:
        out_image = resize_image(out_image, size, min_axis)

    # convert to base64
    temp_output = BytesIO()
    out_image.save(temp_output, format='PNG')
    temp_output.seek(0)
    output_s = temp_output.read()

    return base64.b64encode(output_s).decode('utf-8') if PY3 else base64.b64encode(output_s)

def resize_image(image, size, min_axis):
    if min_axis:
        min_idx, other_idx = (0,1) if image.size[0] < image.size[1] else (1,0)
        aspect = image.size[other_idx]/float(image.size[min_idx])
        if aspect > 10:
            warnings.warn(
                "An aspect ratio greater than 10:1 is not recommended",
                Warning
            )
        size_arr = [0,0]
        size_arr[min_idx] = size
        size_arr[other_idx] = int(size * aspect)
        image = image.resize(tuple(size_arr))
    elif size:
        image = image.resize(size)
    return image


def get_list_dimensions(_list):
    """
    Takes a nested list and returns the size of each dimension followed
    by the element type in the list
    """
    if isinstance(_list, list) or isinstance(_list, tuple):
        return [len(_list)] + get_list_dimensions(_list[0])
    return []


def get_element_type(_list, dimens):
    """
    Given the dimensions of a nested list and the list, returns the type of the
    elements in the inner list.
    """
    elem = _list
    for _ in range(len(dimens)):
        elem = elem[0]
    return type(elem)
