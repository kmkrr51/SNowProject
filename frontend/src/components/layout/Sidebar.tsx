import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";
import {
  LayoutDashboard,
  AlertCircle,
  AlertTriangle,
  GitBranch,
  FileText,
  Bell,
  History,
  X,
} from "lucide-react";
import { RootState } from "@/store";
import clsx from "clsx";

const Sidebar: React.FC = () => {
  const location = useLocation();
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);

  const navItems = [
    {
      label: "Dashboard",
      href: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      label: "Incidents",
      href: "/incidents",
      icon: AlertCircle,
    },
    {
      label: "Problems",
      href: "/problems",
      icon: AlertTriangle,
    },
    {
      label: "Changes",
      href: "/changes",
      icon: GitBranch,
    },
    {
      label: "Requests",
      href: "/requests",
      icon: FileText,
    },
    {
      label: "Notifications",
      href: "/notifications",
      icon: Bell,
    },
    {
      label: "Audit Trail",
      href: "/audit",
      icon: History,
    },
  ];

  const isActive = (href: string) => location.pathname === href;

  return (
    <>
      <aside
        className={clsx(
          "fixed inset-y-0 left-0 z-40 w-64 bg-secondary-900 text-white overflow-y-auto transition-transform duration-300 ease-in-out",
          sidebarOpen ? "translate-x-0" : "-translate-x-full",
          "md:relative md:translate-x-0",
        )}
      >
        <div className="p-6">
          <h2 className="text-xl font-bold text-white mb-8">ITSM</h2>

          <nav className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.href);

              return (
                <Link
                  key={item.href}
                  to={item.href}
                  className={clsx(
                    "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                    active
                      ? "bg-primary-600 text-white"
                      : "text-secondary-300 hover:bg-secondary-800 hover:text-white",
                  )}
                >
                  <Icon size={20} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </aside>

      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black bg-opacity-50 md:hidden"
          onClick={() => {
            // Dispatch close sidebar action
          }}
        />
      )}
    </>
  );
};

export default Sidebar;
