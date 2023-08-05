{% set tab='	' %}
{% for lex in collection.lexemes %}
    {% for lu in lex.lexical_units %}
{{ lu._id }}{{ tab }}{{ lex._id }}{{ tab }}{% for k, v in lu.lemma._data.items() %}{{ k }}: {{ v.strip() }}{% if not loop.last %}, {% endif %}{% endfor %}

    {% endfor %}
{% endfor %}
