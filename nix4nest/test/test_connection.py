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

        self.conn = self.block.dump_connection(self.source_id, self.target_id)

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_create_connection(self):
        not_connected = nest.Create('iaf_neuron')[0]
        try:
            self.block.dump_connection(self.source_id, not_connected)
            raise AssertionError('No connection should raise error')
        except ValueError:
            pass

        assert(self.block.metadata.find_sections(lambda x: x.name == self.conn.name))

    def test_block_neurons(self):
        assert(len(self.block.connections) > 0)

        conn = self.block.connections[0]
        assert(self.conn.name == conn.name)