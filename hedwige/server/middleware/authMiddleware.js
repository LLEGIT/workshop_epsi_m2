module.exports = (req, res, next) => {
    if (!req.session.accessToken) return res.status(401).send('Non autorisé');
    next();
};
