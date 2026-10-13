

import { useEffect, useState } from "react";
import api from "../services/api";

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchEvents() {
      try {
        setLoading(true);
        setError("");

        const response = await api.get("/events/");
        const data = response.data;

        setEvents(
          Array.isArray(data)
            ? data
            : Array.isArray(data.items)
              ? data.items
              : []
        );
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            err.message ||
            "Unable to load events."
        );
      } finally {
        setLoading(false);
      }
    }

    fetchEvents();
  }, []);

  return (
    <div style={{ padding: "24px" }}>
      <h1>SmartEvent — Explore Events</h1>
      <p>Discover events and book your tickets.</p>

      {loading && <p>Loading events...</p>}

      {!loading && error && (
        <div>
          <p style={{ color: "red" }}>Error: {error}</p>
          <p>Check that your FastAPI backend is running.</p>
        </div>
      )}

      {!loading && !error && events.length === 0 && (
        <p>No events found. Please create an event first.</p>
      )}

      {!loading &&
        !error &&
        events.map((event) => (
          <div
            key={event.id}
            style={{
              background: "white",
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "16px",
              marginBottom: "12px",
            }}
          >
            <h2>{event.title}</h2>
            <p>{event.description}</p>
            <p>Location: {event.location}</p>
            <p>Category: {event.category}</p>
            <p>
              Ticket price: ₹
              {event.ticket_price ?? event.price ?? 0}
            </p>
          </div>
        ))}
    </div>
  );
}
