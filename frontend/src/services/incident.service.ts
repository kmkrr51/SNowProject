import apiClient from "./api";
import { Incident, WorkNote, PaginatedResponse } from "@/types";

export const incidentService = {
  getIncidents: async (
    page: number = 1,
    pageSize: number = 10,
    filters?: Record<string, any>,
  ): Promise<PaginatedResponse<Incident>> => {
    const params = { page, pageSize, ...filters };
    const response = await apiClient.get<PaginatedResponse<Incident>>(
      "/incidents",
      { params },
    );
    return response.data;
  },

  getIncidentById: async (id: string): Promise<Incident> => {
    const response = await apiClient.get<Incident>(`/incidents/${id}`);
    return response.data;
  },

  createIncident: async (data: Partial<Incident>): Promise<Incident> => {
    const response = await apiClient.post<Incident>("/incidents", data);
    return response.data;
  },

  updateIncident: async (id: string, data: Partial<Incident>): Promise<Incident> => {
    const response = await apiClient.patch<Incident>(`/incidents/${id}`, data);
    return response.data;
  },

  assignIncident: async (id: string, technicianId: string): Promise<Incident> => {
    const response = await apiClient.post<Incident>(
      `/incidents/${id}/assign`,
      { technician_id: technicianId },
    );
    return response.data;
  },

  changeIncidentStatus: async (
    id: string,
    newStatus: string,
  ): Promise<Incident> => {
    const response = await apiClient.post<Incident>(
      `/incidents/${id}/change-status`,
      { new_status: newStatus },
    );
    return response.data;
  },

  addWorkNote: async (incidentId: string, content: string): Promise<WorkNote> => {
    const response = await apiClient.post<WorkNote>(
      `/incidents/${incidentId}/work-notes`,
      { content },
    );
    return response.data;
  },

  getWorkNotes: async (incidentId: string): Promise<WorkNote[]> => {
    const response = await apiClient.get<WorkNote[]>(
      `/incidents/${incidentId}/work-notes`,
    );
    return response.data;
  },
};
