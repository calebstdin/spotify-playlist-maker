import { AuthSession } from 'expo';

const scopes = ['user-library-read', 'playlist-modify-public'];
const clientId = '85c12f9eeb07445783a0c2ffbdabe9df';

export async function getSpotifyAuthorization() {
  const redirectUrl = AuthSession.getRedirectUrl();
  const authorizeResult = await AuthSession.startAsync({
    authUrl:
      'https://accounts.spotify.com/authorize' +
      '?response_type=code' +
      `&client_id=${clientId}` +
      `&scope=${encodeURIComponent(scopes)}` +
      `&redirect_uri=${encodeURIComponent(redirectUrl)}`,
  });
  const getTokenResult = await fetch(
    'https://accounts.spotify.com/api/token' +
      `?grant_type=authorization_code` +
      `&code=${authorizeResult.params.code}` +
      `&redirect_uri=${encodeURIComponent(redirectUrl)}` +
      `&client_id=${'85c12f9eeb07445783a0c2ffbdabe9df'}` +
      `&client_secret=${'7aee2872683148fcb04fb3e3b608388c'}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  );
  const { access_token: accessToken } = await getTokenResult.json();
  return accessToken;
}
