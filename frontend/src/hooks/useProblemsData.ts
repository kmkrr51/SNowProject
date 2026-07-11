import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { fetchProblems } from "@/store/thunks/problemThunks";
import { AppDispatch } from "@/store";

export const useProblemsData = () => {
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchProblems());
  }, [dispatch]);
};
