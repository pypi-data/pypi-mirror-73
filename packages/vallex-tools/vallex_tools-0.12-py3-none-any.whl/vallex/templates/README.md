The files in this directory are Jinja2 templates used when converting vallex data into a specific
format. Each format should have a corresponding template named `format_name.tpl`. The
templates are evaluated with the context containing a single `db` variable, which is a
list of `Lexemes`. For attributes of `Lexemes` see [data_structures.py](../data_structures.py).
The template format is described in the [Template Designer Documentation](http://jinja.pocoo.org/docs/2.10/templates/).
