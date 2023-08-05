"""
    Run with

        ./vallex-cli scripts mapreduce vallex/scripts/mapreducers/slovko.py

    If the script fails and you want a more verbose message, add `-v DEBUG`
    as an argument to `vallex-cli` before the `scripts` command. If you
    want to run the script on only a subset of the lexicon data, you can
    use the `--pre-pattern PATTERN` argument, which again goes before the
    `scripts` command:

        ./vallex-cli --pre-pattern SEARCH_PATTERN scripts mapreduce vallex/scripts/mapreducers/slovko.py
"""
from collections import defaultdict

from vallex.data_structures.attribs import Specval
from vallex.scripts import changes, requires, TestDoesNotApply
from vallex.scripts.mapreduce import emit


@requires('collection')
def map_table1_noun_verb_forms_summary(lu, collection):
    if lu.isNoun == ['False'] or not lu.valdiff:
        raise TestDoesNotApply

    noun = lu
    type_ = 'prod' if noun.productive == ['True'] else 'noprod'
    class_ = noun.class_[0] if noun.class_ else 'unspecified'

    for verb in [collection.id2lu(id) for id in noun.derivedV.ids]:
        # compute valdiff between verb and noun frame
        spec_val = Specval.diff(verb.frame, noun.frame)

        if set(verb.frame.actant).symmetric_difference(set(noun.frame.actant)):
            emit(('Total number of noun-verb pairs with different actants (ignored in stats)', class_, type_), 1)
            continue

        emit(('Total number of noun-verb pairs with equal actants', class_, type_), 1)

        emit(('Total number of ADVERBAL forms (with repetitions) of common actants', class_, type_), len(verb.frame.actant.form))
        emit(('Total number of ADNOMINAL forms (with repetitions) of common actants', class_, type_), len(noun.frame.actant.form))

        specific_form_count = 0
        typical_form_count = 0
        for funct in noun.frame.actant:
            specific_forms = getattr(spec_val, funct).form.add
            typical_forms = [form for form in getattr(noun.frame, funct).form if form not in specific_forms]
            specific_form_count += len(specific_forms)
            typical_form_count += len(typical_forms)

        emit(('Total number of COMMON or TYPICAL adnominal forms (with repetitions) of common actants', class_, type_), typical_form_count)
        emit(('Total number of SPECIFIC adnominal forms (with repetitions) of common actants', class_, type_), specific_form_count)


@requires('collection')
def map_table1b_differing_actant_summary(lu, collection):
    if lu.isNoun == ['False'] or not lu.valdiff:
        raise TestDoesNotApply

    noun = lu
    type_ = 'prod' if noun.productive == ['True'] else 'noprod'
    class_ = noun.class_[0] if noun.class_ else 'unspecified'

    for verb in [collection.id2lu(id) for id in noun.derivedV.ids]:
        spec_val = Specval.diff(verb.frame, noun.frame)

        del_actants = set(verb.frame.actant).difference(set(noun.frame.actant))
        add_actants = set(noun.frame.actant).difference(set(verb.frame.actant))
        common_actants = set(verb.frame.actant).intersection(set(noun.frame.actant))

        for functor in add_actants:
            emit(('Add (number of times actant was present in noun but not verb)', functor), 1)

        for functor in del_actants:
            emit(('Del (number of times actant was present in verb but not noun)', functor), 1)

        for functor in common_actants:
            emit(('Eq (number of times actant was shared between noun and verb)', functor), 1)


@requires('collection')
def map_table2_spec_nom_forms(lu, collection):
    if lu.isNoun == ['False'] or not lu.valdiff:
        raise TestDoesNotApply

    type_ = 'prod' if lu.productive == ['True'] else 'noprod'
    class_ = lu.class_[0] if lu.class_ else 'unspecified'

    for funct in lu.valdiff.actant.eq:
        emit((class_, funct, type_), list(getattr(lu.valdiff, funct).form.add))


def reduce_table2_spec_nom_forms(key, results):
    form_count = defaultdict(int)
    for forms in results:
        for form in forms:
            form_count[form] += 1
    return '; '.join([f+' ('+str(c)+'x)' for f, c in sorted(form_count.items(), key=lambda x:x[1], reverse=True)])+' (Total:'+str(sum(form_count.values()))+')'


@requires('collection')
def map_table3a_actant_spec_forms(lu, collection):
    if lu.isNoun == ['False'] or not lu.valdiff:
        raise TestDoesNotApply

    type_ = 'prod' if lu.productive == ['True'] else 'noprod'
    class_ = lu.class_[0] if lu.class_ else 'unspecified'

    # Actant functors which have at least one specific form
    # joined together by '+'
    actants_with_spec_form = '+'.join([funct for funct in lu.valdiff.actant.eq if getattr(lu.valdiff, funct).form.add])
    emit((class_, actants_with_spec_form, type_), 1)


@requires('collection')
def map_table3b_actant_spec_forms(lu, collection):
    if lu.isNoun == ['False'] or not lu.valdiff:
        raise TestDoesNotApply

    type_ = 'prod' if lu.productive == ['True'] else 'noprod'
    class_ = lu.class_[0] if lu.class_ else 'unspecified'

    # Actant functors which specific forms in parentheses (joined together by ',')
    # joined together by '+'
    actants_with_spec_form_including_form = '+'.join([funct+'('+','.join(getattr(lu.valdiff, funct).form.add)+')' for funct in lu.valdiff.actant.eq if getattr(lu.valdiff, funct).form.add])
    emit((class_, actants_with_spec_form_including_form, type_), 1)
