const microsoftAuthService = require('../services/microsoftAuthService');

exports.login = (req, res) => {
    const authUrl = microsoftAuthService.getAuthUrl();
    res.redirect(authUrl);
};

exports.callback = async (req, res) => {
    try {
        const token = await microsoftAuthService.getToken(req.query.code);
        req.session.accessToken = token.access_token;
        res.redirect('/mail.html');
    } catch (err) {
        res.status(500).send('Erreur d\'authentification');
    }
};

exports.logout = (req, res) => {
    req.session.destroy();
    res.redirect('/');
};
