import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import type { User } from "../types/api";
import { fetchCurrentUser, login as loginRequest, logout as logoutRequest } from "../services/auth";
import { tokenStorage } from "../services/api";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient();
  const [hasToken, setHasToken] = useState(() => Boolean(tokenStorage.getAccessToken()));

  const { data: user, isLoading } = useQuery({
    queryKey: ["auth", "me"],
    queryFn: fetchCurrentUser,
    enabled: hasToken,
    retry: false,
  });

  useEffect(() => {
    if (!hasToken) {
      queryClient.removeQueries({ queryKey: ["auth", "me"] });
    }
  }, [hasToken, queryClient]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user: user ?? null,
      isLoading: hasToken && isLoading,
      isAuthenticated: Boolean(user),
      login: async (email: string, password: string) => {
        const authData = await loginRequest(email, password);
        setHasToken(true);
        queryClient.setQueryData(["auth", "me"], authData.user);
      },
      logout: async () => {
        await logoutRequest();
        setHasToken(false);
        queryClient.clear();
      },
    }),
    [user, hasToken, isLoading, queryClient],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
