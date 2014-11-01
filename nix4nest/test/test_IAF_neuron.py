import unittest

import nest
import nix

from nix4nest.nest_api.iafneuron import IAFNeuron
from nix4nest.nest_api.utils import ensure_nest_block


class TestIAFNeuron(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.nest_id = nest.Create('iaf_neuron')[0]

        self.file = nix.File.open("/tmp/unittest.h5", nix.FileMode.Overwrite)
        self.block = self.file.create_block("test block", "recordingsession")

        ensure_nest_block(self.file, self.block)

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_create_from_nest(self):
        neuron = IAFNeuron.create_from_nest(self.block, self.nest_id)

        assert(neuron.name == str(self.nest_id))

        for k in nest.GetStatus([self.nest_id])[0].keys():
            assert(neuron.properties.has_property_by_name(str(k)))