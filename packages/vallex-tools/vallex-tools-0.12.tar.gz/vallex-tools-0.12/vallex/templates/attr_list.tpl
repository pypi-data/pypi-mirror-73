{% for lex in collection.lexemes %}
    {% for lu in lex.lexical_units %}
        {% for attr in lu.attribs.keys() %}{{ attr }}, {% endfor %}
    {% endfor %}
{% endfor %}
