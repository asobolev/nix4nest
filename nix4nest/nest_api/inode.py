from __future__ import absolute_import

from abc import ABCMeta, abstractmethod, abstractproperty


class INode:
    """ An Interface for any NEST node to be serialized with NIX. """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, nest_id):
        """
        Init object from its NEST ID

        :param nest_id: NEST ID
        """
        pass

    @abstractproperty
    def name(self):
        """
        Object ID / name

        :return:    Object ID / name
        :type:      str
        """
        pass

    @abstractproperty
    def properties(self):
        """
        Object NEST properties to be serialized

        :return:    dict of object properties
        :type:      dict
        """
        pass