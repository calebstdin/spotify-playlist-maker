from abc import ABC, abstractmethod


class Recommender(ABC):
    def __init__(self, training_set, recommendations_pool):

        self.training_set = training_set
        self.recommendations_pool = recommendations_pool
        self.current_recommendation = self.next()

    def like(self):
        self.next()

    def dislike(self):
        self.next()

    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def next(self):
        pass


class BaselineRecommender(Recommender):
    def current(self):
        return self.current_recommendation

    def next(self):
        if self.recommendations_pool:
            self.current_recommendation = self.recommendations_pool.pop()
        else:
            self.current_recommendation = None

        return self.current_recommendation


def initialize_recommender(training_set, recommendations_pool):
    global recommender
    recommender = BaselineRecommender(training_set, recommendations_pool)


def get_current_recommendation():
    global recommender
    return recommender.current()


def like_current_recommendation():
    global recommender
    return recommender.like()


def dislike_current_recommendation():
    global recommender
    return recommender.dislike()


def get_next_recommendation():
    global recommender
    return recommender.next()
