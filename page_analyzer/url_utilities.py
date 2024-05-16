import validators
from urllib.parse import urlparse


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
