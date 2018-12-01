from graphene import Mutation, List, ObjectType, String, Schema, Field, Boolean
import recommender
from spotify import get_user_playlist, get_user_playlists, get_user_tracks
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
        return track and Track(**track['displayInfo'])


class SelectPlaylist(Mutation):
    class Arguments:
        playlistId = String()

    selectedPlaylist = Field(Playlist)
    recommendedTrack = Field(Track)

    def mutate(self, info, playlistId):
        access_token = info.context.headers['Authorization']
        playlist, playlist_tracks = get_user_playlist(access_token, playlistId)
        user_saved_tracks = get_user_tracks(access_token)

        playlist_tracks_ids = [track['id'] for track in playlist_tracks]
        song_recommendations_pool = [
            track for track in user_saved_tracks
            if track['id'] not in playlist_tracks_ids
        ]
        recommender.initialize_recommender(playlist_tracks,
                                           song_recommendations_pool)

        set_selected_playlist(playlist)
        next_track = recommender.get_next_recommendation()

        return next_track and SelectPlaylist(
            selectedPlaylist=Playlist(**playlist),
            recommendedTrack=Track(**next_track['displayInfo']))


class LikeRecommendation(Mutation):
    class Arguments:
        playlistId = String()

    nextRecommendation = Field(Track)

    def mutate(self, info):
        recommender.like_current_recommendation()
        next_recommendation = recommender.get_next_recommendation()
        return LikeRecommendation(
            nextRecommendation=next_recommendation and Track(
                **next_recommendation['displayInfo']))


class DislikeRecommendation(Mutation):
    class Arguments:
        playlistId = String()

    nextRecommendation = Field(Track)

    def mutate(self, info):
        recommender.dislike_current_recommendation()
        next_recommendation = recommender.get_next_recommendation()
        return DislikeRecommendation(
            nextRecommendation=next_recommendation and Track(
                **next_recommendation['displayInfo']))


class Mutations(ObjectType):
    selectPlaylist = SelectPlaylist.Field()
    likeRecommendation = LikeRecommendation.Field()
    dislikeRecommendation = DislikeRecommendation.Field()


schema = Schema(query=Query, mutation=Mutations)
