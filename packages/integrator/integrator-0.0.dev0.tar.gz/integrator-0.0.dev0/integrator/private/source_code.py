""" representation of code and code changes """

# pylint: disable=too-few-public-methods


class SourceCodeInterface:
    """ Interface for obtainable source code "object" """
    @property
    def source(self):
        """ Get the CodeLocation for the object """
        raise NotImplementedError


class CodeLocation(SourceCodeInterface):
    """
    An abstract address of some source code, and the needed abstraction to
    obtain the source locally.
    """
    @property
    def source_type(self):
        """ Source type identifier, e.g. 'git' """
        raise NotImplementedError

    @property
    def source(self):
        return self


class CodeChange(SourceCodeInterface):
    """
    Representation of change => two different source locations.
    """
    def __init__(self, old_code, new_code):
        self.old_code = old_code
        self.new_code = new_code

    @property
    def source(self):
        return self.new_code


class CodeChangeRequest(SourceCodeInterface):
    """
    Proposed code change (pull-request, merge-request, patch, etc.).  This
    points at the change itself (old code + new code) and location of the
    destination code the code is meant to be applied onto.
    """
    def __init__(self, destination, change):
        self.destination = destination
        self.change = change

    @property
    def source(self):
        return self.change.source


class GitCodeLocation(CodeLocation):
    """
    Addressable git code location.
    """
    source_type = "git"

    def __init__(self, clone_url, committish):
        self.clone_url = clone_url
        self.committish = committish
