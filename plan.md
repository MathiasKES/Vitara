# Vitara — Project Planning Document

> **GitHub Description:**
> `Vitara is a personal journaling and fitness tracking web app — beautifully minimal, privacy-first, and built for daily use. Log your thoughts, track your workouts, and watch yourself grow.`

---

## 1. Tech Stack

### Why Python + Flask?
Flask is a micro-framework — it runs lean, boots fast, and has no bloat. A small Vitara instance can run on as little as 50–80MB RAM, making it ideal for a VPS, Raspberry Pi, or free-tier cloud hosting.

| Layer | Choice | Reason |
|---|---|---|
| **Language** | Python 3.11+ | Readable, fast to write, great ecosystem |
| **Framework** | Flask | Lightweight, minimal overhead, full control |
| **Database** | SQLite (dev) → PostgreSQL (prod) | SQLite needs zero setup; easy to migrate later |
| **ORM** | SQLAlchemy | Clean model definitions, DB-agnostic |
| **Auth** | Flask-Login + Werkzeug | Session management + password hashing built in |
| **Forms** | WTForms + Flask-WTF | CSRF protection, clean validation |
| **Frontend** | Jinja2 + Vanilla JS + Custom CSS | No heavy JS framework, fast load times |
| **Styling** | Custom CSS (CSS variables + flexbox/grid) | Full design control, no framework bloat |
| **Icons** | Lucide Icons (CDN) | Clean, consistent SVG icon set |
| **Fonts** | Google Fonts (CDN) | Loaded only what we need |

### Not Used (and why)
- ❌ Django — too heavy for this scope
- ❌ React/Vue — overkill; Jinja2 + sprinkles of JS is sufficient
- ❌ Tailwind — CDN version is fine for prototyping but we want full CSS control for the design vision

---

## 2. Features

### Authentication
- [x] Register with email + password
- [x] Login / Logout
- [x] "Remember me" session persistence
- [x] Password hashing (bcrypt via Werkzeug)
- [ ] *(v2)* Password reset via email

### User Profile
- [x] Display name, avatar (initials-based, no uploads needed)
- [x] Bio / personal tagline
- [x] Unit preference (kg/lbs, km/miles)
- [x] Account settings (change password, delete account)

### Journal
- [x] Create, Read, Update, Delete (CRUD) journal entries
- [x] Rich text via a lightweight editor (Quill.js CDN)
- [x] Mood tag per entry (😊 Great / 🙂 Good / 😐 Neutral / 😔 Low / 😞 Hard)
- [x] Entry date (auto-set to today, editable)
- [x] Search entries by keyword
- [x] Filter by mood or date range
- [x] Calendar view to see which days have entries
- [ ] *(v2)* Tags/categories per entry

### Fitness Tracker
- [x] Log a workout: date, type, duration, notes
- [x] Workout types: Running, Cycling, Swimming, Strength, Yoga, Walking, Other
- [x] Log sets/reps/weight for strength sessions
- [x] Weekly summary view (total time, sessions, calories if entered)
- [x] Progress charts (bodyweight over time, workout frequency)
- [x] Personal records (PRs) — auto-detected for strength lifts
- [ ] *(v2)* Custom workout templates

### Dashboard (Home)
- [x] Greeting with user's name + current date
- [x] Today's journal entry quick-access (write or view)
- [x] This week's workout summary widget
- [x] Current streak (consecutive days with a journal entry or workout)
- [x] Recent activity feed

### Data & Privacy
- [x] All data is private per user — no social features
- [x] Export all data as JSON (GDPR-friendly)
- [x] Delete account wipes all associated data

---

## 3. UI / UX Design Language

### Aesthetic Direction: **"Refined Calm"**
Clean, warm, editorial. Inspired by quality notebooks and analog tools.
Not cold/clinical. Not playful/childish. Confident and personal.

### Color Palette
```
--color-bg:         #F7F5F0   /* Warm off-white — like good paper */
--color-surface:    #FFFFFF   /* Cards and panels */
--color-border:     #E8E3DB   /* Subtle warm borders */
--color-text:       #1C1917   /* Near-black, warm tone */
--color-muted:      #78716C   /* Secondary text */
--color-accent:     #2D6A4F   /* Forest green — life, growth */
--color-accent-lt:  #D8F3DC   /* Light green for tags/badges */
--color-danger:     #C0392B   /* Errors / delete */
--color-warning:    #E67E22   /* Warnings */
```

### Typography
```
Display font:  'Playfair Display' — Elegant serif for headings
Body font:     'DM Sans' — Clean, modern, highly readable
Mono font:     'JetBrains Mono' — For stats and numbers
```

### Design Principles
- **Generous whitespace** — breathing room everywhere
- **No borders overload** — use shadows and spacing, not boxes
- **Consistent 8px grid** — all spacing is multiples of 8
- **Subtle transitions** — 200ms ease on hover states
- **Mobile-first** — works beautifully on phone, tablet, desktop
- **Dark mode** — supported via CSS variables + `prefers-color-scheme`

### Key UI Components
- Sidebar navigation (collapsible on mobile)
- Card-based content blocks
- Floating action button for "New Entry"
- Mood pills (colored badge buttons)
- Mini calendar widget
- Progress rings for streak tracking
- Toast notifications (no modal popups for simple actions)

---

## 4. File & Folder Structure

```
vitara/
│
├── app/                        # Application package
│   ├── __init__.py             # App factory, extensions init
│   ├── config.py               # Config classes (Dev, Prod, Test)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── journal.py          # Journal entry model
│   │   └── fitness.py          # Workout + exercise models
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py           # /login, /register, /logout
│   │   └── forms.py            # LoginForm, RegisterForm
│   ├── journal/
│   │   ├── __init__.py
│   │   ├── routes.py           # /journal, /journal/new, etc.
│   │   └── forms.py            # JournalEntryForm
│   ├── fitness/
│   │   ├── __init__.py
│   │   ├── routes.py           # /fitness, /fitness/log, etc.
│   │   └── forms.py            # WorkoutForm
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py           # /, /dashboard, /profile, /settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # JSON endpoints for charts/calendar
│   ├── static/
│   │   ├── css/
│   │   │   ├── base.css        # Variables, reset, typography
│   │   │   ├── layout.css      # Sidebar, nav, page shell
│   │   │   ├── components.css  # Cards, buttons, forms, badges
│   │   │   ├── journal.css     # Journal-specific styles
│   │   │   ├── fitness.css     # Fitness-specific styles
│   │   │   └── dark.css        # Dark mode overrides
│   │   ├── js/
│   │   │   ├── app.js          # Global JS (sidebar, toasts, theme)
│   │   │   ├── calendar.js     # Mini calendar widget
│   │   │   ├── charts.js       # Chart.js wrappers
│   │   │   └── editor.js       # Quill rich text init
│   │   └── img/
│   │       └── logo.svg        # Vitara logo
│   └── templates/
│       ├── base.html           # Master layout with sidebar
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── main/
│       │   ├── dashboard.html
│       │   ├── profile.html
│       │   └── settings.html
│       ├── journal/
│       │   ├── index.html      # Entry list + calendar
│       │   ├── entry.html      # Single entry view
│       │   └── editor.html     # New / edit entry
│       └── fitness/
│           ├── index.html      # Workout log + stats
│           ├── log.html        # New / edit workout
│           └── stats.html      # Charts and PRs
│
├── migrations/                 # Flask-Migrate DB migrations
├── tests/
│   ├── test_auth.py
│   ├── test_journal.py
│   └── test_fitness.py
│
├── .env.example                # Template for environment variables
├── .gitignore
├── README.md
├── requirements.txt            # Python dependencies
├── run.py                      # Entry point: `python run.py`
└── wsgi.py                     # Production WSGI entry (gunicorn)
```

---

## 5. Data Models

### User
```
id              INTEGER     PK
email           VARCHAR     UNIQUE, NOT NULL
display_name    VARCHAR     NOT NULL
password_hash   VARCHAR     NOT NULL
bio             TEXT
unit_system     VARCHAR     DEFAULT 'metric'   # 'metric' | 'imperial'
created_at      DATETIME
last_seen       DATETIME
```

### JournalEntry
```
id              INTEGER     PK
user_id         INTEGER     FK → User
title           VARCHAR
body            TEXT        # Stored as HTML from Quill
mood            VARCHAR     # 'great'|'good'|'neutral'|'low'|'hard'
entry_date      DATE        # User-chosen date
created_at      DATETIME
updated_at      DATETIME
```

### Workout
```
id              INTEGER     PK
user_id         INTEGER     FK → User
workout_type    VARCHAR     # 'running'|'strength'|etc.
workout_date    DATE
duration_mins   INTEGER
calories        INTEGER     NULLABLE
notes           TEXT
created_at      DATETIME
```

### Exercise (child of Workout, for strength sessions)
```
id              INTEGER     PK
workout_id      INTEGER     FK → Workout
name            VARCHAR     # e.g. 'Bench Press'
sets            INTEGER
reps            INTEGER
weight          FLOAT       # In user's preferred unit
```

---

## 6. Build Roadmap

### Phase 1 — Foundation
- [ ] Git repo init + project structure
- [ ] Flask app factory + config
- [ ] SQLAlchemy + Flask-Migrate setup
- [ ] User model + auth routes (register/login/logout)
- [ ] Base HTML template + sidebar layout
- [ ] CSS design system (variables, typography, components)

### Phase 2 — Journal
- [ ] Journal model + CRUD routes
- [ ] Entry list page with mood filter
- [ ] Rich text editor (Quill.js)
- [ ] Mini calendar widget
- [ ] Search functionality

### Phase 3 — Fitness Tracker
- [ ] Workout + Exercise models
- [ ] Log workout form (dynamic exercise rows for strength)
- [ ] Workout history list
- [ ] Stats page + Chart.js integration
- [ ] PR auto-detection logic

### Phase 4 — Dashboard & Polish
- [ ] Dashboard with widgets
- [ ] Streak calculation
- [ ] Dark mode
- [ ] Profile + settings pages
- [ ] Data export (JSON)
- [ ] Toast notification system

### Phase 5 — Testing & Deployment
- [ ] Unit tests for models and routes
- [ ] .env + secrets management
- [ ] gunicorn + nginx deployment guide
- [ ] README with setup instructions

---

## 7. Python Dependencies (`requirements.txt`)

```
flask>=3.0
flask-login>=0.6
flask-sqlalchemy>=3.1
flask-migrate>=4.0
flask-wtf>=1.2
werkzeug>=3.0
python-dotenv>=1.0
wtforms>=3.1
email-validator>=2.1
gunicorn>=21.0          # Production server
```

**Estimated RAM usage:** ~60–80MB idle, ~100–120MB under light load.

---

## 8. Git & GitHub Conventions

- **Branches:** `main` (stable) → `dev` (working) → feature branches (`feature/journal-editor`)
- **Commits:** Conventional commits — `feat:`, `fix:`, `style:`, `refactor:`, `test:`, `docs:`
- **Issues:** One issue per feature/bug
- **README:** Setup guide, screenshots, license

---

*Planning complete. Ready to build Phase 1.*