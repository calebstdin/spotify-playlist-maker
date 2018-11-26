from spotipy import Spotify


def playlist(spotify_playlist_data):
    return {
        'id': spotify_playlist_data['id'],
        'name': spotify_playlist_data['name'],
        'url': spotify_playlist_data['external_urls']['spotify']
    }


def track(spotify_track_data):
    return {
        "coverImageUrl": spotify_track_data['album']['images'][0]['url'],
        "name": spotify_track_data['name'],
        "artists":
        [artist['name'] for artist in spotify_track_data['artists']]
    }


def get_user_playlist(access_token, playlist_id):
    sp = Spotify(auth=access_token)
    spotify_playlist = sp.user_playlist(
        user=sp.current_user()['id'], playlist_id=playlist_id)

    tracks = [
        track(spotify_track['track'])
        for spotify_track in spotify_playlist['tracks']['items']
    ]
    return playlist(spotify_playlist), tracks


def get_user_playlists(access_token):
    sp = Spotify(auth=access_token)
    user_playlists = sp.current_user_playlists()['items']
    return [playlist(spotify_playlist) for spotify_playlist in user_playlists]
