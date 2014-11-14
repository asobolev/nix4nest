from datetime import datetime


class NixBase(object):

    def __init__(self, nix_object):
        self._nix_object = nix_object

    @property
    def name(self):
        """ Object name / ID """
        return str(self._nix_object.name)

    @property
    def type(self):
        """ Target ID for this connection """
        return self._nix_object.type

    @property
    def created_at(self):
        """ Target ID for this connection """
        return datetime.fromtimestamp(self._nix_object.created_at)

    @property
    def properties(self):
        """ Object NEST properties as dict """
        properties = {}

        if not self._nix_object.metadata:
            return {}

        for p in self._nix_object.metadata:
            key = p.name
            if len(p.values) == 1:
                value = p.values[0].value
            else:
                value = [x.value for x in p.values]

            properties[key] = value

        return properties