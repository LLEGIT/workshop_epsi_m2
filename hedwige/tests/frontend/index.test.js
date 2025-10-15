/**
 * Test de la page index.html
 * Vérifie que le bouton de connexion Microsoft est présent
 */
import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync(path.resolve(__dirname, '../../public/index.html'), 'utf8');

describe('Frontend index.html', () => {
    it('doit contenir un bouton de connexion Microsoft', () => {
        const dom = new JSDOM(html, { runScripts: "outside-only" });
        const button = dom.window.document.querySelector('a');
        expect(button).not.toBeNull();
        expect(button.textContent).toContain('Se connecter avec Microsoft');
    });
});
