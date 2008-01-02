"""These are custom tags for creating forms more easily."""

from django import template

register = template.Library()

@register.inclusion_tag('widget/fieldrow.html', takes_context=True)
def fieldrow(context, field, label=''):
    """
    This tag creates a form field.

    Syntax::

        {% fieldrow field [label] %}

    field
        This is a formfields.FormFieldWrapper object.
    label (optional)
        This is the label of the field.  It may be a variable or a quoted
        string.  If it is a quoted string, it may contain spaces and template
        variables but underscores will also be converted to spaces. If not
        given then it will default to field.field_name.

    Example usage::

        {% fieldrow form.myfield %}
        {% fieldrow form.myfield form.myfield.field_name %}
        {% fieldrow form.myfield "foo" %}
        {% fieldrow form.myfield "foo label" %}

    """
    form = context['form']
    #fieldname = field.field_name
    fieldname = field
    if not label:
        label = fieldname
    #help_text = form.manipulator.model._meta.get_field(fieldname).help_text
    help_text = field.help_text
	
    return {
        'fieldname': template.Template(fieldname).render(context), 
        'field': field,
        'label': template.Template(label).render(context).replace('_', ' '),
        'help_text': help_text,
    }

@register.inclusion_tag('widget/selectrow.html', takes_context=True)
def selectrow(context, field, url, lookup_field, addlink='', label=''):
    """
    This tag creates a NongSelect form field.

    Syntax::
    
        {% selectrow field url lookup_field [addlink] [label] %}

    field 
        This is a formfields.FormFieldWrapper object.
    url
        This is the JSON lookup URL of the field.  It may be a variable or
        a quoted string.  If it is a quoted string, it may contain spaces and
        template variables.
    lookup_field
        This is the the field being looked up on model.  It may be a variable
        or a quoted string.  If it is a quoted string, it may contain spaces
        and template variables. This is used in prepopulating the select
        element with the correct value in a change form.
    addlink (optional)
        URL to a view which can add a object of the type type being displayed
        in this select element.
    label (optional)
        This is the label of the field.  It may be a variable or a quoted
        string.  If it is a quoted string, it may contain spaces and template
        variables but underscores will also be converted to spaces. If not
        given then it will default to field.field_name.

    Example usage::

        {% selectrow form.myfield "/url/" "foo" "{{ SITE_ROOT }}url/field/add" %}
        {% selectrow form.myfield "{{ SITE_ROOT }}url/" "foo" "/url/field/add" form.myfield.field_name %}
        {% selectrow form.myfield "/url/" "foo" "/url/field/add" "mylabel" %}
        {% selectrow form.myfield "/url/" "foo" "/url/field/add" "my label" %}
    """
    # 
    value = ''
    selection = ''

    form = context['form']
    fieldname = field #.field_name
    if not label:
        label = fieldname
    #help_text = form.manipulator.model._meta.get_field(fieldname).help_text
    help_text = fieldname.help_text
    # set the value and selection if we are changing the object or if it has
    # been already fill in
    str_data = str(field.data)
    #for val, display_name in field.formfield.choices:
    for val, display_name in field.choices:
        if str(val) == str_data:
            value = val
            selection = display_name

    return {
        'fieldname': fieldname, 
        'lookup_field': template.Template(lookup_field).render(context), 
        'addlink': template.Template(addlink).render(context), 
        'field': field,
        'label': template.Template(label).render(context).replace('_', ' '),
        'data_url': template.Template(url).render(context),
        'help_text': help_text,
        'value': value,
        'selection': selection,
    }

# vim: ai ts=4 sts=4 et sw=4
