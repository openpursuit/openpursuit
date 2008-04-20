"""Autocomplete support for foreign keys.


from django.template import loader, Context
from django.utils.html import escape
from django.utils.html import clean_html
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from djangoOp.op.models import Tags


        t = loader.get_template('autocomplete_widget.html')
        c = Context({'cont': {'attrs' : flatatt(final_attrs), 'name' : name, 'id' : final_attrs['id'], 'url' : self.url, 'options' : plist_from_dict(self.options)}} )
        return t.render(c)

# View helper
    qs = Tags.objects.filter(tag__startswith=text)
