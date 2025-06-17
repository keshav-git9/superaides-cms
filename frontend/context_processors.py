# frontend/context_processors.py
from backend.models import Html,Navigroups,Navigroupspages,Cms_setting

#global_html_contents

def dynamic_content(request):
    html_data = {item.code: item.contents for item in Html.objects.filter(status=True)}
    #print("DEBUG: html_data ->", html_data)
    return {'html_data': html_data}


def cms_settings_processor(request):
    """Fetch CMS settings dynamically for all templates."""
    cms_settings = Cms_setting.objects.first()  # Get the first entry
    return {'cms_settings': cms_settings}