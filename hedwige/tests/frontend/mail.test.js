import { describe, it, expect, beforeAll } from 'vitest';
import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

let document;

beforeAll(() => {
    const html = fs.readFileSync(path.resolve('./public/mail.html'), 'utf-8');
    const dom = new JSDOM(html);
    document = dom.window.document;
});

describe('Frontend mail.html', () => {
    it('doit contenir le formulaire d\'envoi de mail', () => {
        // Adapté à l'ID réel dans mail.html
        const form = document.querySelector('#mailForm');
        expect(form).not.toBeNull();
        expect(form.tagName.toLowerCase()).toBe('form');
    });

    it('doit contenir une zone de notifications', () => {
        // Adapté à l'ID réel dans mail.html
        const notif = document.querySelector('#status');
        expect(notif).not.toBeNull();
    });

    it('doit contenir la liste de la boîte de réception', () => {
        // Adapté à l'ID réel dans mail.html
        const inbox = document.querySelector('#mailList');
        expect(inbox).not.toBeNull();
        expect(inbox.tagName.toLowerCase()).toBe('div'); // car dans mail.html c'est un div
    });
});
