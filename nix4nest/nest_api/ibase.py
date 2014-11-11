from __future__ import absolute_import

from abc import ABCMeta, abstractmethod, abstractproperty


class IBase:
    """ An Interface for any NEST node to be serialized with NIX. """

    __metaclass__ = ABCMeta

    _supported_types = (int, float, str)

    @staticmethod
    def _clean(value):
        if not type(value) in IBase._supported_types:
            return str(value)
        return value

    @abstractmethod
    def _fetch_properties(self):
        """
        Fetch properties from NEST state (usually with GetStatus)

        :return:    object state properties as dict
        :type:      dict
        """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Init object from NEST ID(s)
        """
        self._properties = {}

    @abstractproperty
    def name(self):
        """
        Object ID / name

        :return:    Object ID / name
        :type:      str
        """
        pass

    @property
    def type(self):
        """
        Object type

        :return:    Object type as string
        :type:      str
        """
        return self.properties['node_type']

    @property
    def properties(self):
        """
        Object NEST properties to be serialized

        :return:    dict of object properties
        :type:      dict
        """
        if not self._properties:

            for k, v in self._fetch_properties().items():
                self._properties[str(k)] = [IBase._clean(x) for x in v] if \
                    type(v) == list else IBase._clean(v)

        return self._properties