import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
from bs4 import BeautifulSoup


def get_google_search_console_data():
    # Authenticate with Google Search Console API using service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        'C:/xampp/htdocs/DJANGO-APP/cms_project/backend/service-account.json', 
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    
    # Create the Search Console API service
    service = build('searchconsole', 'v1', credentials=credentials)

    # Query Google Search Console for search analytics (get search queries)
    response = service.searchanalytics().query(
        siteUrl='http://pss.bharatpayroll.com/',
        body={
            'startDate': '2025-01-01',
            'endDate': '2025-04-01',
            'dimensions': ['query'],  # Get search queries
            'rowLimit': 10
        }
    ).execute()

    keywords = []
    for row in response.get('rows', []):
        keywords.append(row['keys'][0])  # Extract keywords

    return keywords


def get_seo_keywords_from_meta(url):
    # Scrape the website's meta tags for keywords
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    
    if keywords_tag:
        return keywords_tag.get('content', '')
    else:
        return 'No keywords found'
