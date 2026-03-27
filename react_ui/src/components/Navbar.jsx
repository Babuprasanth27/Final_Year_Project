import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h3>Network IDS</h3>
      <div>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/manual">Manual</Link>
        <Link to="/live">Live</Link>
        <button
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/";
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
