# SmartEvent – Modules 12–17

## Module 12: Event Payment System
- Implement payment simulation or Stripe test mode.
- Store payment records and transaction IDs.
- Update booking status after successful payment.
- Create checkout and payment confirmation pages.

## Module 13: Coupon & Discount System
- Create and validate coupons.
- Check expiry dates, minimum amounts, and usage limits.
- Apply fixed or percentage discounts.
- Display the final booking amount.

## Module 14: Event Feedback & Ratings
- Allow attendees to rate and review events.
- Support editing and deleting personal reviews.
- Display reviews and average ratings.
- Validate ratings from 1 to 5.

## Module 15: Advanced Notifications
- Notify users about bookings, payments, and event updates.
- Add notification history and a notification bell.
- Support marking notifications as read.
- Send event reminders and cancellation alerts.

## Module 16: Event Search & Filtering
- Search by event name, category, and location.
- Filter by date range.
- Sort by date, popularity, and price.

## Module 17: Professional UI/UX
- Create modern event cards and dashboards.
- Improve navigation and booking workflows.
- Add animations, loading skeletons, and feedback messages.
- Implement responsive layouts for mobile and desktop.
- Improve typography, spacing, and page transitions.

## Technology Stack
- Backend: FastAPI, SQLAlchemy, Pydantic
- Frontend: React, Vite, Tailwind CSS
- Database: SQLite
- Authentication: JWT
- Payments: Stripe Test Mode
- Testing: Pytest

## Database Updates
- New tables: Payments, Coupons, Reviews.
- Existing tables: Users, Events, Bookings, Tickets, Notifications.
- Add `coupon_id`, `discount_amount`, and `final_amount` to Bookings.

## Security
- JWT authentication and ownership validation.
- Secure payment verification.
- Coupon validation and input validation.
- Environment variables for secret configuration.

## Expected Outcome
A complete event booking platform with secure payments, discounts, reviews, notifications, advanced search, and a professional, responsive user interface.
