import authReducer, {
  setLoading,
  setError,
  setUser,
  logout,
} from "@/store/slices/authSlice";

describe("authSlice", () => {
  const initialState = {
    user: null,
    token: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  };

  it("should return the initial state", () => {
    expect(authReducer(undefined, { type: "unknown" })).toEqual(initialState);
  });

  it("should handle setLoading", () => {
    const actual = authReducer(initialState, setLoading(true));
    expect(actual.loading).toBe(true);
  });

  it("should handle setError", () => {
    const errorMessage = "Authentication failed";
    const actual = authReducer(initialState, setError(errorMessage));
    expect(actual.error).toBe(errorMessage);
  });

  it("should handle setUser", () => {
    const user = {
      id: "1",
      email: "test@example.com",
      name: "Test User",
      role: "ADMIN",
    };
    const actual = authReducer(initialState, setUser(user));
    expect(actual.user).toEqual(user);
    expect(actual.isAuthenticated).toBe(true);
  });

  it("should handle logout", () => {
    const stateWithUser = {
      ...initialState,
      user: { id: "1", email: "test@example.com", name: "Test", role: "ADMIN" },
      isAuthenticated: true,
      token: "token123",
    };
    const actual = authReducer(stateWithUser, logout());
    expect(actual.user).toBeNull();
    expect(actual.token).toBeNull();
    expect(actual.isAuthenticated).toBe(false);
  });

  it("should clear error when setting user", () => {
    const stateWithError = {
      ...initialState,
      error: "Previous error",
    };
    const user = {
      id: "1",
      email: "test@example.com",
      name: "Test User",
      role: "ADMIN",
    };
    const actual = authReducer(stateWithError, setUser(user));
    expect(actual.error).toBeNull();
  });
});
