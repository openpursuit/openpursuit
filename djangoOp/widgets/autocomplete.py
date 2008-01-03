"""Autocomplete support for foreign keys.Requires the protoculous JavaScript library."""

# Widget# originally from http://www.djangosnippets.org/snippets/253/from django import newforms as formsfrom django.newforms.widgets import TextInput, flatattfrom django.newforms.util import smart_unicode
from django.template import loader, Context
from django.utils.html import escape
from django.utils.html import clean_html
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from djangoOp.op.models import Tags

class AutoCompleteField(TextInput):    def __init__(self, url='', options=None, attrs=None):        self.url = url        self.options = {'paramName': "text"}        if options:            self.options.update(options)        if attrs is None:            attrs = {}        self.attrs = attrs    def render(self, name, value=None, attrs=None):        final_attrs = self.build_attrs(attrs, name=name)        if value:            value = smart_unicode(value)            final_attrs['value'] = escape(value)        if not self.attrs.has_key('id'):            final_attrs['id'] = 'id_%s' % name
        t = loader.get_template('autocomplete_widget.html')
        c = Context({'cont': {'attrs' : flatatt(final_attrs), 'name' : name, 'id' : final_attrs['id'], 'url' : self.url, 'options' : plist_from_dict(self.options)}} )
        return t.render(c)
        #return "ciao"def plist_from_dict(d):    """Convert a Python dict into a JavaScript property list.    The order of the items in the returned string is undefined."""    return '{' + ', '.join(['%s: %r' % kv for kv in d.items()]) + '}'# Query helper

# View helperfrom django.http import HttpResponsedef autocomplete_response(text, model_or_qs, fields, max_count=50):    """Return the unordered list that is required by the Ajax.AutoCompleter.    The field value will be the item's id; its __str__ is displayed    along with it, but not stored."""
    qs = Tags.objects.filter(tag__startswith=text)
    if qs.count() > max_count:        result = [(0, _('Too many results, please enter more'))]    else:        result = [(d.id, '%s' % d) for d in qs]    result = '\n'.join([        '<li><span class="informal">%s</span></li>' % ( escape(name))        for id, name in result    ])    return HttpResponse('<ul>' + result + '</ul>')