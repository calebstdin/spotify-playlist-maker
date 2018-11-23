import { createStackNavigator, createAppContainer } from 'react-navigation';
import { SelectPlaylist, BuildPlaylist } from './screens';

const AppNavigator = createStackNavigator({
  Home: SelectPlaylist,
  BuildPlaylist,
});

export default createAppContainer(AppNavigator);
