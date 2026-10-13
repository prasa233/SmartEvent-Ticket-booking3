
import sqlite3

DB_NAME = "smart_event.db"


def migrate():
    connection = sqlite3.connect(DB_NAME)

    try:
        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(events)"
            ).fetchall()
        }

        if "available_tickets" not in columns:
            connection.execute(
                "ALTER TABLE events "
                "ADD COLUMN available_tickets INTEGER"
            )
            print("Added events.available_tickets")
        else:
            print("available_tickets already exists")

        connection.execute("""
            UPDATE events
            SET available_tickets = total_tickets
            WHERE available_tickets IS NULL
        """)

        connection.commit()
        print("Inventory migration completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    migrate()
