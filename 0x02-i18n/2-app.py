from flask import Flask, render_template, request
from flask_babel import Babel

class Config:
    '''Flask babbel config'''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

@app.route('/')
def index():
    '''render template'''
    return render_template('2-index.html')

@babel.localeselector
def get_locale():
    '''get language from the user accept'''
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if __name__ == '__main__':
    app.run(debug=True)
