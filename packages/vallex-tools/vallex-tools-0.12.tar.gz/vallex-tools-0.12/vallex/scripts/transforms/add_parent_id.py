from vallex import Attrib
from vallex.scripts import changes


@changes('parentid')
def transform_lu_add_parent_id(lu):
    parent_id = Attrib('parentid')
    parent_id._data = lu._parent._id
    lu.attribs['parentid'] = parent_id
