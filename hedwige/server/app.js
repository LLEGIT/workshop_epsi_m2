require('dotenv').config();
const express = require('express');
const session = require('express-session');
const path = require('path');

const authRoutes = require('./routes/auth');
const mailRoutes = require('./routes/mail');
const youtubeRoutes = require('./routes/youtube');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: 'supersecretkey',
    resave: false,
    saveUninitialized: true
}));

app.use(express.static(path.join(__dirname, '../public')));

app.use('/auth', authRoutes);
app.use('/mail', mailRoutes);
app.use('/youtube', youtubeRoutes);

module.exports = app;

// Démarrage du serveur uniquement si lancé directement
if (require.main === module) {
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
}
