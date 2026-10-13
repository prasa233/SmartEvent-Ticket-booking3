
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Booking, Event, Ticket, Notification, User
from app.schemas import BookingCreate, BookingOut

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingOut)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        event = (
            db.query(Event)
            .filter(Event.id == data.event_id)
            .with_for_update()
            .first()
        )

        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        if event.event_status == "CANCELLED":
            raise HTTPException(status_code=400, detail="Event is cancelled")

        if data.ticket_quantity > event.available_tickets:
            raise HTTPException(
                status_code=400,
                detail="Not enough tickets available",
            )

        total = round(event.price * data.ticket_quantity, 2)

        # Create a pending booking. Checkout will confirm it after payment.
        booking = Booking(
            user_id=user.id,
            event_id=event.id,
            quantity=data.ticket_quantity,
            ticket_quantity=data.ticket_quantity,
            total_amount=total,
            total_price=total,
            final_amount=total,
            discount_amount=0.0,
            status="PENDING",
            booking_status="PENDING",
        )

        event.available_tickets -= data.ticket_quantity
        db.add(booking)
        db.flush()

        ticket = Ticket(
            booking_id=booking.id,
            ticket_code=f"TKT-{uuid.uuid4().hex[:12].upper()}",
            qr_code_url=f"/tickets/{booking.id}/qr",
        )

        notification = Notification(
            user_id=user.id,
            title="Booking created",
            message=f"Your booking for {event.title} is awaiting payment.",
            type="BOOKING",
        )

        db.add(ticket)
        db.add(notification)
        db.commit()
        db.refresh(booking)

        return booking

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


@router.get("/history", response_model=list[BookingOut])
def booking_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return (
        db.query(Booking)
        .filter(Booking.user_id == user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )


@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id,
            Booking.user_id == user.id,
        )
        .first()
    )

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.booking_status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    if booking.status == "CONFIRMED":
        raise HTTPException(
            status_code=400,
            detail="A paid booking cannot be cancelled through this endpoint",
        )

    if booking.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending bookings can be cancelled",
        )

    try:
        booking.status = "CANCELLED"
        booking.booking_status = "CANCELLED"

        if booking.event:
            booking.event.available_tickets += booking.quantity

        db.commit()
        return {"message": "Booking cancelled"}

    except Exception:
        db.rollback()
        raise
