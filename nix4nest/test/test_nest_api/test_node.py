import unittest

import nest
from nix4nest.nest_api.models.node import NestNode


class TestNode(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.nest_id = nest.Create('iaf_neuron')[0]
        self.node = NestNode(self.nest_id)

    def tearDown(self):
        nest.ResetKernel()

    def test_properties(self):
        assert(self.node.name == str(self.nest_id))

        for k in nest.GetStatus([self.nest_id])[0].keys():
            assert(k in self.node.properties)