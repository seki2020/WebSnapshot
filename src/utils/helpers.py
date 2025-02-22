def fetch_url(url):
    import requests
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

def parse_html(html_content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def save_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)