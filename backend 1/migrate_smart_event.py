
import sqlite3

from app.database import Base, engine
from app import models  # Register all SQLAlchemy models


def migrate():
    # Create only tables that do not already exist.
    Base.metadata.create_all(bind=engine)

    connection = sqlite3.connect("smart_event.db")

    try:
        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(bookings)"
            ).fetchall()
        }

        new_columns = {
            "booking_status": "VARCHAR(30)",
            "ticket_quantity": "INTEGER",
            "total_price": "FLOAT",
            "final_amount": "FLOAT",
            "coupon_id": "INTEGER",
            "discount_amount": "FLOAT NOT NULL DEFAULT 0.0",
            "created_at": "DATETIME",
        }

        for column, definition in new_columns.items():
            if column not in columns:
                connection.execute(
                    f"ALTER TABLE bookings ADD COLUMN "
                    f"{column} {definition}"
                )
                print(f"Added bookings.{column}")
            else:
                print(f"Already exists: bookings.{column}")

        # Preserve existing booking values and populate compatible fields.
        connection.execute("""
            UPDATE bookings
            SET ticket_quantity = quantity
            WHERE ticket_quantity IS NULL
        """)

        connection.execute("""
            UPDATE bookings
            SET total_price = total_amount
            WHERE total_price IS NULL
        """)

        connection.execute("""
            UPDATE bookings
            SET final_amount = total_amount
            WHERE final_amount IS NULL
        """)

        connection.execute("""
            UPDATE bookings
            SET booking_status = status
            WHERE booking_status IS NULL
        """)

        connection.execute("""
            UPDATE bookings
            SET created_at = CURRENT_TIMESTAMP
            WHERE created_at IS NULL
        """)

        connection.commit()
        print("Migration completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    migrate()
