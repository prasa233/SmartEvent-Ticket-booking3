
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    toast.success("Logged out successfully");
    navigate("/login");
  }

  return (
    <nav className="navbar">
      <Link className="brand" to="/events">SmartEvent</Link>

      <div className="nav-links">
        <Link to="/events">Events</Link>

        {token && <Link to="/bookings">My Bookings</Link>}

        {role === "ORGANIZER" && (
          <>
            <Link to="/organizer">Organizer Dashboard</Link>
            <Link to="/organizer/events">Manage Events</Link>
            <Link to="/organizer/create">Create Event</Link>
          </>
        )}

        {role === "ADMIN" && (
          <Link to="/admin">Admin Dashboard</Link>
        )}

        {token ? (
          <button onClick={logout}>Logout</button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}