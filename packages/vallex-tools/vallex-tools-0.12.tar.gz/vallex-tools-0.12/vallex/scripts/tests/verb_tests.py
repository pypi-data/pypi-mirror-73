import re

from vallex.scripts import TestDoesNotApply, TestFailed, requires, provides


def test_lu_acc_without_deagent(lu):
    """
        Verbs that allow accusative form of one of their complementations
        must also allow the deagentive diathesis.
    """
    forms = sum([fe.forms for fe in lu.frame.elements], [])
    has_acc = '4' in forms or 'adj-4' in forms

    if not has_acc or lu.isReflexverb:
        raise TestDoesNotApply

    deagent = 'diat' in lu.attribs and 'deagent' in lu.attribs['diat']._data

    if not deagent:
        raise TestFailed()


def test_lu_chybejici_pat(lu):
    """
        Ramce, ve kterych je ADDR|EFF|ORIG, ale ne PAT (tedy zanedbany princip posouvani) -- s vyjimkou ramcu obsahujicich [CD]PHR
    """

    functors = {fe.functor for fe in lu.frame.elements}

    if 'ACT' not in functors:
        raise TestDoesNotApply

    if 'ADDR' not in functors and "ORIG" not in functors and 'EFF' not in functors:
        raise TestDoesNotApply

    if 'CPHR' in functors or 'DPHR' in functors:
        raise TestDoesNotApply

    if 'PAT' not in functors:
        raise TestFailed()


def test_lu_chybejici_act(lu):
    """
        Ramce, ve kterych je PAT|CPHR|DPHR, ale ne ACT
    """
    if lu.isVerb == ['False']:
        raise TestDoesNotApply

    functors = {fe.functor for fe in lu.frame.elements}

    if 'PAT' not in functors and "CPHR" not in functors and 'DPHR' not in functors:
        raise TestDoesNotApply

    if 'ACT' not in functors:
        raise TestFailed()


def test_lu_example_lvc_count(lu):
    """
        Atribut example by měl mít přesně tolik příkladů pro každý vid, kolik je hodnot v lvc.
    """
    failures = []
    lvc_varianty = [k for k in lu.attribs.keys() if k.startswith('lvc')]
    for attrib in lvc_varianty:
        ex_name = 'example' if attrib == 'lvc' else 'example' + attrib[-1]
        if ex_name not in lu.attribs:
            failures.append("Missing examples for "+attrib)
        else:
            exs = lu.attribs[ex_name]._data
            expected_len = sum([len(v) for v in lu.attribs[attrib]._data.values()])
            for vid, vexs in exs.items():
                if len(vexs) != expected_len:
                    failures.append("Number of examples ("+str(len(exs[vid]))+") for "+attrib+" does not match number of ids ("+str(expected_len)+") in aspect "+vid)
    if failures:
        raise TestFailed("\n".join(failures))


@requires('lumap')
def test_lu_lvc_references(lu, lumap):
    """
        In attributes with links, each link should point to an existing lu.
    """
    failures = []
    lvc_variants = [k for k in lu.attribs.keys() if k.startswith('lvc')]
    if not lvc_variants:
        raise TestDoesNotApply
    applies = False
    for attrib in lvc_variants:
        if not isinstance(lu.attribs[attrib]._data, dict):
            continue
        refs = lu.attribs[attrib]._data['ids']
        if refs:
            applies = True
            for ref in refs:
                if not ref._id.startswith('@') and ref._id not in lumap:
                    failures.append(str(ref._id))
    if failures:
        raise TestFailed("The following references not found in db: "+','.join(failures))


def test_lexicon_chybejici_varianta(lexicon):
    """
        Slovesa, ktera jsou jednou uvedena s variantou, by se nikdy nemela vyskytovat bez ni (ignorujeme se/si)
    """
    variants = {}
    for lex in lexicon.lexemes:
        for lu in lex.lexical_units:
            for vb in lu.lemma._data.values():
                # Throw away any si / se
                vb = re.sub(r"\s*\(?\s*s[ei]\s*\)?\s*", "", vb)
                vars = vb.split('/')
                if len(vars) > 1:
                    variants.update({v.strip(): lu for v in vars})

    if not variants:
        raise TestDoesNotApply

    for lex in lexicon.lexemes:
        for lu in lex.lexical_units:
            for vb in lu.lemma._data.values():
                # Throw away any si / se
                vb = re.sub(r"\s*\(\s*s[ei]\s*\)\s*", "", vb).strip()
                if '/' not in vb:
                    applies = True
                    if vb in variants:
                        raise TestFailed("Lemma "+vb+" has no variant in "+lu._id+" but has a variant in "+variants[vb]._id)
    return str(len(variants))+" instances passed"


def test_lu_dublovana_forma(lu):
    """
        Ramce by neměly mít v témže slotu jednu formu dvakrát
    """
    for frame_elt in lu.frame.elements:
        if len(frame_elt.forms) != len(set(frame_elt.forms)):
            raise TestFailed()


def test_lu_reciprocal_verbs_attrs(lu):
    """
        Verbs having reflexverb=derived-recipr need to also have
        values for `recipr`, `reciprevent` and `reciprverb`
        attributes.
    """
    if lu.isVerb == ['False'] or not lu.reflexverb or 'derived-recipr' not in lu.reflexverb[0]:
        raise TestDoesNotApply
    failures = []
    if not lu.recipr.src:
        failures.append("recipr")
    if not lu.reciprevent:
        failures.append("reciprevent")
    if not lu.reciprverb:
        failures.append("reciprverb")
    if failures:
        raise TestFailed("Missing attributes: " + ','.join(failures))
