import * as React from 'react';
import { View, Text } from 'native-base';

class BuildPlaylist extends React.Component {
  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('playlistName', 'Playlist'),
    };
  };

  render() {
    return (
      <View>
        <Text>foo</Text>
      </View>
    );
  }
}

export default BuildPlaylist;
