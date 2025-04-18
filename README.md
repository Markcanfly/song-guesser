# song-guesser

A small web app to use as a tool for music guessing games involving Spotify QR codes.

## Prerequisites

```bash
pip install -r requirements.txt
```

Define the following environment variables:

```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

# Issues

- Playback only starts when music is already being played (no active devices)
- Camera isn't flipped on front facing? not a problem, can't know if it's front facing or not
- Current queue gets completely lost when using QR reader
