const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const { getAuthUrl, getToken } = require('../services/youtubeAuth');
const { getLikedVideos } = require('../services/youtubeService');

router.use(authMiddleware);

// Redirection vers OAuth YouTube si pas connecté
router.get('/login', (req, res) => {
    if (req.session.youtubeToken?.access_token) {
        return res.redirect('/youtube.html');
    }
    const authUrl = getAuthUrl();
    res.redirect(authUrl);
});

// Callback OAuth YouTube
router.get('/callback', async (req, res) => {
    const { code } = req.query;
    try {
        const tokenData = await getToken(code);
        req.session.youtubeToken = tokenData;
        res.redirect('/youtube.html');
    } catch (err) {
        console.error('Erreur token YouTube:', err.message);
        res.status(500).send('Impossible de récupérer le token YouTube');
    }
});

// Récupération des vidéos likées
router.get('/liked', async (req, res) => {
    try {
        if (!req.session.youtubeToken?.access_token) {
            return res.status(401).json({ error: 'Non connecté à YouTube' });
        }
        const videos = await getLikedVideos(req.session.youtubeToken.access_token);
        res.json(videos);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Impossible de récupérer les vidéos' });
    }
});

module.exports = router;
