import json
import numpy as np
from recommender import BaselineRecommender, NaiveClassification

with open('data/data.json') as data_file:
    data = json.load(data_file)

playlist = data['playlists'][3]
playlist_tracks = playlist['tracks']

hidden_tracks = np.random.choice(
    playlist_tracks, int(round(len(playlist_tracks) / 3)), replace=False)
hidden_track_ids = [track['id'] for track in hidden_tracks]

recommendation_pool = [
    track for track in data['saved_tracks']
    if track['id'] not in playlist_tracks
]

recommender = BaselineRecommender(playlist_tracks, recommendation_pool)

recommendation_count = 0
while (hidden_track_ids):
    recommendation_count += 1
    recommended_track_id = recommender.current()['id']
    if recommended_track_id in hidden_track_ids:
        hidden_track_ids.remove(recommended_track_id)
        recommender.like()
    else:
        recommender.dislike()

print(recommendation_count)
