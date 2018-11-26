from spotipy import Spotify


def get_user_playlist_tracks(access_token, playlist_id):
    sp = Spotify(auth=access_token)
    playlist_tracks = sp.user_playlist_tracks(
        user=sp.current_user()['id'],
        playlist_id=playlist_id,
        fields="next, items(track(name,artists(name),album(images)))")

    tracks = []
    for playlist_item in playlist_tracks['items']:
        spotify_track = playlist_item['track']
        tracks.append({
            "coverImageUrl":
            spotify_track['album']['images'][0]['url'],
            "name":
            spotify_track['name'],
            "artists": [artist['name'] for artist in spotify_track['artists']]
        })
    return tracks
