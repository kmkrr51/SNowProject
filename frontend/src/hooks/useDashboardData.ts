import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { fetchIncidents } from "@/store/thunks/incidentThunks";
import { AppDispatch } from "@/store";

export const useDashboardData = () => {
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchIncidents());
  }, [dispatch]);
};
