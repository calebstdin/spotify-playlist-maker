import json
import numpy as np
from tabulate import tabulate
from recommender import BaselineRecommender, NaivePUClassifier

with open('data/data.json') as data_file:
    data = json.load(data_file)


def evaluate_recommender_for_playlist(Recommender, playlist_tracks):
    playlist_tracks = list(playlist_tracks)
    hidden_tracks = np.random.choice(
        playlist_tracks, int(round(len(playlist_tracks) / 3)), replace=False)
    hidden_track_ids = [track['id'] for track in hidden_tracks]

    recommendation_pool = [
        track for track in data['saved_tracks']
        if track['id'] not in playlist_tracks
    ]

    recommender = Recommender(playlist_tracks, recommendation_pool)

    recommendation_count = 0
    while (hidden_track_ids):
        recommendation_count += 1
        recommended_track_id = recommender.current()['id']
        if recommended_track_id in hidden_track_ids:
            hidden_track_ids.remove(recommended_track_id)
            recommender.like()
        else:
            recommender.dislike()

    return recommendation_count


def evaluate_recommender(Recommender):
    evaluations = {}
    for playlist in data['playlists']:
        recommendation_counts = []
        for _ in range(20):
            recommendation_count = evaluate_recommender_for_playlist(
                Recommender, playlist['tracks'])
            recommendation_counts.append(recommendation_count)

        evaluations[playlist['name']] = np.mean(recommendation_counts)
    return evaluations


baseline = evaluate_recommender(BaselineRecommender)
pu_classifier = evaluate_recommender(NaivePUClassifier)

results = [[key, baseline[key], pu_classifier[key]] for key in baseline]

results_table = tabulate(
    results, headers=['Playlist', 'Baseline Score', 'PU Classifier Score'])

print(results_table)
