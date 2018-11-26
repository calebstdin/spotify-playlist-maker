class Recommender:
    def __init__(self, songs_in_playlist):
        self.songs_in_playlist = songs_in_playlist
        self.recommendations = 0

    def current(self):
        return self.songs_in_playlist[self.recommendations]

    def next(self):
        self.recommendations += 1
        if self.recommendations < len(self.songs_in_playlist):
            return self.songs_in_playlist[self.recommendations]
        else:
            return None

    def like(self):
        self.next()

    def dislike(self):
        self.next()


def initialize_recommender(songs_in_playlist):
    global recommender
    recommender = Recommender(songs_in_playlist)


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
