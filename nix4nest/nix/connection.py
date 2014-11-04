from __future__ import absolute_import


class Connection(object):

    def __init__(self, nix_source):
        self._nix_source = nix_source

    @property
    def name(self):
        """ Object name / ID """
        return str(self._nix_source.name)

    @property
    def type(self):
        """ Target ID for this connection """
        return self._nix_source.type

    @property
    def properties(self):
        """ Object NEST properties """
        return self._nix_source.metadata

    @property
    def source(self):
        """ Source ID for this connection """
        return self.properties['source']

    @property
    def target(self):
        """ Target ID for this connection """
        return self.properties['target']

    def __del__(self):
        """ Delete related NIX source object """
        del self._nix_source