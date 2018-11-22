import * as React from 'react';
import { StyleSheet, Text, View, Picker } from 'react-native';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

class PlaylistBuilder extends React.Component {
  state = {
    selectedPlaylist: undefined,
  };

  selectPlaylist = playlistId => {
    this.setState({ selectedPlaylist: playlistId });
  };

  render() {
    const { selectedPlaylist } = this.state;
    const { data } = this.props;

    if (!data || !data.playlists) {
      return <View />;
    }

    return (
      <Picker
        selectedValue={selectedPlaylist}
        mode="dialog"
        onValueChange={this.selectPlaylist}
        prompt="Select a playlist">
        {data.playlists.map(playlist => (
          <Picker.Item key={playlist.id} label={playlist.name} value={playlist.id} />
        ))}
      </Picker>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export default graphql(gql`
  {
    playlists {
      id
      name
    }
  }
`)(PlaylistBuilder);
