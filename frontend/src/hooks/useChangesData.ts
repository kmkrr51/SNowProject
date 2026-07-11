import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { fetchChanges } from "@/store/thunks/changeThunks";
import { AppDispatch } from "@/store";

export const useChangesData = () => {
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchChanges());
  }, [dispatch]);
};
