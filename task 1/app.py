from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

app = Flask(__name__)   
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
MAILTO_PATTERN = re.compile(r'^mailto:')


def validate_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def ensure_scheme(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url


def extract_emails(html, soup):
    emails = set(EMAIL_PATTERN.findall(soup.get_text()))

    for link in soup.find_all('a', href=MAILTO_PATTERN):
        email = link['href'].replace('mailto:', '').split('?')[0].strip()
        if '@' in email:
            emails.add(email)

    return sorted(emails)


def scrape_emails(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return extract_emails(response.text, soup)
    except Exception as e:
        return {'error': str(e)}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')

        if not url:
            return render_template('index.html', error="Enter URL")

        url = ensure_scheme(url)

        if not validate_url(url):
            return render_template('index.html', error="Invalid URL")

        result = scrape_emails(url)

        if isinstance(result, dict):
            return render_template('index.html', error=result['error'])

        return render_template('index.html', emails=result, url=url)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)