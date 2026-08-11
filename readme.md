# Support CRM

A full-stack customer support ticketing system built for the Datastraw AI + Tech

## Live Demo
- **App:** [https://support-crm-k68j.onrender.com/]
- **API Docs:** [https://support-crm-k68j.onrender.com/docs]

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** SQLite + SQLAlchemy ORM
- **Frontend:** Vanilla HTML, CSS, JavaScript (no framework — talks to the backend via `fetch()`)
- **Deployment:** Render.com

## Features
- Create tickets with customer info, subject, and description
- Auto-generated ticket IDs and timestamps
- List view with live search (name, email, ticket ID, description) and status filtering
- Pagination (10 tickets per page) — added as the stand-out feature to handle high ticket volume
- Ticket detail view with status updates and note/comment history
- Demo data auto-seeds on first run

## Why pagination as the stand-out feature
The assignment asks what a real team handling hundreds of tickets a day would need. An unpaginated list breaks down fast at that scale — both for page load performance and for a human trying to scan it. I added server-side pagination (`page`/`page_size` query params, with total count and page metadata returned) rather than just a frontend "load more" button, since the filtering logic (search + status) needed to stay in sync with which page you're on.

**Tradeoff:** to support pagination properly, `GET /api/tickets` returns an object (`{ tickets, total, page, total_pages }`) instead of a bare array as shown in the original spec — a deliberate deviation, since a frontend can't render page controls without knowing the total.

## Project Structure
\```
support-crm/
├── app/
│   ├── main.py        # FastAPI app, routes, API endpoints
│   ├── database.py     # DB connection/session setup
│   ├── models.py        # SQLAlchemy table definitions
│   ├── schemas.py        # Pydantic request/response validation
│   ├── seed.py            # Auto-seeds demo data on first run
│   ├── static/             # CSS + JS
│   └── templates/           # HTML pages
├── requirements.txt
├── .env.example
└── README.md
\```

## Running Locally

1. Clone the repo and enter the folder:
\```bash
git clone [https://github.com/Zishan108/support-crm]
cd support-crm
\```

2. Create and activate a virtual environment:
\```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
\```

3. Install dependencies:
\```bash
pip install -r requirements.txt
\```

4. Run the app:
\```bash
uvicorn app.main:app --reload
\```

5. Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

The database is created and seeded with sample data automatically on first run — no manual setup needed.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/api/tickets` | Create a new ticket |
| GET | `/api/tickets?status=&search=&page=&page_size=` | List tickets (filtered, paginated) |
| GET | `/api/tickets/{ticket_id}` | Get full ticket details |
| PUT | `/api/tickets/{ticket_id}` | Update status and/or add a note |

Full interactive docs available at `/docs` once running.

## Challenges & Solutions
- **Jinja2 `TemplateResponse` API change:** hit a `TypeError` from an older argument order in a newer Starlette version — fixed by passing `request` as the first positional argument.
- **SQLite foreign key constraints:** had to delete `notes` rows before `tickets` rows when resetting demo data, since notes reference tickets via foreign key.
- **Ephemeral filesystem on free-tier deploys:** rather than committing a database file (which would be wiped on restart), built a seed script that repopulates demo data automatically only if the database is empty.

## Improvements With More Time
- Authentication for support agents
- Ticket priority levels and assignment to specific agents
- Email notifications on status changes