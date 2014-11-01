from __future__ import absolute_import


def ensure_nest_block(nixfile, block):
    assert(nixfile.is_open())

    # ensure metadata section for block exist
    if block.metadata is None:
        block.metadata = nixfile.create_section(block.name, 'root')

    # ensure metadata has 'sources' subsection
    if not block.metadata.find_sections(lambda x: x.name == 'sources'):
        block.metadata.create_section('sources', 'group')