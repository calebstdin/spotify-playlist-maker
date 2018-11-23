import * as React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { List, ListItem } from 'native-base';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

class SelectPlaylist extends React.Component {
  static navigationOptions = {
    headerTitle: 'Select a playlist',
  };

  selectPlaylist = playlist => {
    const { navigation } = this.props;
    navigation.navigate('BuildPlaylist', {
      playlistId: playlist.id,
      playlistName: playlist.name,
    });
  };

  render() {
    const { data } = this.props;

    if (!data || !data.playlists) {
      return <View />;
    }

    return (
      <View>
        <List>
          {data.playlists.map(playlist => (
            <ListItem key={playlist.id} onPress={() => this.selectPlaylist(playlist)}>
              <Text>{playlist.name}</Text>
            </ListItem>
          ))}
        </List>
      </View>
    );
  }
}

export default graphql(gql`
  {
    playlists {
      id
      name
    }
  }
`)(SelectPlaylist);
