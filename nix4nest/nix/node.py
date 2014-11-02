from __future__ import absolute_import


class Node(object):

    def __init__(self, nix_source):
        self._nix_source = nix_source

    @property
    def name(self):
        """ Object name / ID """
        return str(self._nix_source.name)

    @property
    def properties(self):
        """ Object NEST properties to be serialized """
        return self._nix_source.metadata

    def __del__(self):
        """ Delete related NIX object """
        del self._nix_source