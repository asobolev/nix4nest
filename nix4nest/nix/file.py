from nix import File as NixFile
from .inject import Inject


class FileMixin(NixFile):
    """
    This mixin adds NEST Block creation method to the original NIX::File
    """

    class __metaclass__(Inject, NixFile.__class__):
        # this injects all members and the doc into nix.core.File
        pass

    def create_nest_block(self, *args, **kwargs):
        block = self.create_block(*args, **kwargs)

        # ensure metadata section for block exist
        if block.metadata is None:
            block.metadata = self.create_section(block.name, 'root')

        # ensure metadata has 'sources' subsection
        if not block.metadata.find_sections(lambda x: x.name == 'sources'):
            block.metadata.create_section('sources', 'group')

        return block