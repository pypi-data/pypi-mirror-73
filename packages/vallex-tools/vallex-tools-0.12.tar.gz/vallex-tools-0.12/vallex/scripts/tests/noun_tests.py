from vallex.scripts import requires, TestDoesNotApply, TestFailed


@requires('lumap')
def test_lu_derived_references(lu, lumap):
    """
        The derived attribute should point to an existing lu.
    """
    failures = []
    derived_varianty = [k for k in lu.attribs.keys() if k.startswith('derived')]
    if not derived_varianty:
        raise TestDoesNotApply
    applies = False
    for attrib in derived_varianty:
        if not isinstance(lu.attribs[attrib]._data, dict):
            continue
        refs = lu.attribs[attrib]._data['ids']
        if refs:
            applies = True
            for ref in refs:
                if not ref._id.startswith('@') and ref._id not in lumap:
                    failures.append(str(ref._id))
        else:
            continue
    if failures:
        raise TestFailed("The following references not found in db: "+','.join(failures))
    if not applies:
        raise TestDoesNotApply
