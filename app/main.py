
from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from . import models, schemas
from .database import engine, get_db

# Creates the actual tables in support_crm.db if they don't exist yet.
# This runs once, when the app starts.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support CRM")

# Mounts the /static folder so CSS/JS files are servable at /static/...
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Points Jinja2 at our templates folder so we can return HTML pages.
templates = Jinja2Templates(directory="app/templates")


# =========================================================
# API ENDPOINTS (the 4 required by the assignment)
# =========================================================

@app.post("/api/tickets", response_model=schemas.TicketCreateResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    """Creates a new support ticket."""
    new_ticket = models.Ticket(
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)  # reloads it so we get the auto-generated ticket_id
    return new_ticket


@app.get("/api/tickets", response_model=schemas.PaginatedTickets)
def list_tickets(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lists tickets, optionally filtered by status/search, paginated."""
    query = db.query(models.Ticket)

    if status:
        query = query.filter(models.Ticket.status == status)

    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(
                models.Ticket.customer_name.ilike(term),
                models.Ticket.customer_email.ilike(term),
                models.Ticket.ticket_id.ilike(term),
                models.Ticket.description.ilike(term),
                models.Ticket.subject.ilike(term),
            )
        )

    query = query.order_by(models.Ticket.created_at.desc())

    total = query.count()
    total_pages = max(1, (total + page_size - 1) // page_size)  # ceiling division
    offset = (page - 1) * page_size
    tickets = query.offset(offset).limit(page_size).all()

    return {
        "tickets": tickets,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@app.get("/api/tickets/{ticket_id}", response_model=schemas.TicketDetail)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """Returns full details for one ticket, including its notes."""
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.put("/api/tickets/{ticket_id}", response_model=schemas.TicketUpdateResponse)
def update_ticket(ticket_id: str, update: schemas.TicketUpdate, db: Session = Depends(get_db)):
    """Updates a ticket's status and/or adds a note."""
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if update.status:
        ticket.status = update.status

    if update.notes:
        new_note = models.Note(ticket_id=ticket.id, note_text=update.notes)
        db.add(new_note)

    db.commit()
    db.refresh(ticket)
    return {"success": True, "updated_at": ticket.updated_at}


# =========================================================
# HTML PAGES (frontend)
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    return templates.TemplateResponse(request, "create.html", {})


@app.get("/tickets/{ticket_id}", response_class=HTMLResponse)
def detail_page(request: Request, ticket_id: str):
    return templates.TemplateResponse(request, "detail.html", {"ticket_id": ticket_id})