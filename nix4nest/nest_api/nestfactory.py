from nix4nest.nix.node import Node
from nix4nest.nix.connection import Connection
from nix4nest.nix.signal import Signal
from nix4nest.nix.spiketrain import SpikeTrain
from nix4nest.nest_api.models.node import NestNode
from nix4nest.nest_api.models.connection import NestConnection
from nix4nest.nest_api.models.multimeter import NestMultimeter
from nix4nest.nest_api.models.spike_detector import NestSpikeDetector
# TODO replace imports by *


class NestFactory(object):
    """
    A factory class to create proper NIX objects from NEST entities.

    The class uses actual global state (NEST feature) to build objects.
    This is the only nix-dependent class in the NEST API.
    """

    @staticmethod
    def dump_node(where, nest_id, name=None):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param where:   nix::Block where to create a Node
        :param nest_id: ID of the NEST Node
        :param name:    save Node under a given name (to avoid duplicates)
        :return:        an instance of <INode> object.
        """
        assert(type(nest_id) == int)

        node = NestNode(nest_id)
        final_name = name or node.name

        return Node.create_node(where, final_name, node.type, node.properties)

    @staticmethod
    def dump_connection(where, source_id, target_id, name=None):
        """
        Factory method to build an connection instance from actual NEST global
        state using a nest source and target IDs.

        :param where:       nix::Block where to create a Node
        :param source_id:   ID of the source NEST Node
        :param target_id:   ID of the target NEST Node
        :param name:        save Connection under a given name (to avoid duplicates)
        :return:            an instance of <IConnection> object.
        """
        assert(type(source_id) == int)
        assert(type(target_id) == int)

        cn = NestConnection(source_id, target_id)
        final_name = name or cn.name

        return Connection.create_connection(where, final_name, cn.type, cn.properties)

    @staticmethod
    def dump_multimeter(where, nest_id, recordable, name=None):
        """
        Factory method to dump recorded signals from a Multimeter with a given
        NEST ID.

        :param where:       nix::Block where to create a signal
        :param nest_id:     NEST ID of the multimeter
        :param recordable:  name of the recordable (like 'V_m')
        :param name:        save Signal under a given name (to avoid duplicates)
        :return:            an instance of <AnalogSignal> object.
        """
        assert(type(nest_id) == int)

        mm = NestMultimeter(nest_id, recordable)
        final_name = name or mm.name

        signal = Signal.create_signal(where, final_name, mm.data, mm.unit, mm.interval)

        if len(mm.senders) > 0:

            c1 = lambda x: bool(x.metadata)
            c2 = lambda x: 'global_id' in x.metadata
            c3 = lambda x: x.metadata['global_id'].values[0].value == mm.senders[0]

            sources = where.find_sources(lambda x: c1(x) and c2(x) and c3(x))
            if sources:
                signal.source = Node(sources[0])

        return signal

    @staticmethod
    def dump_spike_detector(where, nest_id, prefix=None):
        """
        Factory method to dump recorded spike times from a Spike Detector with a
        given NEST ID.

        :param where:       nix::Block where to create a signal
        :param nest_id:     NEST ID of the spike detector
        :param prefix:      save spikes with a given prefix (to avoid duplicates)
        :return:            list of <SpikeTrain> instances.
        """
        assert(type(nest_id) == int)

        sd = NestSpikeDetector(nest_id)

        spiketrains = []
        for sender in sd.senders_list:
            times = sd.get_spike_times(sender)
            final_name = prefix + str(sender) if prefix else str(sender)

            st = SpikeTrain.create_spiketrain(where, final_name, times)

            c1 = lambda x: bool(x.metadata)
            c2 = lambda x: 'global_id' in x.metadata
            c3 = lambda x: x.metadata['global_id'].values[0].value == sender

            sources = where.find_sources(lambda x: c1(x) and c2(x) and c3(x))
            if sources:
                st.source = Node(sources[0])

            spiketrains.append(st)

        return spiketrains