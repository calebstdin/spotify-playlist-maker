import * as React from 'react';
import { View, Text } from 'native-base';

class BuildPlaylist extends React.Component {
  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('playlistName', 'Playlist'),
    };
  };

  render() {
    const { navigation } = this.props;
    return (
      <View>
        <Text>{navigation.getParam('playlistId')}</Text>
      </View>
    );
  }
}

export default BuildPlaylist;
