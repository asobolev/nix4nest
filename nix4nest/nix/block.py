from nix import Block as NixBlock
from .inject import Inject
from nix4nest.nest_api.neuron import Neuron


class BlockMixin(NixBlock):
    """
    This mixin adds special methods to the original NIX::Block
    """

    class __metaclass__(Inject, NixBlock.__class__):
        # this injects all members and the doc into nix.core.File
        pass

    def neurons(self):
        sources = self.find_sources(lambda x: x.type == 'neuron')

        return [Neuron(x) for x in sources]