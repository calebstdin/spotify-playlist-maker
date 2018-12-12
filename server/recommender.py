from abc import ABC, abstractmethod
import pandas as pd
from sklearn import preprocessing
from sklearn.svm import SVC


class Recommender(ABC):
    def __init__(self, playlist_tracks, recommendations_pool):

        self.playlist_tracks = playlist_tracks
        self.disliked_tracks = []
        self.recommendations_pool = recommendations_pool
        self.current_recommendation = self.next()

    def like(self):
        self.next(True)

    def dislike(self):
        self.next(False)

    def current(self):
        return self.current_recommendation

    def next(self, like_current_recommendation=None):
        if like_current_recommendation:
            self.playlist_tracks.append(self.current_recommendation)
        if like_current_recommendation is False:
            self.disliked_tracks.append(self.current_recommendation)

        if self.recommendations_pool:
            self.current_recommendation = self.next_recommendation(
                like_current_recommendation)
        else:
            self.current_recommendation = None

        return self.current_recommendation

    @abstractmethod
    def next_recommendation():
        pass


class BaselineRecommender(Recommender):
    def next_recommendation(self, like_current_recommendation):
        return self.recommendations_pool.pop()


# All songs in the playlist have target feature = True
# All songs in the recommendation pool have target feature = False
# Train classifier based on that.
class NaivePUClassifier(Recommender):
    def next_recommendation(self, like_current_recommendation):
        X_train = preprocessing.scale(
            pd.DataFrame(
                list([
                    x['features']
                    for x in (self.playlist_tracks + self.disliked_tracks +
                              self.recommendations_pool)
                ])))

        X_predict = preprocessing.scale(
            pd.DataFrame(
                list([x['features'] for x in self.recommendations_pool])))

        y = pd.Series([True] * len(self.playlist_tracks) +
                      [False] * len(self.disliked_tracks) +
                      [False] * len(self.recommendations_pool))

        clf = SVC(gamma='auto', probability=True)
        clf.fit(X_train, y)
        predictions = clf.predict_proba(X_predict)[:, 1]

        recommendation_index = predictions.argmax()
        return self.recommendations_pool.pop(recommendation_index)


def initialize_recommender(playlist_tracks, recommendations_pool):
    global recommender
    recommender = NaivePUClassifier(playlist_tracks, recommendations_pool)


def get_recommendation():
    global recommender
    return recommender.current()


def like_recommendation():
    global recommender
    return recommender.like()


def dislike_recommendation():
    global recommender
    return recommender.dislike()
