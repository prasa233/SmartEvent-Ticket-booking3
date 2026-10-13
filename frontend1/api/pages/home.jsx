import { useEffect, useState } from "react";
import api from "../axios";

function Home() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  const fetchEvents = async () => {
    try {
      const response = await api.get(
        "GET http://127.0.0.1:8000/events/",
        {
          params: {
            search: search || undefined,
            category: category || undefined,
          },
        }
      );

      setEvents(response.data);

    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [search, category]);

  return (
    <div>

      <h1>SmartEvent</h1>

      <input
        placeholder="Search events..."
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
      />

      <select
        value={category}
        onChange={(e) =>
          setCategory(e.target.value)
        }
      >
        <option value="">
          All Categories
        </option>

        <option value="Music">
          Music
        </option>

        <option value="Tech">
          Tech
        </option>

        <option value="Sports">
          Sports
        </option>

        <option value="Business">
          Business
        </option>
      </select>

      {events.map((event) => (
        <div key={event.id}>

          <h2>{event.title}</h2>

          <p>
            {event.description}
          </p>

          <p>
            Location: {event.location}
          </p>

          <p>
            Price: ₹{event.ticket_price}
          </p>

          <p>
            Tickets:
            {event.available_tickets}
          </p>

        </div>
      ))}

    </div>
  );
}

export default Home;