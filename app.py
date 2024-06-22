"""Flask app of song-guesser"""

import secrets
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

SCOPE = 'user-modify-playback-state'

@app.route('/')
def index():
    """Handle the homepage and OAuth redirect sites"""
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=SCOPE,
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    # spotify = spotipy.Spotify(auth_manager=auth_manager)
    # return f'<h2>Hi {spotify.me()["display_name"]}, ' \
    #        f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
    #        f'<a href="/playlists">my playlists</a> | ' \
    #        f'<a href="/currently_playing">currently playing</a> | ' \
    #     f'<a href="/current_user">me</a>' \
    return render_template('index.html')

@app.route('/play', methods=['GET'])
def play_song():
    """Play a track passed in through a parameter"""
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    uri = request.args.get('track')
    if not uri:
        return "Track uri is required", 400

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    try:
        spotify.start_playback(uris=[uri])
        return f"Playing {uri}"
    except spotipy.exceptions.SpotifyException as e:
        return f"Spotify API error: {e.http_status} - {e.reason}"

@app.route('/sign_out')
def sign_out():
    """Sign out of the Spotify Account"""
    session.pop("token_info", None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
