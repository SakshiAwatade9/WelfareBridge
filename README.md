# WelfareBridge — Flask + MySQL + Bootstrap Setup Guide

Full-stack welfare scheme discovery platform, built with:
**HTML + CSS + JavaScript + Bootstrap** (frontend) → **Python Flask REST API** (backend) → **MySQL** (database)

No frontend build step at all — the frontend is plain static files you open in a browser.

```
welfarebridge-flask/
├── backend/     Flask API (Python)
└── frontend/    Static HTML/CSS/JS + Bootstrap (no build tools needed)
```

---

## 1. Prerequisites

| Tool | Version | Check with |
|---|---|---|
| Python | 3.9+ | `python --version` (or `python3 --version`) |
| MySQL | 8.0+ | `mysql --version` |
| A way to serve static files | any | see step 4 — several options, pick whichever is easiest |

You do **not** need Node.js, npm, or any frontend build tools for this version.

---

## 2. Set up MySQL

Open a MySQL shell (or MySQL Workbench, or the VS Code MySQL extension — whichever you have
working) and create the database:

```sql
CREATE DATABASE welfarebridge;
```

Flask will automatically create all the tables inside it on first run — this step just
creates the empty database itself.

### Configure your MySQL credentials

Copy `backend/.env.example` to a new file named `backend/.env`, then edit the `DATABASE_URL`
line to match your MySQL username/password:

```
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/welfarebridge
```

---

## 3. Run the backend

Open a terminal in the `backend` folder:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (Command Prompt):** `venv\Scripts\activate.bat`
- **Mac/Linux:** `source venv/bin/activate`

Then install dependencies and run:

```bash
pip install -r requirements.txt
python run.py
```

The API starts on **http://localhost:5000**. On first run you'll see:

```
>>> Seeded demo admin account: admin@welfarebridge.gov.in / admin123
>>> Seeded 14 sample welfare schemes.
```

This only happens once — restarting won't duplicate data.

### Quick sanity check

Visit **http://localhost:5000/api/schemes** in your browser — you should see a JSON array
of 14 welfare schemes. If you see that, the backend is working.

> **Windows PowerShell note:** if `python` isn't recognized, try `py` instead
> (e.g. `py -m venv venv`). If `pip` isn't recognized after activating the virtual
> environment, make sure the activation command above actually printed no errors —
> your terminal prompt should show `(venv)` at the start once it's active.

---

## 4. Run the frontend

The frontend is plain static files — **no npm, no build step.** But you do need to serve
it over `http://` rather than double-clicking the HTML files directly, because browsers
block some fetch requests from `file://` URLs. Pick whichever of these is easiest for you:

**Option A — VS Code Live Server extension (easiest if you use VS Code)**
Install the "Live Server" extension, right-click `frontend/index.html`, choose
"Open with Live Server." It'll open automatically, usually at `http://127.0.0.1:5500`.

**Option B — Python's built-in server (no extra install needed)**
Open a **new terminal** (keep the backend running in the other one):
```bash
cd frontend
python -m http.server 5500
```
Then open **http://localhost:5500** in your browser.

Either way, the frontend is already configured (in `js/api.js`) to talk to the backend at
`http://localhost:5000/api`. If you run the backend on a different port, update the
`API_BASE` constant at the top of that file.

---

## 5. Try it out

- **As a citizen:** Click "Check my eligibility" → Register a new account → fill out the
  4-step questionnaire → see your ranked, personalized scheme matches on the dashboard.
- **As the administrator:** Click "Admin sign in" → use the demo account:
  - Email: `admin@welfarebridge.gov.in`
  - Password: `admin123`
  - From there you can add/edit/remove schemes and view usage statistics.

---

## 6. How the pieces fit together

- **Eligibility engine** (`backend/app/eligibility.py`) — the same rule-based logic from
  the PRD (age, income, state, occupation, gender, senior-citizen checks), running in
  Python instead of JavaScript or Java.
- **JWT auth** — on login/register, the backend issues a signed token
  (via Flask-JWT-Extended), which the frontend stores in `localStorage` and attaches to
  every request (`frontend/js/api.js`). Protected routes are guarded with a
  `@roles_required(...)` decorator on the backend (`backend/app/decorators.py`).
- **Role-based access** — citizens can manage their own profile, check eligibility, and
  save schemes; only admins can create/edit/delete schemes or view platform-wide stats,
  enforced both by the Flask backend and by `requireRole(...)` checks in the frontend JS.
- **Data persistence** — everything (accounts, profiles, schemes, saved schemes) lives in
  your local MySQL database and survives restarts.
- **No frontend framework** — each page (`index.html`, `dashboard.html`, etc.) is a
  standalone HTML file. Shared behavior (the navbar, the API client, toast notifications,
  the scheme card/modal rendering) lives in `frontend/js/*.js` files, included via
  `<script>` tags on each page.

---

## 7. Common issues

**"Access denied for user 'root'@'localhost'"**
→ Your password in `backend/.env` doesn't match your actual MySQL root password.

**`mysql` not recognized in the terminal**
→ You don't actually need the `mysql` command-line tool for this to work — Flask connects
to MySQL directly over its network port. You only need the MySQL *server* running as a
service, not the command-line client on your PATH. If you'd still like the `CREATE DATABASE`
step to work from a terminal, add MySQL's `bin` folder (e.g.
`C:\Program Files\MySQL\MySQL Server 8.0\bin`) to your Windows PATH and restart your terminal.

**CORS / network errors in the browser console**
→ Make sure the backend is actually running (`http://localhost:5000/api/health` should
respond). Also make sure you're serving the frontend over `http://`, not opening the HTML
files directly by double-clicking them.

**`ModuleNotFoundError` when running `python run.py`**
→ Your virtual environment probably isn't activated, or `pip install -r requirements.txt`
didn't complete. Re-run the activation command for your OS (step 3), confirm your prompt
shows `(venv)`, then reinstall.

**Port 5000 or 5500 already in use**
→ For the backend, change the port in the last line of `backend/run.py`
(`app.run(..., port=5000)`) and update `API_BASE` in `frontend/js/api.js` to match. For the
frontend, just pick a different port when starting the static server
(e.g. `python -m http.server 5501`).

---

## 8. Production notes (before deploying anywhere public)

This setup is configured for **local development**. Before deploying anywhere real:

- Change `JWT_SECRET_KEY` in `.env` to a new, randomly generated secret.
- Change the demo admin password, or remove the seeded admin account.
- Set Flask's debug mode off (`debug=True` → `debug=False` in `run.py`) and run behind a
  proper WSGI server (e.g. Gunicorn) rather than Flask's built-in dev server.
- Move all secrets into real environment variables rather than a committed `.env` file.
- Restrict CORS (`backend/app/config.py`) to your actual frontend domain instead of `*`.
- Serve the frontend from a real web server (Nginx, a CDN, etc.) rather than
  `python -m http.server`.
