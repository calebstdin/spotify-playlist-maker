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

    def yes(self):
        self.next()

    def no(self):
        self.next()


def initialize_recommender(songs_in_playlist):
    global recommender
    recommender = Recommender(songs_in_playlist)


def get_next_recommendation():
    global recommender
    return recommender.next()
