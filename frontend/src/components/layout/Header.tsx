import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Menu, Bell, User, LogOut } from "lucide-react";
import { RootState } from "@/store";
import { toggleSidebar } from "@/store/slices/uiSlice";
import { logout } from "@/store/slices/authSlice";
import Button from "@/components/common/Button";

const Header: React.FC = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <header className="bg-white border-b border-secondary-200 shadow-sm">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => dispatch(toggleSidebar())}
            className="p-2 hover:bg-secondary-100 rounded-md transition-colors"
          >
            <Menu size={24} className="text-secondary-600" />
          </button>
          <h1 className="text-2xl font-bold text-primary-600">ITSM</h1>
        </div>

        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-secondary-100 rounded-md transition-colors relative">
            <Bell size={20} className="text-secondary-600" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-danger-600 rounded-full" />
          </button>

          <div className="flex items-center gap-3 pl-4 border-l border-secondary-200">
            <div className="text-right">
              <p className="text-sm font-medium text-secondary-900">{user?.name}</p>
              <p className="text-xs text-secondary-500">{user?.role}</p>
            </div>
            <button className="p-2 hover:bg-secondary-100 rounded-md transition-colors">
              <User size={20} className="text-secondary-600" />
            </button>
            <Button
              variant="secondary"
              size="sm"
              icon={<LogOut size={16} />}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
