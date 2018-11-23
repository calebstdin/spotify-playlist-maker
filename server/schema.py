from graphene import Mutation, List, ObjectType, String, Schema, Field, Boolean
from spotipy import Spotify
from recommender import Recommender


def getNextRecommendation(addPreviousRecommendationToPlaylist=None):
    global recommender
    next_track = recommender.next()
    if not (next_track):
        return None
    return SelectPlaylist(
        recommendedTrack=RecommendedTrack(
            coverImageUrl=next_track['track']['album']['images'][0]['url'],
            name=next_track['track']['name'],
            artists=[
                artist['name'] for artist in next_track['track']['artists']
            ]))


class Playlist(ObjectType):
    id = String()
    name = String()


class RecommendedTrack(ObjectType):
    coverImageUrl = String()
    name = String()
    artists = List(String)


class Query(ObjectType):

    playlists = List(Playlist)

    def resolve_playlists(self, info):
        accessToken = info.context.headers['Authorization']
        sp = Spotify(auth=accessToken)
        user_playlists = sp.current_user_playlists()['items']
        return [
            Playlist(id=playlist['id'], name=playlist['name'])
            for playlist in user_playlists
        ]


class SelectPlaylist(Mutation):
    class Arguments:
        playlistId = String()

    recommendedTrack = Field(RecommendedTrack)

    def mutate(self, info, playlistId):
        accessToken = info.context.headers['Authorization']
        sp = Spotify(auth=accessToken)
        playlist_tracks = sp.user_playlist_tracks(
            user=sp.current_user()['id'],
            playlist_id=playlistId,
            fields="next, items(track(name,artists(name),album(images)))")
        global recommender
        recommender = Recommender(playlist_tracks['items'])
        return getNextRecommendation()


class EvaluateRecommendation(Mutation):
    class Arguments:
        addToPlaylist = Boolean()

    recommendedTrack = Field(RecommendedTrack)

    def mutate(self, info, addToPlaylist):
        global recommender
        next_track = recommender.next()
        if not (next_track):
            return None

        return getNextRecommendation(addToPlaylist)


class Mutations(ObjectType):
    selectPlaylist = SelectPlaylist.Field()
    evaluateRecommendation = EvaluateRecommendation.Field()


schema = Schema(query=Query, mutation=Mutations)
