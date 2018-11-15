import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { getSpotifyAuthorization } from "./auth";

export default class App extends React.Component {
  state = {
    result: null
  };

  async componentDidMount() {
    const result = await getSpotifyAuthorization();
    this.setState({ result });
  }

  render() {
    return (
      <View style={styles.container}>
        <Text>{JSON.stringify(this.state.result)}</Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center"
  }
});
