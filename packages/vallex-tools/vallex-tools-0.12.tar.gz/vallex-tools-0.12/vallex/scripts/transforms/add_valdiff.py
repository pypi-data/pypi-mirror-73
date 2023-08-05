""" A transform for adding/recomputing the valdiff attribute in noun data




    ./vallex-cli --no-sort --output-format txt -o ../aktualni_data/data-txt/ scripts transform vallex/scripts/transforms/add_valdiff.py

    Note that the file with the verb data (v-vallex.txt) is exported empty.
"""

import logging
import sys
import os  # for better debugging

from vallex import Frame, Specval
from vallex.log import log
from vallex.scripts import changes, requires, TestDoesNotApply, TestFailed


@changes('valdiff')
@requires('lumap')
def transform_lu_add_valdiff(lu, lumap):
    if 'isNoun' not in lu.dynamic_attrs or not lu.dynamic_attrs['isNoun']._data:
        raise TestDoesNotApply
    if 'derivedV' not in lu.attribs or lu.attribs['derivedV']._data['ids'] == []:
        raise TestDoesNotApply
    try:
        verb = lumap[lu.attribs['derivedV']._data['ids'][0]._id]
        log("add_valdiff", logging.DEBUG, "first derivedV value of ", lu._id, ": ", verb._id)
    except Exception as ex:
        log("add_valdiff", logging.WARN, "error adding valdiff to ", lu, " with derivedV=", str(lu.attribs['derivedV']._data), " failed with: ", ex)
        raise TestFailed

    try:
        if lu._id in ['blu-n-velení-1', 'blu-n-velení-3', 'blu-n-vyučování-vyučení-1', 'blu-n-výuka-1']:
            changeset = {x: Specval.TYPICAL_CHANGES[x] for x in Specval.TYPICAL_CHANGES if x != '3'}   # in those two LUs, 3>2,pos should not be treated as a typical change
            ret = Specval.diff(verb.frame, lu.frame, changeset=changeset)
        else:
            ret = Specval.diff(verb.frame, lu.frame)

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log("add_valdiff", logging.ERROR, "computing valdiff for ", lu._id, " and the first source verb ", verb._id, " resulted in exception of ", exc_type, "in file", fname, "at line", exc_tb.tb_lineno)

    if len(lu.attribs['derivedV']._data['ids']) > 1:
        for verb_ref in lu.attribs['derivedV']._data['ids'][1:]:
            log("add_valdiff", logging.DEBUG, "later derivedV value of ", lu._id, ": ", verb_ref._id)
            try:
                verb = lumap[verb_ref._id]
            except Exception as ex:
                log("add_valdiff", logging.WARN, "error adding later value of derivedV to valdiff of ", lu, " with derivedV=", str(lu.attribs['derivedV']._data), " failed with: ", ex)
                raise TestFailed

            try:
                if lu._id in ['blu-n-velení-1', 'blu-n-velení-3', 'blu-n-vyučování-vyučení-1', 'blu-n-výuka-1']:
                    changeset = {x: Specval.TYPICAL_CHANGES[x] for x in Specval.TYPICAL_CHANGES if x != '3'}   # in those two LUs, 3>2,pos should not be treated as a typical change
                    spec_val = Specval.diff(verb.frame, lu.frame, changeset=changeset)
                else:
                    spec_val = Specval.diff(verb.frame, lu.frame)

                for slot in spec_val._data:
                    if slot.spec == "-":
                        ret._data.append(slot)
                    else:
                        list_slots = [i for i, oldslot in enumerate(ret._data) if oldslot.functor == slot.functor]
                        if len(list_slots) != 1:
                            log("add_valdiff", logging.ERROR, "there is not a unique slot with the", slot.functor, "functor: ", ' '.join([ret._data[i] for i in list_slots]))
                        else:
                            old_index = list_slots[0]
                            if slot.spec == '=':
                                ret._data[old_index].spec = '='  # even if it was added relative to the first verb

                            for form in slot.forms_eq:  # it is in the noun frame -> it was either eq or added
                                if form in ret._data[old_index].forms_add:
                                    log("add_valdiff", logging.DEBUG, "should treat form", form, "as equal, not added")
                                    ret._data[old_index].forms_eq.append(form)
                                    ret._data[old_index].forms_add.remove(form)
                            for form in slot.forms_del:  # it is not in the noun frame -> it either was not in valdiff or is already in forms_del
                                if not form in ret._data[old_index].forms_del:
                                    log("add_valdiff", logging.DEBUG, "should treat form", form, "as deleted")
                                    ret._data[old_index].forms_del.append(form)
                            # for form in slot.forms_add:
                                    # we do not need to do anything -- the form is either already added, or even eq
                            if slot.oblig_verb == slot.oblig_noun:  # we prefer no change in obligatoriness
                                ret._data[old_index].oblig_verb = slot.oblig_verb

            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                log("add_valdiff", logging.ERROR, "computing valdiff between ", lu._id, " and additional source verb ", verb._id, " resulted in exception of ", exc_type, "in file", fname, "at line", exc_tb.tb_lineno)

    lu.attribs[ret.name] = ret
    log("add_valdiff", logging.DEBUG, "exit transform_lu_add_valdiff, unit", lu._id, "has value", lu.attribs['valdiff'])
