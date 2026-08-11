
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


def generate_ticket_id():
    """
    Generates a short, human-friendly ticket ID like TKT-A1B2C3
    instead of a raw incrementing number, so IDs look professional
    in a real support tool.
    """
    return f"TKT-{uuid.uuid4().hex[:6].upper()}"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True, default=generate_ticket_id)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="Open")  # Open / In Progress / Closed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # This creates a Python-side link: ticket.notes gives you all
    # Note objects tied to this ticket, ordered by newest first.
    notes = relationship(
        "Note", back_populates="ticket", cascade="all, delete-orphan",
        order_by="desc(Note.created_at)"
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    ticket = relationship("Ticket", back_populates="notes")