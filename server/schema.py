from graphene import Mutation, List, ObjectType, String, Schema, Field, Boolean
import recommender
from spotify import get_user_playlist, get_user_playlists
from state import set_selected_playlist, get_selected_playlist


class Playlist(ObjectType):
    id = String()
    name = String()
    url = String()


class Track(ObjectType):
    coverImageUrl = String()
    name = String()
    artists = List(String)


class Query(ObjectType):

    playlists = List(Playlist)
    currentRecommendation = Field(Track)
    selectedPlaylist = Field(Playlist)

    def resolve_playlists(self, info):
        access_token = info.context.headers['Authorization']
        user_playlists = get_user_playlists(access_token)
        return [Playlist(**user_playlist) for user_playlist in user_playlists]

    def resolve_selectedPlaylist(self, info):
        playlist = get_selected_playlist()
        return playlist and Playlist(**playlist)

    def resolve_currentRecommendation(self, info):
        track = recommender.get_current_recommendation()
        return track and Track(**track)


class SelectPlaylist(Mutation):
    class Arguments:
        playlistId = String()

    recommendedTrack = Field(Track)

    def mutate(self, info, playlistId):
        access_token = info.context.headers['Authorization']
        playlist, tracks = get_user_playlist(access_token, playlistId)
        recommender.initialize_recommender(tracks)
        set_selected_playlist(playlist)
        next_track = recommender.get_next_recommendation()
        if not next_track:
            return None

        return SelectPlaylist(recommendedTrack=Track(**next_track))


class EvaluateRecommendation(Mutation):
    class Arguments:
        addToPlaylist = Boolean()

    recommendedTrack = Field(Track)

    def mutate(self, info, addToPlaylist):
        next_track = recommender.get_next_recommendation()
        if not next_track:
            return None

        return EvaluateRecommendation(recommendedTrack=Track(**next_track))


class Mutations(ObjectType):
    selectPlaylist = SelectPlaylist.Field()
    evaluateRecommendation = EvaluateRecommendation.Field()


schema = Schema(query=Query, mutation=Mutations)
