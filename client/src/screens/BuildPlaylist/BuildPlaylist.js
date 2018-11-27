import * as React from 'react';
import { View, Text } from 'native-base';
import gql from 'graphql-tag';
import { graphql, compose } from 'react-apollo';
import { LoadingScreen } from '../components';

class BuildPlaylist extends React.Component {
  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('playlistName', 'Playlist'),
    };
  };

  render() {
    const { data } = this.props;

    if (!data || !data.selectedPlaylist) {
      return <LoadingScreen />;
    }

    const { selectedPlaylist } = data;

    return (
      <View>
        <Text>{selectedPlaylist.url}</Text>
      </View>
    );
  }
}

export default compose(
  graphql(gql`
    query CurrentState {
      selectedPlaylist {
        name
        url
      }
      currentRecommendation {
        name
        artists
        coverImageUrl
      }
    }
  `),
  graphql(
    gql`
      mutation LikeRecommendation {
        likeRecommendation {
          nextRecommendation {
            name
          }
        }
      }
    `,
    { name: 'likeRecommendation' }
  ),
  graphql(
    gql`
      mutation DisikeRecommendation {
        dislikeRecommendation {
          nextRecommendation {
            name
          }
        }
      }
    `,
    { name: 'dislikeRecommendation' }
  )
)(BuildPlaylist);
