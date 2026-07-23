import type { ApiResponse, DashboardStats } from "../types/api";
import { api } from "./api";

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const response = await api.get<ApiResponse<DashboardStats>>("/dashboard/stats");
  if (!response.data.data) {
    throw new Error(response.data.message ?? "Failed to fetch dashboard stats");
  }
  return response.data.data;
}
