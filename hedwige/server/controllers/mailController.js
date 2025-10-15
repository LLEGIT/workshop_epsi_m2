const mailService = require('../services/mailService');

exports.getInbox = async (req, res) => {
    try {
        const mails = await mailService.getInbox(req.session.accessToken);
        res.json(mails);
    } catch (err) {
        res.status(500).json({ error: 'Impossible de récupérer les mails' });
    }
};

exports.sendMail = async (req, res) => {
    const { to, subject, body } = req.body;
    try {
        await mailService.sendMail(req.session.accessToken, { to, subject, body });
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'Impossible d\'envoyer le mail' });
    }
};
