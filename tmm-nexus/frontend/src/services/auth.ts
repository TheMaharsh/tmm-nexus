import type { ApiResponse, AuthData, User } from "../types/api";
import { api, tokenStorage } from "./api";

export async function login(email: string, password: string): Promise<AuthData> {
  const response = await api.post<ApiResponse<AuthData>>("/auth/login", {
    email,
    password,
  });

  if (!response.data.data) {
    throw new Error(response.data.message ?? "Login failed");
  }

  tokenStorage.setTokens(response.data.data.tokens);
  return response.data.data;
}

export async function logout(): Promise<void> {
  const refreshToken = tokenStorage.getRefreshToken();
  if (refreshToken) {
    try {
      await api.post("/auth/logout", { refresh_token: refreshToken });
    } catch {
      // Proceed with local logout even if server call fails
    }
  }
  tokenStorage.clear();
}

export async function fetchCurrentUser(): Promise<User> {
  const response = await api.get<ApiResponse<User>>("/auth/me");
  if (!response.data.data) {
    throw new Error(response.data.message ?? "Failed to fetch user");
  }
  return response.data.data;
}
