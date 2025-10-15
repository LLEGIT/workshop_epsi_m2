const axios = require('axios');

exports.getInbox = async (accessToken) => {
    const response = await axios.get('https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages', {
        headers: { Authorization: `Bearer ${accessToken}` }
    });
    return response.data.value.map(mail => ({
        id: mail.id,
        subject: mail.subject,
        from: mail.from.emailAddress.name,
        body: mail.bodyPreview
    }));
};

exports.sendMail = async (accessToken, { to, subject, body }) => {
    const message = {
        message: {
            subject,
            body: { contentType: 'Text', content: body },
            toRecipients: [{ emailAddress: { address: to } }]
        }
    };
    await axios.post('https://graph.microsoft.com/v1.0/me/sendMail', message, {
        headers: { Authorization: `Bearer ${accessToken}` }
    });
};
