/**
 * Test de la page mail.html
 * Vérifie la présence du formulaire et des champs
 */
import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync(path.resolve(__dirname, '../../public/mail.html'), 'utf8');

describe('Frontend mail.html', () => {
    let dom, document;

    beforeEach(() => {
        const dom = new JSDOM(html, { runScripts: "outside-only" });
        document = dom.window.document;
    });

    it('doit contenir le formulaire d\'envoi de mail', () => {
        const form = document.querySelector('#sendMailForm');
        expect(form).not.toBeNull();
    });

    it('doit contenir un champ destinataire', () => {
        const to = document.querySelector('#to');
        expect(to).not.toBeNull();
        expect(to.type).toBe('email');
    });

    it('doit contenir un champ sujet', () => {
        const subject = document.querySelector('#subject');
        expect(subject).not.toBeNull();
        expect(subject.type).toBe('text');
    });

    it('doit contenir un champ message', () => {
        const body = document.querySelector('#body');
        expect(body).not.toBeNull();
        expect(body.tagName.toLowerCase()).toBe('textarea');
    });

    it('doit contenir une zone de notifications', () => {
        const notif = document.querySelector('#notifications');
        expect(notif).not.toBeNull();
    });

    it('doit contenir la liste de la boîte de réception', () => {
        const inbox = document.querySelector('#inbox');
        expect(inbox).not.toBeNull();
        expect(inbox.tagName.toLowerCase()).toBe('ul');
    });
});
