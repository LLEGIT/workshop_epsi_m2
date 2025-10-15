/**
 * Test des routes mail
 * Vérifie que les routes protègent l'accès sans session
 */
const request = require('supertest');
const app = require('../../server/app');

describe('Mail routes', () => {
    it('GET /mail/inbox sans session doit renvoyer 401', async () => {
        const res = await request(app).get('/mail/inbox');
        expect(res.status).toBe(401);
    });
});
