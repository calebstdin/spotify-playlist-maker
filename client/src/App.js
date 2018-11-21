import React from 'react';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from 'react-apollo';
import { getSpotifyAuthorization } from './auth';
import SelectPlaylist from './SelectPlaylsit';

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
        <SelectPlaylist />
      </ApolloProvider>
    );
  }
}
