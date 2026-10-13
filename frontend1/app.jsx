
import { useState } from "react";
import {
  Routes,
  Route,
  NavLink,
  Navigate,
  useNavigate,
} from "react-router-dom";
import {
  CalendarDays,
  Ticket,
  Bell,
  Star,
  Search,
  Menu,
  X,
} from "lucide-react";

import Events from "./pages/Events";
import Checkout from "./pages/Checkout";
import PaymentConfirmation from "./pages/PaymentConfirmation";
import Reviews from "./pages/Reviews";
import Notifications from "./pages/Notifications";
import PaymentCheckout from "./pages/PaymentCheckout.jsx";

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();

  const links = [
    { to: "/events", label: "Explore Events", icon: Search },
    { to: "/checkout", label: "Checkout", icon: Ticket },
    { to: "/reviews", label: "Reviews", icon: Star },
    { to: "/notifications", label: "Notifications", icon: Bell },
  ];

  return (
    <div className="app-shell">
      <header className="navbar">
        <button
          className="brand"
          onClick={() => navigate("/events")}
          type="button"
        >
          <span className="brand-icon">
            <CalendarDays size={23} />
          </span>
          <span>
            Smart<span className="brand-highlight">Event</span>
          </span>
        </button>

        <button
          className="mobile-menu"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle navigation"
          type="button"
        >
          {menuOpen ? <X /> : <Menu />}
        </button>

        <nav className={menuOpen ? "nav-links nav-open" : "nav-links"}>
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setMenuOpen(false)}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              <Icon size={17} />
              {label}
            </NavLink>
          ))}
        </nav>

        <button
          className="profile-button"
          onClick={() => navigate("/events")}
          type="button"
        >
          Discover <span>↗</span>
        </button>
      </header>

      <main className="page-container">
        <Routes>
          <Route path="/" element={<Navigate to="/events" replace />} />
          <Route path="/events" element={<Events />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route
            path="/payment/checkout"
            element={<PaymentCheckout />}
          />
          <Route
            path="/payment-confirmation"
            element={<PaymentConfirmation />}
          />
          <Route path="/reviews" element={<Reviews />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route
            path="*"
            element={<Navigate to="/events" replace />}
          />
        </Routes>
      </main>

      <footer className="footer">
        <strong>SmartEvent</strong>
        <span>Discover experiences. Create memories.</span>
        <span>© 2026 SmartEvent</span>
      </footer>
    </div>
  );
}
