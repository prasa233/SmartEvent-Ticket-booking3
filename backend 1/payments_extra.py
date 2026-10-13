
from uuid import uuid4
from decimal import Decimal, ROUND_HALF_UP

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Booking, Payment
from ..schemas_extra import PaymentCreate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Payments"])


def money(value):
    return Decimal(str(value)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


@router.post("/checkout", response_model=PaymentOut)
def checkout(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    booking = db.query(Booking).filter(
        Booking.id == data.booking_id,
        Booking.user_id == user.id,
    ).with_for_update().first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.status != "PENDING":
        raise HTTPException(400, "Booking is not pending")
    booking.status = "CONFIRMED"
    booking.booking_status = "CONFIRMED"
    previous = db.query(Payment).filter(
        Payment.booking_id == booking.id,
        Payment.payment_status == "SUCCESS",
    ).first()

    if previous:
        raise HTTPException(400, "Booking already paid")

    amount = (
    booking.final_amount
    if booking.final_amount is not None
    else booking.total_price
    if booking.total_price is not None
    else booking.total_amount
)


    payment = Payment(
        booking_id=booking.id,
        payment_method="SIMULATION",
        payment_status="PENDING",
        amount=float(money(amount)),
    )

    try:
        db.add(payment)
        db.flush()

        # Demo only: simulate a successful payment.
        payment.payment_status = "SUCCESS"
        payment.transaction_id = "SIM-" + uuid4().hex.upper()
        booking.status = "CONFIRMED"

        db.commit()
        db.refresh(payment)
        return payment
    except Exception:
        db.rollback()
        raise
