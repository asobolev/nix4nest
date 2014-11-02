import unittest

import nest
import nix
# TODO find nicer injection way
import nix4nest


class TestNode(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.nest_id = nest.Create('iaf_neuron')[0]

        self.file = nix.File.open("/tmp/unittest.h5", nix.FileMode.Overwrite)
        self.block = self.file.create_nest_block("test block", "session")

        self.node = self.block.create_node(self.nest_id)

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_create_node(self):
        assert(self.node.name == str(self.nest_id))

        for k in nest.GetStatus([self.nest_id])[0].keys():
            assert(self.node.properties.has_property_by_name(str(k)))

    def test_block_nodes(self):
        assert(len(self.block.nodes) > 0)

        node = self.block.nodes[0]
        assert(self.node.name == node.name)
