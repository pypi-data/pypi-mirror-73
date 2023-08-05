""" The Vallex Web Backend app




    This module provides handlers for the various web-app urls.
    The :func:`index` serves the basic ``index.html`` at ``/``, the :func:`static` method
    handler serves files from the ``frontend/dist/static`` directory at ``/static/``.
    The other handlers provide a `REST <https://en.wikipedia.org/wiki/Representational_State_Transfer>`-like
    API at ``/api/``. Currently only `JSON <https://www.json.org/>`_-encoded responses are implemented.
    The API is documented in the docstrings of the methods handling the API requests.
"""
import json
import logging
import re

from pathlib import Path
from urllib.parse import unquote

from vallex.vendor import bottle

from vallex.grep import grep, histogram, filter_db
from vallex.scripts import run_lu_scripts
from vallex.txt_parser import parse_lexical_unit
from vallex.txt_tokenizer import TokenStream
from vallex.utils import load_lexicon
from vallex.log import log

from .bottle_utils import WebAppFactory as factory, Environment, BadRequest, NotFound, Forbidden


@factory.route('/', method='GET')
def index(env: Environment):
    """
        Serves the ``frontend/dist/index.html`` containing the javascript app
        at the base url ``/``.
    """
    return bottle.static_file("index.html", root=str(env.state.config.web_dist_dir))  # type: ignore


@factory.route('/favicon.ico', method='GET')
def favicon(env: Environment):
    """
        Serves the ``frontend/dist/favicon.ico`` containing the favicon.
    """
    return bottle.static_file("favicon.ico", root=str(env.state.config.web_dist_dir))  # type: ignore


@factory.route('/api/lexical_unit/<id>/', method='POST', CORS=True, add_timestamp=True)
def update_lu(id: str, env: Environment):
    """
        Updates the textual source of the lexical unit whose id is `id`.

        The textual source is parsed and the lexicon collection is updated with the
        new lexical unit.


        :param id:                  The id of the lexical unit to update.

        :<json string src:          The new textual source of the lexical unit.

        :>json LexicalUnit result:  The newly parsed lexical unit.

        :status 404:                If a lexical unit with the provided id does not exist.


        **Example**:

        ..  http:example:: curl wget python-requests

            POST /api/lexical_unit/blu-v-brát-vzít-1/ HTTP/1.1
            Host: localhost:8080
            Accept: application/json
            Content-Type: application/json

            {
                "src": "~ impf: brát (si) pf: vzít (si) iter: brávat (si)\\n+ ACT(1;obl) PAT(4;obl) ORIG(od+2;opt)\\n   -synon: impf: přijímat; získávat pf: přijmout; získat"
            }


            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "ts": 1590609536.9895885,
                "result": {
                    "id": "blu-v-brát-vzít-1",
                    "__type__": "LexicalUnit",
                    "lemma": {
                        "__type__": "Lemma",
                        "type": "~",
                        "data": {
                            "impf": "brát (si)",
                            "pf": "vzít (si)",
                            "iter": "brávat (si)"
                        },
                        "comments":[]
                    },
                    "frame": {
                        "elements":[
                            {"functor":"ACT","forms":"1","oblig":"obl","__type__":"FrameElement"},
                            {"functor":"PAT","forms":"4","oblig":"obl","__type__":"FrameElement"},
                            {"functor":"ORIG","forms":"od+2","oblig":"opt","__type__":"FrameElement"}
                        ],
                        "comments":[],
                        "__type__": "Frame"
                    },
                    "attrs": {
                        "synon": {
                            "__type__":"Attrib",
                            "type": "synon",
                            "data": {
                                "impf": [["přijímat"], ["získávat"]],
                                "pf": [["přijímout"], ["získat"]]
                            }
                        }
                    }
                    "comments":[],
                    "errors":[],
                    "source": {
                        "start": {"__type__":"Location", "pos":92, "ln":3, "col":0},
                        "end": {"__type__":"Location", "pos":531, "ln":6, "col":0},
                        "text": "~ impf: brát (si) pf: vzít (si) iter: brávat (si)\\n+ ACT(1;obl) PAT(4;obl) ORIG(od+2;opt)\\n   -synon: impf: přijímat; získávat pf: přijmout; získat"
                    }

                }
            }

    """
    if env.state.config.web_mode != 'client':
        raise Forbidden("Editing lexical units not allowed in server mode.")

    env.state.store.refresh()
    try:
        old_lu = env.state.store.id2lu(id)
    except KeyError:
        log('server:api:update_lu', logging.WARN, f'Lexical unit {id} does not exist. Request: {env.request.json}.')
        raise NotFound('Lexical unit ', id, 'not found.')
    new_lu_src = env.request.json.get('src')
    new_lu = parse_lexical_unit(TokenStream(new_lu_src, fname=old_lu._src_start._fname), old_lu._parent)  # type: ignore
    if new_lu._id != old_lu._id:
        log('server:api:update_lu', logging.WARN, f"Editing lexical unit ids is not implemented. ({old_lu._id} => {new_lu}).")
        raise BadRequest("Editing lexical unit ids is not implemented.")
    new_lu = env.state.store.update_lu(old_lu, new_lu, 'web')
    run_lu_scripts(new_lu, 'compute')
    new_lu._errors = run_lu_scripts(new_lu, 'test')
    return {'result': new_lu}


@factory.route('/api/search', method='POST', CORS=True, compress=True, add_timestamp=True)
def search(env: Environment):
    """
        Searches the lexicon collection for lexical units matching
        a provided pattern.

        The query argument is passed to the :func:`grep <vallex.grep.grep>`
        function along with the currently loaded lexicon collection.

        :<json List[str] query: A list of strings, each string of the
                                form ``key=pattern``, with ``pattern`` a regular expression
                                and ``key`` a dot-separated match key.
        :<json bool id_only:    Controls whether the full lexical units are returned
                                or just their ids; defaults to ``False``.


        :>json list result:     The matching lexical units grouped into Lexemes as a list.
                                If `id_only`` is True key, then it is a list of
                                ``(lexeme_id, lexical_unit_id)`` pairs instead, one pair
                                for each matching lexical unit.

        :status 400:            If the ``query`` is not provided or not in the required
                                format or one of the regular expressions is invalid (e.g. wrong syntax).
    """
    try:
        patterns = []
        for cond in env.request.json['query']:
            attr_path, pattern = cond.split('=', 1)
            patterns.append((attr_path.split('.'), re.compile(pattern, re.DOTALL)))
    except Exception as ex:
        log('server:api:search', logging.WARN, f'Error parsing pattern. Query: {env.request.json["query"]}. Got exception: {ex}')
        raise BadRequest("Error parsing pattern:", ex)

    # If 'id_only' parameter present and true in the request,
    # only return matched lexical unit ids instead of full lexical units
    # save bandwith
    id_only = env.request.json.get('id_only', False)
    for key, pat in patterns:
        env.state.update_stat(key='.'.join(key), pattern=pat.pattern, table='search', user='web')
    res, stats = grep(env.state.store.lexemes, patterns, id_only=id_only)
    return {'result': res, 'stats': stats, 'data_version': list(env.state.vallex.version)}


@factory.route('/api/lexical_unit/<id>/match_map', method='GET', CORS=True, compress=True)
def match_map(id: str, env: Environment):
    """
        Returns a map mapping match keys to their respective match values for a
        specified lexical unit.

        :>json dict result:         A mapping of match keys to match values.

        :status 404:                The lexical unit was not found.
    """
    try:
        ret = {}
        lu = env.state.store.id2lu(id)
        for mk, _ in lu.match_keys():
            ret[mk] = list(lu.match_key_values(mk.split('.')))
        return {'result': ret}
    except KeyError:
        log('server:api:match_map', logging.WARN, f'Lexical unit {id} does not exist')
        raise NotFound("Lexical unit", id, "does not exist.")


@factory.route('/api/stats', method='GET', CORS=True, compress=True)
def stats(env: Environment):
    """
        Computes several statistics (currently only a histogram) on the set
        of lexical units matching a query.

        :<json str query:           A ``#`` separated list of conditions where each
                                    condition is a string of the form ``key=pattern``,
                                    with ``pattern`` a regular expression
                                    and ``key`` a dot-separated match key.
        :<json str select_pattern:  A regular expression to be passed to the
                                    :func:`histogram <vallex.grep.histogram>` function;
                                    optional, defaults to ``.*``



        :>json dict result:         A dictionary with two keys: The ``bins`` key contains the
                                    counts for each encountered value and the ``total`` key contains
                                    the total number of values encountered.

        :status 400:                If the ``query`` argument is not provided or not in the required
                                    format or one of the regular expressions is invalid (e.g. wrong syntax).
    """

    try:
        patterns = []
        if env.request.GET['query']:
            for cond in json.loads(unquote(env.request.GET['query'])):
                attr_path, pattern = cond.split('=')
                patterns.append((attr_path.split('.'), re.compile(pattern, re.DOTALL)))
        key = unquote(env.request.GET['key']).split('.')
        if env.request.GET['select_pattern']:
            select_pat = re.compile(unquote(env.request.GET['select_pattern']))
        else:
            select_pat = re.compile('.*')
    except Exception as ex:
        log('server:api:stats', logging.WARN, f'Error parsing pattern. Query: {env.request.GET["query"]}. Select: {env.request.GET["select_pattern"]}. Got exception: {ex}')
        raise BadRequest("Error parsing pattern:", ex)

    coll = filter_db(env.state.store.collection, patterns, no_sort=True)
    print("Computing histogram for", key, select_pat, "restricted to", patterns)
    occurrences, unique_lus = histogram(coll, key, select_pat)
    env.state.update_stat(key='.'.join(key), pattern=select_pat.pattern, table='histogram', user='web')

    return {'result': {'occurrences': occurrences, 'unique_lus': unique_lus}}


@factory.route('/api/rpc/<method>', method='POST', CORS=True)
def rpc_meth(method: str, env: Environment):
    """
        Executes an action on the server.

        The actions currently available are:

        - save:     saves all modified lexicons to disk in textual format
        - reload:   reloads lexicons which have changed on disk

        :param method:      The action to execute.


        :<json args:        Arguments needed by the action

        :>json dict result: Results of the action

        :status 303:        The app runs in ``server`` mode in which it does not allow executing actions.
        :status 400:        Bad arguments to the action
        :status 404:        Invalid action
    """
    if env.state.config.web_mode != 'client' and method != 'log':
        raise Forbidden("RPC calls not allowed in server mode.")

    if method == 'save':
        for lexicon in env.state.store.changed_lexicons():
            if lexicon.changed_on_disk(since=env.state.store.get_lexicon_version(lexicon)):
                env.state.add_message("File", lexicon._path, "changed by another application, moving it to",
                                      lexicon._path+'.backup', "and overwriting with the web version")
                Path(lexicon._path).rename(lexicon._path+'.backup')
            lexicon.write_to_disk()
            env.state.store.update_lexicon_version(lexicon)

    elif method == 'reload':
        for lexicon in env.state.store.lexicons:
            if lexicon.changed_on_disk(since=env.state.store.get_lexicon_version(lexicon)):
                with open(lexicon._path, 'r', encoding='uft-8') as LEX_SRC:
                    updated_lexicon = load_lexicon(LEX_SRC)
                env.state.store.update_lexicon(updated_lexicon)
                env.state.store.update_lexicon_version(updated_lexicon)

    elif method == 'log':
        LEVEL_MAP = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNINNG': logging.WARNING,
            'ERROR': logging.ERROR,
        }
        try:
            area = env.request.json['area']
            level = LEVEL_MAP[env.request.json['level']]
            message = env.request.json['message']
            log('frontend:'+area, level, message)
        except Exception as ex:
            log('server:api:rpc:log', logging.ERROR, f'rpc:log could not log. Request data: {env.request.json}. Got exception: {ex}')
            raise BadRequest("Bad request")
    else:
        raise NotFound("Method", method, "does not exist.")


@factory.route('/api/messages', method='GET', CORS=True, compress=True, add_timestamp=True)
def messages(env: Environment):
    timestamp = float(env.request.GET.get('timestamp', 0))
    with env.state.store.execute_sql("SELECT * FROM messages WHERE timestamp > ?", (timestamp, )) as msgs:
        return {'result': [m.items() for m in msgs]}


@factory.route('/api/changes', method='GET', CORS=True, compress=True, add_timestamp=True)
def changes(env: Environment):
    """
        Returns all lexical units which have changed since the specified timestamp.

        :<param float timestamp:    Since what time to return changes. Specified
                                    in seconds since the start of the Unix epoch.

        :>json dict result:         A list of LexicalUnits which have changed,

        :status 400:                If the ``query`` argument is not provided or not in the required
                                    format or one of the regular expressions is invalid (e.g. wrong syntax).
    """
    try:
        timestamp = float(env.request.GET.get('timestamp'))
    except Exception:
        raise BadRequest("Timestamp not provided or not a number.")
    return {'result': env.state.store.lu_changed_since(timestamp)}


@factory.route('/api/config', method='GET', CORS=True, compress=True)
def config(env: Environment):
    """
        Returns frontend configuration.

        :<json dict result:         The configuration object.
    """
    return {'result': env.state.frontend_config, 'backend_version': env.state.backend_version}


@factory.route('/api/attribs', method='GET', CORS=True)
def list_attribs(env: Environment):
    """
        Returns lexical unit attribute names which appear at least once.

        :<json list result:         A list of attribute names (simple strings)
    """

    return {'result': [{'name': attr, 'desc': desc} for attr, desc in env.state.vallex.attrs]}


@factory.route('/api/sources', method='GET', CORS=True)
def list_sources(env: Environment):
    """
        Returns a list of loaded lexicons.

        :<json list result:         A list of lexicons (simple strings)
    """
    return {'result': [str(src) for src in env.state.store.sources]}


@factory.route('/api/tests', method='GET', CORS=True)
def list_tests(env: Environment):
    """
        Returns a list of data validation tests.

        :<json list result:    A list of data-validation tests. Each test is an object with a ``name`` key,
                               containing the test name, and a ``doc`` key, containing
                               a description of the test.
    """
    return {'result': env.state.vallex.tests}


@factory.route('/api/help/toc', method='GET', CORS=True)
def get_help_toc(env: Environment):
    """
        Returns help contents

        :<json dict result:    Help contents.

    """
    return {'result': env.state.help_toc}


@factory.route('/api/help/guide/<section>/', method='GET', CORS=True)
def get_guide_section(section: str, env: Environment):
    """
        Returns a section from the help guide

        :<json dict result:    A dict containing the html content in the ``result`` key.

        :status 400:           If the section does not exist in the guide.
    """
    if '..' in section:
        raise BadRequest("Invalid section", section)
    try:
        section = section.replace('..', '')
        section_path = env.state.HELP_DIR/'content'/'guide'/section
        return {'result': section_path.read_text(encoding='utf-8')}
    except Exception as ex:
        log('server:api:help', logging.ERROR, f'get_guide_section could not load section {section}. Looked for {section_path}. Got exception: {ex}')
        raise NotFound("Section", section, "does not exist.")


@factory.route('/api/help/topics/<topic>/', method='GET', CORS=True)
def get_help(topic: str, env: Environment):
    """
        Returns help on the given topic.

        :<json dict result:    A dict containing at least a ``title`` and a ``content`` key,
                               The ``content`` key contains a html snippet with the help text.

        :status 400:           If there is no help on the given topic.
    """
    try:
        result = {}  # type: ignore
        meta = env.state.help_toc["topics"][topic]
        result.update(meta)
        topic_dir = env.state.HELP_DIR/'content'/'topics'
        result['content'] = content = (topic_dir/meta['content']).read_text(encoding='utf-8')
        return {'result': result}
    except Exception as ex:
        log('server:api:help', logging.ERROR, f'get_help_topic could not find topic {topic}. Searched in: {topic_dir}. Got exception: {ex}. ')
        raise NotFound("help on", topic, "does not exist.")


@factory.route('/static/help/<path:path>', method='GET')
def static_help(path: str, env: Environment):
    """
        Serves files from the ``frontend/help/static`` directory.
    """
    return bottle.static_file(path, root=str(env.state.HELP_DIR/'static'))  # type: ignore


@factory.route('/static/<path:path>', method='GET')
def static(path: str, env: Environment):
    """
        Serves files from the ``frontend/dist/static`` directory.
    """
    return bottle.static_file(path, root=str(env.state.STATIC_DIR))  # type: ignore
