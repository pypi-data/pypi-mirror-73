{% macro indent(x) %}{% for i in range(x) %} {% endfor %}{% endmacro %}
{% set separator=' ' %}
{% for lexicon in collection.lexicons if lexicon.lexemes %}
# START ========== {{ lexicon.path }} ========== START
#
{% for c in lexicon._preamble %}
# {{ str(c) }}
{% endfor %}
{% for lex in lexicon.lexemes %}

* {{ lex._id }}{% for c in lex.comments %} #{{ str(c) }}
{% endfor %}{{ '' }}
{% for lu in lex.lexical_units %}{% if not loop.first %}

{% endif %}
 : id: {{ lu._id }}{% for c in lu.comments %} #{{ str(c) }}
{% endfor %}{{ '' }}
 ~ {% for k, v in lu.lemma._data.items() %}{{ k }}: {{ v.strip() }}{% if not loop.last %}{{ separator }}{% endif %}{% endfor %}{{ '' }}{% for c in lu.lemma.comments['all'] %} #{{ str(c) }}{% endfor %}{{ '' }}
 +{% if 'idiom' in lu.attribs %}i{% endif %}{% for f in lu.frame.elements %} {{ str(f) }}{% endfor %}{% for c in lu.frame.comments['all'] %} #{{ str(c) }}{% endfor %}{{ '' }}
  {% for attr in lu.attribs.values() %}{% if attr.duplicate %}{% set attr_name = attr.duplicate %}{% else %}{% set attr_name = attr.name %}{% endif %}
      {% if transformed_attrs and attr_name not in transformed_attrs and attr_name != 'idiom' %}
    {{ attr.src.strip() }}
      {% elif attr_name.startswith('example') and len(attr_name)<=8 %}
      {% set val_indent = len(attr_name)+6 %}
      {% set show_all = len(attr._data.items()) > 1 %}
    -{{ attr_name }}:
          {%- for aspect, val in attr._data.items() -%}
          {%- if not loop.first %}{{ indent(val_indent) }}{% endif -%}
	  {% if aspect != 'all' or show_all %}{% set aspect_indent = 2+len(aspect) %}{% else %}{% set aspect_indent = 1 %}{% endif %}
{{ '' }}{% if aspect != 'all' or show_all %} {{ aspect }}: {{ indent(4-len(aspect)) }}{% else %}{{ indent(1) }}{% endif %}
              {%- for ex in val -%}
              {%- if not loop.first %}{{ indent(val_indent+aspect_indent) }}{% endif -%}
{{ '' }}{{ ex }}{% if not loop.last %};{% endif %}{{ '' }}
              {% endfor %}{% if aspect in attr.comments %}{% for c in attr.comments[aspect] %} #{{ str(c) }}
              {% endfor %}{% endif %}
          {% endfor %}
      {% elif attr_name == 'synon' %}
      {% set val_indent = len(attr_name)+6 %}
      {% set show_all = 'all' in attr._data.keys() and len(attr._data.keys()) > 1%}
    -synon:
      {%- for aspect, groups in attr._data.items() -%}
        {%- if not loop.first %}{{ indent(val_indent) }}{% endif -%}
        {%- if aspect != 'all' or show_all %} {{ aspect }}: {{ indent(4-len(aspect)) }}{% else %}{{ indent(1) }}{% endif %}
              {%- for g in groups -%}{% for s in g %}{{ s }}{% if not loop.last %}, {% endif %}{% endfor %}{% if not loop.last %}; {% endif %}{% endfor %}{% if aspect in attr.comments %}{% for c in attr.comments[aspect] %} #{{ str(c) }} {% endfor %}{% endif %}{{ '' }}
          {% endfor %}
      {% elif attr_name.startswith('recipr') and len(attr_name)<=7 %}
        {% set val_indent = len(attr_name)+6 %}
    -{{ attr_name }}:
        {%- if 'all' in attr._data.keys() -%}
          {%- for spec, ex in attr._data['all'].items() -%}
            {%- if not loop.first %}{{ indent(val_indent+6) }}{% endif -%}
  {{ '' }} {{ spec }} {% for e in ex %}%{{e}}%{% if not loop.last %} {% endif %}{% endfor %}{{ '' }}
          {%- endfor -%}{% if 'all' in attr.comments %}{% for c in attr.comments['all'] %} #{{ str(c) }} {% endfor %}{% endif %}{{ '' }}
        {% endif %}
        {%- for aspect, val in attr._data.items()  -%}{%- if aspect != 'all' -%}
          {%- if not loop.first or 'all' in attr._data.keys() -%}{{ indent(val_indent) }}{%- endif -%}
  {{ '' }}{% if aspect != 'all' %} {{ aspect }}: {{ indent(4-len(aspect)) }}{% else %}{{ indent(1) }}{% endif %}
            {%- for spec, ex in val.items() -%}
              {%- if not loop.first %}{{ indent(val_indent+6) }}{% endif -%}
  {{ '' }}{{ spec }} {% for e in ex %}%{{e}}%{% if not loop.last %} {% endif %}{% endfor %}{{ '' }}
            {%- endfor -%}{% if aspect in attr.comments %}{% for c in attr.comments[aspect] %} #{{ str(c) }} {% endfor %}{% endif %}{{ '' }}
        {% endif %}{% endfor %}
      {% elif 'lvc' in attr_name or 'derivedN' in attr_name or 'derivedV' in attr_name or attr_name == 'ref' %}
    -{{ attr_name }}: {% for ref in attr._data['ids'] %}{{ ref._id }}{% if not loop.last %}{{ separator }}{% endif %}{% endfor %}{% if len(attr._data['lemmas']) > 0 %}|{% for l in attr._data['lemmas']%} {{ l }}{% endfor %}{% endif %}{% for c in attr.comments['all'] %}{{'\n'}}
                        #{{ str(c) }} {% endfor %}{{ '' }}
      {% elif attr_name == 'note' %}{% for note in attr._data %}
    -{{ attr_name }}: {{ note }}
      {% endfor %}
      {% elif attr_name == 'valdiff' %}
    -{{ attr_name }}: {{ str(attr) }}
      {% elif attr_name != 'idiom' %}
    -{{ attr_name }}: {{ str(attr._data) }}{% for c in attr.comments['all'] %} #{{ str(c) }}{% if not '\n' in str(c) -%}{{ '\n' }}{% endif %}{% endfor %}{{ '' }}
    {% endif %}
  {% endfor %}
{% endfor %}
{% endfor %}
#
# END ========== {{ lexicon.path }} ========== END

{% endfor %}


