# sitemaps.py
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime

def manual_sitemap(request):
    # The basic structure of a sitemap file
    print("Sitemap view is being called!")  # Debug line

    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    '''

    # Add URLs to the sitemap manually
    urls = [
        {'url': reverse('home'), 'lastmod': datetime.now()},
        
        # Add more URLs here...
    ]

    # Loop through each URL and add it to the sitemap
    for entry in urls:
        sitemap += f'''
        <url>
            <loc>{request.build_absolute_uri(entry['url'])}</loc>
            <lastmod>{entry['lastmod'].strftime('%Y-%m-%d')}</lastmod>
        </url>
        '''
    
    # Close the urlset tag
    sitemap += '</urlset>'

    # Return the sitemap as an XML response
    return HttpResponse(sitemap, content_type='application/xml')
