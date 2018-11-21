from graphene import Mutation, List, ObjectType, String, Schema
from spotipy import Spotify


class Playlist(ObjectType):

    id = String()
    name = String()


class Query(ObjectType):

    playlists = List(Playlist)

    def resolve_playlists(self, info, **args):
        accessToken = info.context.headers['Authorization']
        sp = Spotify(auth=accessToken)
        user_playlists = sp.current_user_playlists()['items']
        return [
            Playlist(id=playlist['id'], name=playlist['name'])
            for playlist in user_playlists
        ]


class CreatePlaylist(Mutation):
    class Arguments:
        accessToken = String()

    playlistId = String()
    recommendedSong = String()

    def mutate(self, info, accessToken):
        return CreatePlaylist(playlistId='foo', recommendedSong='bar')


class Mutations(ObjectType):
    createPlaylist = CreatePlaylist.Field()


schema = Schema(query=Query, mutation=Mutations)
