#!/usr/bin/env python3
'''A Flask app'''
from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    '''Flask babbel config'''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    '''get language from the user accept'''
    lan = request.args.get('locale')
    if lan in app.config['LANGUAGES']:
        return lan
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def get_index() -> str:
    '''render template'''
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
