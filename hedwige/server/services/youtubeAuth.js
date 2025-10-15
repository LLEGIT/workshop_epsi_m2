const querystring = require('querystring');
const axios = require('axios');

const clientId = process.env.YOUTUBE_CLIENT_ID;
const clientSecret = process.env.YOUTUBE_CLIENT_SECRET;
const redirectUri = process.env.YOUTUBE_REDIRECT_URI;

const authEndpoint = 'https://accounts.google.com/o/oauth2/v2/auth';
const tokenEndpoint = 'https://oauth2.googleapis.com/token';

exports.getAuthUrl = () => {
    const params = querystring.stringify({
        client_id: clientId,
        redirect_uri: redirectUri,
        response_type: 'code',
        scope: 'https://www.googleapis.com/auth/youtube.readonly',
        access_type: 'offline',
        prompt: 'consent'
    });
    return `${authEndpoint}?${params}`;
};

exports.getToken = async (code) => {
    const response = await axios.post(tokenEndpoint, querystring.stringify({
        code,
        client_id: clientId,
        client_secret: clientSecret,
        redirect_uri: redirectUri,
        grant_type: 'authorization_code'
    }), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });

    return response.data;
};
