import unittest

import nest
import nix
# TODO find nicer injection way
import nix4nest


class TestConnection(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.source_id = nest.Create('iaf_neuron')[0]
        self.target_id = nest.Create('iaf_neuron')[0]
        nest.Connect([self.source_id], [self.target_id])

        self.file = nix.File.open("/tmp/unittest.h5", nix.FileMode.Overwrite)
        self.block = self.file.create_nest_block("test block", "session")

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_create_connection(self):
        not_connected = nest.Create('iaf_neuron')[0]
        try:
            self.block.create_connection(self.source_id, not_connected)
            raise AssertionError('No connection should raise error')
        except ValueError:
            pass

        conn = self.block.create_connection(self.source_id, self.target_id)
        assert(self.block.metadata.find_sections(lambda x: x.name == conn.name))

    def test_block_neurons(self):
        conn = self.block.create_connection(self.source_id, self.target_id)
        assert(len(self.block.connections()) > 0)