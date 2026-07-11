import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { fetchRequests } from "@/store/thunks/requestThunks";
import { AppDispatch } from "@/store";

export const useRequestsData = () => {
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchRequests());
  }, [dispatch]);
};
