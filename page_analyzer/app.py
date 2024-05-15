from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for
                   )
from dotenv import load_dotenv
from .func_url import validate, normalizer, get_data
from .db import URLRepository
import os
import requests


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
repo = URLRepository(DATABASE_URL)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    urls = repo.find_all_urls()

    return render_template(
        'urls.html',
        urls=urls
    )


@app.route('/urls', methods=['POST'])
def post_urls():
    url = request.form.get('url')
    error = validate(url)

    if error:
        flash(error, 'alert-danger')
        return render_template('index.html', url=url), 422

    url_name = normalizer(url)
    url_check = repo.find_url_by_name(url_name)

    if url_check:
        flash('Страница уже существует', 'alert-info')
        return redirect(url_for('urls_id', id=url_check.id))

    url_id = repo.create_url(url_name)
    flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('urls_id', id=url_id))


@app.route('/urls/<id>')
def urls_id(id):
    url = repo.find_url_by_id(id)
    url_checks = repo.find_url_check(id)

    return render_template('url_id.html',
                           url=url,
                           url_checks=url_checks
                           )


@app.route('/urls/<id>/checks', methods=['POST'])
def url_check(id):
    url = repo.find_url_by_id(id)

    try:
        page = requests.get(url.name)
    except Exception:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('urls_id', id=id))

    status_code = page.status_code
    h1, title, description = get_data(page.text)
    repo.create_url_check(id, status_code, h1, title, description)

    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('urls_id', id=id))
