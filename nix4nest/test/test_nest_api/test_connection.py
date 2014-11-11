import unittest

import nest
from nix4nest.nest_api.models.connection import NestConnection


class TestConnection(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.source_id = nest.Create('iaf_neuron')[0]
        self.target_id = nest.Create('iaf_neuron')[0]
        nest.Connect([self.source_id], [self.target_id])

        self.node = NestConnection(self.source_id, self.target_id)

    def tearDown(self):
        nest.ResetKernel()

    def test_properties(self):
        nest_conn = nest.GetConnections([self.source_id], [self.target_id])

        for k in nest.GetStatus(nest_conn)[0].keys():
            assert(k in self.node.properties)