const express = require('express');
const router = express.Router();
const mailController = require('../controllers/mailController');
const authMiddleware = require('../middleware/authMiddleware');

router.use(authMiddleware);

router.get('/inbox', mailController.getInbox);
router.post('/send', mailController.sendMail);

module.exports = router;
