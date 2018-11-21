import * as React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

class SelectPlaylist extends React.Component {
  render() {
    const { data } = this.props;

    let result;

    if (!data || !data.playlists) {
      result = 'Failed';
    } else {
      result = data.playlists[0].name;
    }

    return (
      <View style={styles.container}>
        <Text>{result}</Text>
      </View>
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
`)(SelectPlaylist);
