from __future__ import absolute_import

from abc import ABCMeta, abstractmethod, abstractproperty


class IConnection:
    """
    An Interface for any NEST connection (synapse) to be serialized with NIX.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, source_id, target_id):
        """
        Init object from source and target NEST IDs

        :param source_id:   NEST ID
        :type:              int
        :param target_id:   NEST ID
        :type:              int
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

    @abstractproperty
    def source(self):
        """
        Source ID for this connection

        :return:    NEST ID of the source Node
        :type:      int
        """
        pass

    @abstractproperty
    def target(self):
        """
        Target ID for this connection

        :return:    NEST ID of the source Node
        :type:      int
        """
        pass
