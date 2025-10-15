# Hedwige - Messagerie étudiante Outlook simplifiée

Hedwige est une application web permettant d’envoyer et recevoir des emails via un compte étudiant Outlook. L’application est conçue pour être simple, épurée et sécurisée.

---

## ⚙️ Stack technique

- **Backend** : Node.js + Express
- **Frontend** : HTML + Tailwind CSS (CLI)
- **Authentification** : Microsoft Azure OAuth2.0
- **Tests backend** : Jest
- **Tests frontend** : Vitest
- **CI/CD** : GitHub Actions

---

## 📂 Structure du projet

```text
hedwige/
├─ server/                  # Backend Node.js Express
│  ├─ app.js
│  ├─ routes/
│  ├─ controllers/
│  └─ services/
├─ public/                  # Frontend statique
│  ├─ index.html
│  ├─ mail.html
│  └─ css/
│     ├─ tailwind.css       # Entrée Tailwind
│     └─ output.css         # CSS compilé
├─ tests/
│  ├─ backend/
│  └─ frontend/
├─ package.json
├─ tailwind.config.js
├─ postcss.config.js
└─ README.md
🚀 Installation
Cloner le dépôt :

bash
Copy code
git clone <repo_url>
cd <repo_root>/hedwige
Installer les dépendances :

bash
Copy code
npm install
Installer Tailwind CLI et générer le CSS :

bash
Copy code
npx tailwindcss -i ./public/css/tailwind.css -o ./public/css/output.css --minify
Créer un fichier .env à la racine du dossier /hedwige :

env
Copy code
MICROSOFT_CLIENT_ID=xxxx-xxxx-xxxx-xxxx
MICROSOFT_CLIENT_SECRET=xxxx-xxxx-xxxx-xxxx
MICROSOFT_REDIRECT_URI=http://localhost:3000/auth/callback
SESSION_SECRET=uneCleSecrete
🔑 Configuration Microsoft Azure OAuth
Aller sur Azure Portal.

Créer une App Registration :

Type de comptes : Accounts in any organizational directory (Any Azure AD directory) and personal Microsoft accounts.

Redirect URI : http://localhost:3000/auth/callback

Noter le Client ID et Client Secret.

Ajouter ces valeurs dans le .env.

Permissions API Microsoft Graph :

Mail.ReadWrite

Mail.Send

offline_access

openid

✉️ Gestion des emails
Envoi d’email : via formulaire sur mail.html → /api/send.

Réception d’email : via /api/mails, affichée dynamiquement sur mail.html.

Notifications : zone #status pour succès/erreur de l’envoi.

Logout : bouton #logoutBtn → /auth/logout.

Lien 360Learning : bouton ouvre https://reseau-cd.360learning.com/.

🧪 Tests
Backend (Jest) :

bash
Copy code
npm test
Frontend (Vitest) :

bash
Copy code
npx vitest run
📦 CI/CD GitHub Actions
Fichier : .github/workflows/ci.yml

Exécute l’installation, build Tailwind, tests backend et frontend.

Adapté au monorepo (working-directory: ./hedwige).

Variables sensibles à définir dans les Secrets GitHub :

AZURE_CLIENT_ID

AZURE_CLIENT_SECRET

REDIRECT_URI

SESSION_SECRET

🎨 Frontend
Style épuré et professionnel via Tailwind CSS.

Boutons visibles par défaut (bg-primary, text-white, shadow-md).

Formulaire d’envoi, liste de mails et notifications dynamiques.

💡 Notes
Toutes les opérations OAuth et emails passent par le backend Express pour sécurité.

Compatible navigateur en mode navigation privée, mais certains tokens peuvent être perdus selon les restrictions de stockage.

