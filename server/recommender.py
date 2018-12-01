class Recommender:
    def __init__(self, training_set, recommendations_pool):

        self.training_set = training_set
        self.recommendations_pool = recommendations_pool
        self.recommendations = -1

    def current(self):
        return self.recommendations_pool[self.recommendations]

    def next(self):
        self.recommendations += 1
        if self.recommendations < len(self.recommendations_pool):
            return self.recommendations_pool[self.recommendations]
        else:
            return None

    def like(self):
        self.next()

    def dislike(self):
        self.next()


def initialize_recommender(training_set, recommendations_pool):
    global recommender
    recommender = Recommender(training_set, recommendations_pool)


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
