

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import require_organizer
from ..models import User, Event
from ..schemas import EventCreate, EventUpdate, EventResponse

router = APIRouter(prefix="/events", tags=["Events"])


# CREATE EVENT
@router.post("", response_model=EventResponse, status_code=201)
def create_event(
    data: EventCreate,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer),
):
    if data.event_date <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Event date must be in the future",
        )

    event = Event(
        title=data.title,
        description=data.description,
        category=data.category,
        location=data.location,
        event_date=data.event_date,
        price=data.price,
        total_tickets=data.total_tickets,
        organizer_id=organizer.id,
        event_status="UPCOMING",
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


# GET ALL EVENTS — FOR THE FRONTEND
@router.get("", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return (
        db.query(Event)
        .filter(Event.event_status != "CANCELLED")
        .order_by(Event.event_date.asc())
        .all()
    )


# GET ORGANIZER'S EVENTS
@router.get("/my-events", response_model=list[EventResponse])
def get_my_events(
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer),
):
    return (
        db.query(Event)
        .filter(Event.organizer_id == organizer.id)
        .all()
    )


# CANCEL EVENT
@router.patch("/{event_id}/cancel")
def cancel_event(
    event_id: int,
    db: Session = Depends(get_db),
    organizer: User = Depends(require_organizer),
):
    event = db.query(Event).filter(Event.id == event_id).first()

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    if event.organizer_id != organizer.id:
        raise HTTPException(
            status_code=403,
            detail="You can only cancel your own events",
        )

    event.event_status = "CANCELLED"
    db.commit()
    db.refresh(event)

    return {
        "message": "Event cancelled successfully",
        "event_id": event.id,
        "status": event.event_status,
    }
