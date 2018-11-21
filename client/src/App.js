import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';
import { getSpotifyAuthorization } from './auth';

const client = new ApolloClient({
  uri: 'https://fakerql.com/graphql',
});

export default class App extends React.Component {
  state = {
    result: null,
  };

  async componentWillMount() {
    const result = await getSpotifyAuthorization();
    this.setState({ result });
  }

  render() {
    return (
      <ApolloProvider client={client}>
        <View style={styles.container}>
          <Text>{JSON.stringify(this.state.result)}</Text>
        </View>
      </ApolloProvider>
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
