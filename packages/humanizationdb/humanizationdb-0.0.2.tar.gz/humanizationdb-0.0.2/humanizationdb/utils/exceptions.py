class TableNotFound(Exception):
    """Raises if given table can not be found in database
    """
    pass

class AnnotationMissing(Exception):
    """Raises if annotation of IgObject is missing
    """
    pass