import { NavLink, Outlet, useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import { useAuth } from "../hooks/useAuth";

const navItems = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/leads", label: "Lead Engine" },
];

export function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <div className="flex min-h-screen">
      <aside className="flex w-64 flex-col bg-sidebar text-gray-300">
        <div className="border-b border-sidebar-border px-6 py-5">
          <img src={logo} alt="The Mac Media" className="h-12 w-auto" />
          <p className="mt-2 text-xs uppercase tracking-widest text-gray-500">Nexus</p>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `block rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                  isActive
                    ? "bg-sidebar-hover text-white"
                    : "text-gray-400 hover:bg-sidebar-hover hover:text-white"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-sidebar-border px-4 py-4">
          <div className="mb-3 px-2">
            <p className="truncate text-sm font-medium text-white">
              {user?.first_name} {user?.last_name}
            </p>
            <p className="truncate text-xs text-gray-500">{user?.email}</p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full rounded-lg px-3 py-2 text-left text-sm text-gray-400 transition hover:bg-sidebar-hover hover:text-white"
          >
            Sign out
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-auto bg-gray-50">
        <Outlet />
      </main>
    </div>
  );
}
