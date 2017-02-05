"""
Contains Indico Custom Errors
"""

class IndicoError(ValueError):
    pass

class DataStructureException(Exception):
    """
    If a non-accepted datastructure is passed, throws an exception
    """
    def __init__(self, callback, passed_structure, accepted_structures):
        self.callback = callback.__name__
        self.structure = str(type(passed_structure))
        self.accepted = [str(structure) for structure in accepted_structures]

    def __str__(self):
        return """
        function %s does not accept %s, accepted types are: %s
        """ % (self.callback, self.structure, str(self.accepted))
