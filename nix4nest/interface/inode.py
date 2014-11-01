from __future__ import absolute_import

from abc import ABCMeta, abstractmethod, abstractproperty


class INode:
    """ An Interface for any NEST node to be serialized with NIX. """

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        """ Object ID """
        pass

    @abstractproperty
    def properties(self):
        """ Object NEST properties to be serialized """
        pass

    @classmethod
    @abstractmethod
    def create_from_nest(cls, where, nest_id):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param where:   nix::Block where to create a Node
        :param nest_id: ID of the NEST Node
        :return:        an instance of <INode> object.
        """
        pass

    def __del__(self):
        """
        Delete related NIX object
        """
        del self._nix_source