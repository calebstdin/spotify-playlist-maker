class Recommender:
    def __init__(self, songs_in_playlist):
        self.songs_in_playlist = songs_in_playlist
        self.recommendations = 0

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
