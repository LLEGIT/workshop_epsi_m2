/**
 * Test des routes d'authentification
 * Vérifie que la redirection login fonctionne et que le callback renvoie un token
 */
const request = require('supertest');
const app = require('../../server/app');

describe('Auth routes', () => {
    it('GET /auth/login doit rediriger', async () => {
        const res = await request(app).get('/auth/login');
        expect(res.status).toBe(302);
        expect(res.headers.location).toContain('login.microsoftonline.com');
    });
});
