
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ---------- Ticket creation ----------

class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str


class TicketCreateResponse(BaseModel):
    ticket_id: str
    created_at: datetime


# ---------- Notes ----------

class NoteOut(BaseModel):
    note_text: str
    created_at: datetime

    class Config:
        from_attributes = True  # lets Pydantic read SQLAlchemy objects directly


# ---------- Ticket list (GET /api/tickets) ----------

class TicketListItem(BaseModel):
    ticket_id: str
    customer_name: str
    subject: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Ticket detail (GET /api/tickets/{id}) ----------

class TicketDetail(BaseModel):
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    notes: List[NoteOut] = []

    class Config:
        from_attributes = True


# ---------- Ticket update (PUT /api/tickets/{id}) ----------

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None  # a new note to add, if provided


class TicketUpdateResponse(BaseModel):
    success: bool
    updated_at: datetime

# ---------- Paginated ticket list ----------

class PaginatedTickets(BaseModel):
    tickets: List[TicketListItem]
    total: int
    page: int
    page_size: int
    total_pages: int