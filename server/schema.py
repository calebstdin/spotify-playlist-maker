from graphene import Mutation, ObjectType, String, Schema
from spotipy import Spotify


class CreatePlaylist(Mutation):
    class Arguments:
        playlistName = String()
        accessToken = String()

    playlistId = String()
    recommendedSong = String()

    def mutate(self, info, playlistName, accessToken):
        sp = Spotify(auth=accessToken)
        track = sp.current_user_saved_tracks()['items'][0]['track']['name']
        return CreatePlaylist(playlistId=playlistName, recommendedSong=track)


class Mutations(ObjectType):
    createPlaylist = CreatePlaylist.Field()


schema = Schema(mutation=Mutations)
