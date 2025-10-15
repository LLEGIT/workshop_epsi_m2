const axios = require('axios');
const querystring = require('querystring');

const clientId = process.env.MICROSOFT_CLIENT_ID;
const clientSecret = process.env.MICROSOFT_CLIENT_SECRET;
const redirectUri = process.env.MICROSOFT_REDIRECT_URI;

// Le endpoint v2.0 gère à la fois les comptes personnels et scolaires/universitaires
const authEndpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize';
const tokenEndpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token';

exports.getAuthUrl = () => {
    const params = querystring.stringify({
        client_id: clientId,
        response_type: 'code',
        redirect_uri: redirectUri,
        response_mode: 'query',
        scope: 'openid offline_access Mail.ReadWrite Mail.Send',
        prompt: 'select_account'
    });
    return `${authEndpoint}?${params}`;
};

exports.getToken = async (code) => {
    try {
        const response = await axios.post(tokenEndpoint,
            querystring.stringify({
                client_id: clientId,
                scope: 'openid offline_access Mail.ReadWrite Mail.Send',
                code,
                redirect_uri: redirectUri,
                grant_type: 'authorization_code',
                client_secret: clientSecret
            }),
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        );
        return response.data;
    } catch (err) {
        console.error('Erreur token Microsoft:', err.response?.data || err.message);
        throw new Error('Impossible d’obtenir le token OAuth');
    }
};
