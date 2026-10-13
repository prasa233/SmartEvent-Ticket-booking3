
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Booking, Event, Review
from ..schemas_extra import ReviewCreate, ReviewUpdate, ReviewOut

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewOut)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    event = db.query(Event).filter(
        Event.id == data.event_id
    ).first()

    if not event:
        raise HTTPException(404, "Event not found")

    if event.event_status != "COMPLETED":
        raise HTTPException(400, "Event is not completed")

    booking = db.query(Booking).filter(
        Booking.user_id == user.id,
        Booking.event_id == event.id,
        Booking.status == "CONFIRMED",
    ).first()

    if not booking:
        raise HTTPException(
            403, "A confirmed booking is required to review"
        )

    existing = db.query(Review).filter(
        Review.user_id == user.id,
        Review.event_id == event.id,
    ).first()

    if existing:
        raise HTTPException(400, "You already reviewed this event")

    review = Review(
        user_id=user.id,
        event_id=event.id,
        rating=data.rating,
        review_text=data.review_text,
    )

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/event/{event_id}")
def event_reviews(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(404, "Event not found")

    reviews = db.query(Review).filter(
        Review.event_id == event_id
    ).order_by(Review.created_at.desc()).all()

    average = db.query(func.avg(Review.rating)).filter(
        Review.event_id == event_id
    ).scalar()

    return {
        "event_id": event_id,
        "average_rating": round(float(average or 0), 2),
        "total_reviews": len(reviews),
        "reviews": [
            ReviewOut.model_validate(r).model_dump(mode="json")
            for r in reviews
        ],
    }


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user.id,
    ).first()

    if not review:
        raise HTTPException(404, "Review not found")

    review.rating = data.rating
    review.review_text = data.review_text

    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user.id,
    ).first()

    if not review:
        raise HTTPException(404, "Review not found")

    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}
