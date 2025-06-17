# frontend/templatetags/custom_filters.py
from django import template
from backend.models import Html,Navigroups, Navigroupspages,Pages,Cms_setting
import re

register = template.Library()

@register.filter
def replace_code(value):
    """Replace [[code]] with corresponding content from Html model"""   
    if not value:
        return value  # Return unchanged if no content
    def replace_match(match):
        code_value = match.group(1)  # Extract code inside [[code]]
        html_obj = Html.objects.filter(code=code_value).first()
        #print("DEBUG: html_data ->", html_obj)
        return html_obj.contents if html_obj else f"[[{code_value}]] (Not Found)"

    return re.sub(r'\[\[(.*?)\]\]', replace_match, value)  # Replace all [[code]] occurrences




@register.simple_tag
def get_menu_tree(menu_code):
    """Fetch the menu tree dynamically"""
    try:
        #group = Navigroups.objects.get(code=menu_code)  # Get the navigation group
        group = Navigroups.objects.filter(code=menu_code, status=True).first()
        menu_items = Navigroupspages.objects.filter(navi_code=group, status=True, parent__isnull=True).prefetch_related('children')  # Get top-level items
    except Navigroups.DoesNotExist:
        return ""

    return menu_items  # Return for template use


def cms_settings_processor(request):
    """Fetch CMS settings dynamically for all templates."""
    cms_settings = Cms_setting.objects.first()  # Get the first entry
    return {'cms_settings': cms_settings}