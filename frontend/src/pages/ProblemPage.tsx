import React, { useState } from "react";
import ProblemList from "@/components/problem/ProblemList";
import CreateProblemModal from "@/components/problem/CreateProblemModal";
import { Problem } from "@/types";
import { useProblemsData } from "@/hooks/useProblemsData";

const ProblemPage: React.FC = () => {
  useProblemsData();
  const [selectedProblem, setSelectedProblem] = useState<Problem | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-secondary-900">Problem Management</h1>
        <p className="text-secondary-600 mt-2">
          Identify, investigate, and resolve problems affecting your services
        </p>
      </div>

      <ProblemList
        onCreateClick={() => setShowCreateModal(true)}
        onProblemClick={(problem) => {
          setSelectedProblem(problem);
        }}
      />

      <CreateProblemModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
      />

      {selectedProblem && (
        <div className="mt-6 p-6 bg-white rounded-lg shadow-md border border-secondary-200">
          <h2 className="text-xl font-semibold text-secondary-900 mb-4">
            {selectedProblem.title}
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-secondary-600">ID</p>
              <p className="font-medium text-secondary-900">{selectedProblem.id}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Status</p>
              <p className="font-medium text-secondary-900">{selectedProblem.status}</p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Related Incidents</p>
              <p className="font-medium text-secondary-900">
                {selectedProblem.relatedIncidents?.length || 0}
              </p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Impacted Services</p>
              <p className="font-medium text-secondary-900">
                {selectedProblem.impactedServices?.length || 0}
              </p>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-sm text-secondary-600">Description</p>
            <p className="text-secondary-900">{selectedProblem.description}</p>
          </div>
          {selectedProblem.rootCause && (
            <div className="mt-4">
              <p className="text-sm text-secondary-600">Root Cause</p>
              <p className="text-secondary-900">{selectedProblem.rootCause}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ProblemPage;
