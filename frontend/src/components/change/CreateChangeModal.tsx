import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { X } from "lucide-react";
import { AppDispatch } from "@/store";
import { createChange } from "@/store/thunks/changeThunks";
import Button from "@/components/common/Button";

interface CreateChangeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const CreateChangeModal: React.FC<CreateChangeModalProps> = ({
  isOpen,
  onClose,
}) => {
  const dispatch = useDispatch<AppDispatch>();
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    changeType: "STANDARD",
    riskLevel: "MEDIUM",
    impactAssessment: "",
    rollbackPlan: "",
    createdBy: "admin@company.com",
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await dispatch(createChange(formData)).unwrap();
      setFormData({
        title: "",
        description: "",
        changeType: "STANDARD",
        riskLevel: "MEDIUM",
        impactAssessment: "",
        rollbackPlan: "",
        createdBy: "admin@company.com",
      });
      onClose();
    } catch (error) {
      console.error("Failed to create change:", error);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      zIndex: 9999,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      backgroundColor: "rgba(0, 0, 0, 0.5)",
    }}>
      <div style={{
        backgroundColor: "white",
        borderRadius: "8px",
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
        maxWidth: "448px",
        width: "100%",
        margin: "0 16px",
        maxHeight: "90vh",
        overflowY: "auto",
        zIndex: 10000,
      }}>
        <div className="flex items-center justify-between p-6 border-b border-secondary-200 sticky top-0 bg-white">
          <h2 className="text-xl font-semibold text-secondary-900">
            Create New Change
          </h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-secondary-100 rounded-md transition-colors"
          >
            <X size={20} className="text-secondary-600" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-1">
              Title
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
              className="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Change title"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-1">
              Description
            </label>
            <textarea
              required
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              className="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Change description"
              rows={2}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-1">
              Risk Level
            </label>
            <select
              value={formData.riskLevel}
              onChange={(e) =>
                setFormData({ ...formData, riskLevel: e.target.value })
              }
              className="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-secondary-700 mb-1">
              Impact Assessment
            </label>
            <input
              type="text"
              value={formData.impactAssessment}
              onChange={(e) =>
                setFormData({ ...formData, impactAssessment: e.target.value })
              }
              className="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Impact assessment"
            />
          </div>

          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={onClose}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              loading={loading}
              className="flex-1"
            >
              Create
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateChangeModal;
