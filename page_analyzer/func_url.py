import validators
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def validate(url):
    error = None
    if not url:
        error = 'URL обязателен'
    elif len(url) > 255:
        error = ('URL превышает 255 символов')
    elif not validators.url(url):
        error = ('Некорректный URL')
    return error


def normalizer(url):
    data = urlparse(url)
    return f'{data.scheme}://{data.netloc}'


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.text if soup.title else ''
    h1 = soup.h1.text if soup.h1 else ''
    descr_tag = soup.find('meta', attrs={'name': 'description'})
    description = descr_tag.get('content') if descr_tag else ''
    return h1, title, description
