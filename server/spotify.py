from spotipy import Spotify


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


def playlist(spotify_playlist_data):
    return {
        'id': spotify_playlist_data['id'],
        'name': spotify_playlist_data['name'],
        'url': spotify_playlist_data['external_urls']['spotify']
    }


def tracks(spotify_track_data, access_token):
    sp = Spotify(auth=access_token)
    track_id_chunks = list(
        chunks([track['track']['id'] for track in spotify_track_data], 100))

    tracks = []
    for track_id_chunk in track_id_chunks:
        audio_features_chunk = sp.audio_features(track_id_chunk)
        for idx, audio_features in enumerate(audio_features_chunk):
            if not audio_features:
                continue
            track = spotify_track_data[idx]['track']
            tracks.append({
                'features': {
                    "danceability": audio_features['danceability'],
                    "energy": audio_features['energy'],
                    "key": audio_features['key'],
                    "loudness": audio_features['loudness'],
                    "mode": audio_features['mode'],
                    "speechiness": audio_features['speechiness'],
                    "acousticness": audio_features['acousticness'],
                    "instrumentalness": audio_features['instrumentalness'],
                    "liveness": audio_features['liveness'],
                    "valence": audio_features['valence'],
                    "tempo": audio_features['tempo'],
                },
                'id': track['id'],
                'displayInfo': {
                    "coverImageUrl": track['album']['images'][0]['url'],
                    "name": track['name'],
                    "artists": [artist['name'] for artist in track['artists']]
                }
            })
    return tracks


def get_user_playlist(access_token, playlist_id):
    sp = Spotify(auth=access_token)
    spotify_playlist = sp.user_playlist(
        user=sp.current_user()['id'], playlist_id=playlist_id)

    return playlist(spotify_playlist), tracks(
        spotify_playlist['tracks']['items'], access_token)


def get_user_playlists(access_token):
    sp = Spotify(auth=access_token)
    user_playlists = sp.current_user_playlists()['items']
    return [playlist(spotify_playlist) for spotify_playlist in user_playlists]


def get_user_tracks(access_token):
    sp = Spotify(auth=access_token)
    spotify_tracks_chunk = sp.current_user_saved_tracks()
    spotify_tracks = spotify_tracks_chunk['items']
    while (spotify_tracks_chunk['next']):
        spotify_tracks_chunk = sp.next(spotify_tracks_chunk)
        spotify_tracks += spotify_tracks_chunk['items']

    return tracks(spotify_tracks, access_token)


if __name__ == "__main__":
    get_user_tracks(
        'BQCcj9i65BMh3QUyFAAWJbfknqaHYCSY96gW18TgdBjZzfwjumbzlOmgyKc0cdjTrkdM84E1h4rfFt8OAoIg3-T8LC6TKv0reu5phONexWslptAO53CFesY8IMGl24ahp7ZNEP3kfIYnqut0rcvjT-PHLdd2p6HFTxQltB-LcmBrvgt0zWW1AzNGHdbqGzUv34lG8TBPWjwEoA'
    )
