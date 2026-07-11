import React, { useState } from "react";
import IncidentList from "@/components/incident/IncidentList";
import CreateIncidentModal from "@/components/incident/CreateIncidentModal";
import { Incident } from "@/types";
import { useDashboardData } from "@/hooks/useDashboardData";

const IncidentPage: React.FC = () => {
  useDashboardData();
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-secondary-900">Incident Management</h1>
        <p className="text-secondary-600 mt-2">Manage and track incidents across your organization</p>
      </div>

      <IncidentList
        onCreateClick={() => setShowCreateModal(true)}
        onIncidentClick={(incident) => {
          setSelectedIncident(incident);
        }}
      />

      <CreateIncidentModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
      />

      {selectedIncident && (
        <div className="mt-6 p-6 bg-white rounded-lg shadow-md border border-secondary-200">
          <h2 className="text-xl font-semibold text-secondary-900 mb-4">
            {selectedIncident.title}
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-secondary-600">ID</p>
              <p className="font-medium text-secondary-900">{selectedIncident.id}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Status</p>
              <p className="font-medium text-secondary-900">{selectedIncident.status}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Priority</p>
              <p className="font-medium text-secondary-900">{selectedIncident.priority}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Assigned To</p>
              <p className="font-medium text-secondary-900">
                {selectedIncident.assignedTo || "Unassigned"}
              </p>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-sm text-secondary-600">Description</p>
            <p className="text-secondary-900">{selectedIncident.description}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default IncidentPage;
