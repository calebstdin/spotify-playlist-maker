import * as React from 'react';
import { Image, Linking } from 'react-native';
import { Text, DeckSwiper, Card, CardItem, Left, Body, View, H3, Button } from 'native-base';
import gql from 'graphql-tag';
import { graphql, compose } from 'react-apollo';
import { LoadingScreen } from '../components';

class BuildPlaylist extends React.Component {
  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('playlistName', 'Playlist'),
    };
  };

  openPlaylist = playlistUrl => {
    Linking.openURL(playlistUrl);
  };

  like = () => {
    const { likeRecommendation } = this.props;
    likeRecommendation();
  };

  dislike = () => {
    const { dislikeRecommendation } = this.props;
    dislikeRecommendation();
  };

  render() {
    const { data } = this.props;

    if (!data || !data.selectedPlaylist || !data.currentRecommendation) {
      return <LoadingScreen />;
    }

    const { selectedPlaylist, currentRecommendation } = data;

    return (
      <View style={{ padding: 5, flex: 1, flexDirection: 'column' }}>
        <DeckSwiper
          onSwipeRight={this.like}
          onSwipeLeft={this.dislike}
          dataSource={[currentRecommendation]}
          renderItem={item => (
            <Card style={{ elevation: 3 }}>
              <CardItem cardBody>
                <Image
                  style={{ height: 300, width: 300, flex: 1 }}
                  source={{ uri: currentRecommendation.coverImageUrl }}
                />
              </CardItem>
              <CardItem>
                <Left>
                  <Body>
                    <H3>{item.name}</H3>
                    <Text note>{item.artists[0]}</Text>
                  </Body>
                </Left>
              </CardItem>
            </Card>
          )}
        />
        <View
          style={{
            flexDirection: 'row',
            flex: 1,
            position: 'absolute',
            bottom: 70,
            left: 0,
            right: 0,
            justifyContent: 'center',
            padding: 15,
          }}>
          <Button iconLeft onPress={() => this.openPlaylist(selectedPlaylist.url)}>
            <Text>Open playlist in Spotify</Text>
          </Button>
        </View>
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
    { name: 'likeRecommendation', options: { refetchQueries: ['CurrentState'] } }
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
    { name: 'dislikeRecommendation', options: { refetchQueries: ['CurrentState'] } }
  )
)(BuildPlaylist);
