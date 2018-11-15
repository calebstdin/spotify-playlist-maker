import { AuthSession } from 'expo';
import { post } from 'axios';

const scopes = ['user-library-read', 'playlist-modify-public'];
const clientId = '85c12f9eeb07445783a0c2ffbdabe9df';

export async function getSpotifyAuthorization() {
  const redirectUrl = AuthSession.getRedirectUrl();
  const result = await AuthSession.startAsync({
    authUrl:
      'https://accounts.spotify.com/authorize' +
      '?response_type=code' +
      `&client_id=${clientId}` +
      `&scope=${encodeURIComponent(scopes)}` +
      `&redirect_uri=${encodeURIComponent(redirectUrl)}`,
  });
  const res = await post('https://accounts.spotify.com/api/token', {
    grant_type: 'authorization_code',
    code: result.params.code,
    redirect_uri: redirectUrl,
  });
  console.log(res);
}
