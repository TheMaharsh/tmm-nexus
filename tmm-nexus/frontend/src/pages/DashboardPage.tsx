import { useQuery } from "@tanstack/react-query";
import { StatCard } from "../components/StatCard";
import { useAuth } from "../hooks/useAuth";
import { fetchDashboardStats } from "../services/dashboard";

export function DashboardPage() {
  const { user } = useAuth();
  const { data: stats, isLoading } = useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: fetchDashboardStats,
  });

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-gray-900">
          Welcome back, {user?.first_name}
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          {user?.organization_name} · Lead Engine overview
        </p>
      </div>

      {isLoading ? (
        <p className="text-sm text-gray-500">Loading dashboard...</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StatCard label="Total Leads" value={stats?.total_leads ?? 0} />
          <StatCard label="New Leads" value={stats?.new_leads ?? 0} />
          <StatCard label="Qualified" value={stats?.qualified_leads ?? 0} />
          <StatCard label="Contacted" value={stats?.contacted_leads ?? 0} />
          <StatCard label="Won" value={stats?.won_leads ?? 0} />
          <StatCard label="Recent Searches" value={stats?.recent_searches ?? 0} />
        </div>
      )}
    </div>
  );
}
