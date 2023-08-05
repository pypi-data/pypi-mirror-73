from vallex.scripts import TestDoesNotApply, TestFailed, requires


def test_lu_correct_obligatory_type(lu):
    """
        Obligatornost "opt" je nepřípůstná pouze u rámců ACT|PAT|ADDR|EFF|ORIG|OBST|DIFF|INTT,
        naopak u těchto rámců je nepřípustná obligatornost "typ"
    """
    applies = False
    for frame_elt in lu.frame.elements:
        if frame_elt.oblig == 'typ':
            applies = True
            if frame_elt.functor in ['ACT', 'PAT', 'ADDR', 'EFF', 'ORIG', 'OBST', 'DIFF', 'INTT']:
                raise TestFailed()
        elif frame_elt.oblig == 'opt':
            applies = True
            if frame_elt.functor not in ['ACT', 'PAT', 'ADDR', 'EFF', 'ORIG', 'OBST', 'DIFF', 'INTT']:
                raise TestFailed()

    if not applies:
        raise TestDoesNotApply


def test_lexeme_id_prefixes(lexeme):
    """
        ID prefixes of all lexical units in a given lexeme should match
    """
    if len(lexeme.lexical_units) < 2:
        raise TestDoesNotApply

    pref = lexeme.lexical_units[0]._id
    pref = pref[:pref.rfind('-')]

    mismatched_lus = []
    for lu in lexeme.lexical_units:
        if not lu._id.startswith(pref):
            mismatched_lus.append(lu._id)

    if mismatched_lus:
        raise TestFailed("The following lu id's do not match the expected prefix '"+str(pref)+"' (from the first lu): "+','.join(mismatched_lus))


@requires('luidcount')
def test_lu_unique_lu_ids(lu, luidcount):
    """
        IDs of lexical units should be unique across a lexicon
    """
    if luidcount[lu._id] > 1:
        raise TestFailed("The lu id "+str(lu._id)+" is not unique, multiplicity: "+str(luidcount[lu._id]))

def test_lexicon_unique_lu_ids(lexicon):
    """
        IDs of lexical units should be unique across a lexicon
    """

    ids = {}
    bad_ids = set()
    for lu in lexicon.lexical_units:
        if lu._id in ids:
            bad_ids.add(lu._id)
        else:
            ids[lu._id] = True

    if bad_ids:
        raise TestFailed("The following lu id's were not unique: "+','.join(bad_ids))
