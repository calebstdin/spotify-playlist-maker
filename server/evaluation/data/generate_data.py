import json
from spotify import get_user_playlist, get_user_tracks


def generate_data(access_token, playlist_ids):
    playlists = []
    for playlist_id in playlist_ids:
        playlist, playlist_tracks = get_user_playlist(access_token,
                                                      playlist_id)
        playlists.append({'name': playlist['name'], 'tracks': playlist_tracks})
    tracks = get_user_tracks(access_token)
    data = {'playlists': playlists, 'saved_tracks': tracks}
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
