#----------------------- widgets.py------------------------
# -*- coding: utf-8 -*-
# 
# In order to use this widget you need:
# 1. download YUI library and put it in 
#    your MEDIA folder (http://developer.yahoo.com/yui/)
# 2. Include necessary js and css imports at your page
#    Check for necessary imports at 'YUI autocomplete' page
#    My imports are:
#     <!-- yui -->
#     <link rel="stylesheet" type="text/css" href="{{ MEDIA_URL }}yui/tabview/assets/skins/sam/tabview.css" />
#     <script type="text/javascript" src="{{ MEDIA_URL }}yui/utilities/utilities.js"></script>
#     <script type="text/javascript" src="{{ MEDIA_URL }}yui/autocomplete/autocomplete-min.js"></script>
#     <script type="text/javascript" src="{{ MEDIA_URL }}yui/datasource/datasource-beta-min.js"></script>
#    <!-- /yui-->
# 3. Assign a widget to field (with schema and lookup_url parameters)
# 4. Define view to do a data lookup for ajax queries
#
from django import newforms as forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
        
AC_SNIPPET = """
<div id = "autocomplete" class="id_tags_container">
    <input id="%s" name="%s" value="%s" />
    <div id="%s_container" class="yui-skin-sam"></div>
  

    <script type="text/javascript">
        // An XHR DataSource
        var acServer_%s = "%s";
        var acSchema_%s = %s;
        var acDataSource_%s = new YAHOO.widget.DS_XHR(acServer_%s, acSchema_%s);
        acDataSource_%s.queryMatchContains = true;
        
        
        acAutoComp_%s = new YAHOO.widget.AutoComplete("%s","%s_container", acDataSource_%s);
        acAutoComp_%s.useIFrame = true;
		 
		
        acAutoComp_%s.doBeforeExpandContainer = function(oTextbox, oContainer, sQuery, aResults) { 
  	        var pos = YAHOO.util.Dom.getXY(oTextbox); 
	        pos[1] += YAHOO.util.Dom.get(oTextbox).offsetHeight + 2; 
	        YAHOO.util.Dom.setXY(oContainer,pos); 
	        return true; 
        }; 
        
        //  http://developer.yahoo.com/yui/autocomplete/#using
        
        
        // Container will expand and collapse vertically 
        acAutoComp_%s.animVert = true
        
        // Container will expand and collapse horizontally 
        acAutoComp_%s.animHoriz = false; 
        
        // Container animation will take 2 seconds to complete
        acAutoComp_%s.animSpeed = 0.3; 
        
        // Semi-colons may delimited queries...
        acAutoComp_%s.delimChar = [" "]; 
        
        // Display up to 20 results in the container
        acAutoComp_%s.maxResultsDisplayed = 20;
        
        // Require user to type at least 3 characters before triggering a query
        //acAutoComp.minQueryLength = 3;
        
        
        // Every key input event will trigger an immediate query...
        acAutoComp_%s.queryDelay = 0;
        
        // Do not automatically highlight the first result item in the container
        acAutoComp_%s.autoHighlight = false;
        
        // Use a custom class for LI elements
        //acAutoComp.highlightClassName = "myCustomHighlightClass";
        
        // Use a custom class for mouseover events
        //acAutoComp.prehighlightClassName = "myCustomPrehighlightClass";
        acAutoComp_%s.useShadow = true; 
        
        acAutoComp_%s.typeAhead = true; 
        acAutoComp_%s.formatResult = function(oResultItem, sQuery) {
           var sResult = oResultItem[0];
           var sOcc = oResultItem[1]
           if(sResult) {
             var aMarkup = ["<div>",
             "<span style='text-align:left'>",
             sResult,
             "</span>",
             "<span style='font-size:x-small;color:green;'>",
             "(",
             sOcc,
             " results)",
             "</span>",
             "</div>"];
             return (aMarkup.join("")); 
        }
         else {
          return "";
        }
    
    
      
    
    
};
        
 
        %s
        %s
    </script>
</div>
"""

def_format_result = 'acAutoComp_%s.formatResult = %s;'
def_item_select_handler = 'acAutoComp_%s.itemSelectEvent.subscribe(%s);'

class AutoCompleteWidget(forms.widgets.TextInput):
    """ widget autocomplete dla zwyklych pol tekstowych (nie FK)
    """    
    
    def render(self, name, value, attrs=None):
        html_id = attrs.get('id', name)
        # url for YUI XHR Datasource
        lookup_url = self.lookup_url
        # YUI schema
        schema = self.schema
        # optional name of javascript function that handles item select event (YUI)
        item_select_handler_fname = getattr(self, 'item_select_handler_fname', '')
        # optional name of javascript function that formats results (YUI)
        format_result_fname = getattr(self, 'format_result_fname', '')

        fr = '' # format result
        sh = '' # select handler
        if format_result_fname:
            fr = def_format_result % (html_id, format_result_fname)
        if item_select_handler_fname:
            sh = def_item_select_handler % (html_id,
                                            item_select_handler_fname)

        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '': final_attrs['value'] = force_unicode(value) # Only add the 'value' attribute if a value is non-empty.
       # final_attrs['class'] = 'autocomplete_widget'

        return mark_safe(AC_SNIPPET % (html_id, name, value, html_id, html_id,
                             lookup_url,html_id, schema, html_id, html_id,
                             html_id, html_id, html_id, html_id, html_id,
                             html_id,html_id, html_id, 
                             html_id, html_id, html_id,
                             html_id, html_id, html_id,
                             html_id, html_id, html_id,
                             html_id,
                             fr, sh))
