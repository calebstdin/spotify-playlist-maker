import * as React from 'react';
import { Image } from 'react-native';
import { Text, DeckSwiper, Card, CardItem, Left, Body, View, H3 } from 'native-base';
import gql from 'graphql-tag';
import { graphql, compose } from 'react-apollo';
import { LoadingScreen } from '../components';

class BuildPlaylist extends React.Component {
  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('playlistName', 'Playlist'),
    };
  };

  like = () => {
    console.log('liked!');
  };

  dislike = () => {
    console.log('disliked!');
  };

  render() {
    const { data } = this.props;

    if (!data || !data.selectedPlaylist || !data.currentRecommendation) {
      return <LoadingScreen />;
    }

    const { selectedPlaylist, currentRecommendation } = data;

    console.log(currentRecommendation.coverImageUrl);

    return (
      <View style={{ padding: 5 }}>
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
