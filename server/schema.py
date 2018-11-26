from graphene import Mutation, List, ObjectType, String, Schema, Field, Boolean
from spotipy import Spotify
from recommender import initialize_recommender, get_next_recommendation
from spotify import get_user_playlist_tracks


class Playlist(ObjectType):
    id = String()
    name = String()


class Track(ObjectType):
    coverImageUrl = String()
    name = String()
    artists = List(String)


class Query(ObjectType):

    playlists = List(Playlist)
    currentRecommendation = Field(Track)

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

    recommendedTrack = Field(Track)

    def mutate(self, info, playlistId):
        accessToken = info.context.headers['Authorization']
        playlist_tracks = get_user_playlist_tracks(accessToken, playlistId)
        initialize_recommender(playlist_tracks)
        next_track = get_next_recommendation()
        if not next_track:
            return None

        return SelectPlaylist(recommendedTrack=Track(**next_track))


class EvaluateRecommendation(Mutation):
    class Arguments:
        addToPlaylist = Boolean()

    recommendedTrack = Field(Track)

    def mutate(self, info, addToPlaylist):
        next_track = get_next_recommendation()
        if not next_track:
            return None

        return EvaluateRecommendation(recommendedTrack=Track(**next_track))


class Mutations(ObjectType):
    selectPlaylist = SelectPlaylist.Field()
    evaluateRecommendation = EvaluateRecommendation.Field()


schema = Schema(query=Query, mutation=Mutations)
