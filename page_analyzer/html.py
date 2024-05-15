from bs4 import BeautifulSoup


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.text if soup.title else ''
    h1 = soup.h1.text if soup.h1 else ''
    descr_tag = soup.find('meta', attrs={'name': 'description'})
    description = descr_tag.get('content') if descr_tag else ''
    return h1, title, description
