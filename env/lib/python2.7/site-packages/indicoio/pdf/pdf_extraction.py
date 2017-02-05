from ..utils.pdf import pdf_preprocess, postprocess_images
from ..utils.api import api_handler
from ..utils.decorators import detect_batch_decorator

@detect_batch_decorator
def pdf_extraction(pdf, cloud=None, batch=False, api_key=None, version=None, **kwargs):
    """
    Given a pdf, returns the text and metadata associated with the given pdf.
    PDFs may be provided as base64 encoded data or as a filepath.
    Base64 image data and formatted table is optionally returned by setting 
    `images=True` or `tables=True`.

    Example usage:

    .. code-block:: python

       >>> from indicoio import pdf_extraction
       >>> results = pdf_extraction(pdf_file)
       >>> results.keys()
       ['text', 'metadata']

    :param pdf: The pdf to be analyzed.
    :type pdf: str or list of strs
    :rtype: dict or list of dicts
    """
    pdf = pdf_preprocess(pdf, batch=batch)
    url_params = {"batch": batch, "api_key": api_key, "version": version}
    results = api_handler(pdf, cloud=cloud, api="pdfextraction", url_params=url_params, **kwargs)
    image_results = results.get('images')
    if image_results is not None:
        results['images'] = postprocess_images(image_results)
    return results
