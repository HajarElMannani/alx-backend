from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Dict
import pytz
from datetime import datetime


class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = "UTC"

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

@babel.localeselector
def get_locale() -> str:
    '''get language for the web page'''
    lan = request.args.get('locale')
    if lan in app.config['LANGUAGES']:
        return lan
    if g.get('user'):
        local_user = g.user.get('locale')
        if local_user in app.config['LANGUAGES']:
            return local_user
    return request.accept_languages.best_match(app.config['LANGUAGES'])

def get_user() -> Dict:
    ''' function that returns a user dictionary or None if the ID
     cannot be found or if login_as was not passed'''
    user_id = request.args.get('login_as')
    if user_id:
        try:
            return users.get(int(user_id))
        except ValueError:
            return None
    return None

@babel.timezoneselector
def get_timezone() -> str:
    '''return a URL-provided or user time zone'''
    tzone = request.args.get('timezone')
    if tzone:
        try:
            return str(pytz.timezone(tzone))
        except pytz.UnknownTimeZoneError:
            pass
    if g.get('user') and 'timezone' in g.user:
        try:
            return str(pytz.timezone(g.user['timezone']))
        except pytz.UnknownTimeZoneError:
            pass
    return 'UTC'

@app.before_request
def before_request() -> None:
    '''use get_user to find a user if any'''
    g.user = get_user()

@app.route('/')
def get_index() -> str:
    '''render template'''
    timezone_name = get_timezone()
    tzone = pytz.timezone(timezone_name)
    time_now = datetime.now(tzone)
    current_time = time_now.strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
