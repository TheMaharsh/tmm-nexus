interface StatCardProps {
  label: string;
  value: number;
  accent?: string;
}

export function StatCard({ label, value, accent = "text-brand-red" }: StatCardProps) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-gray-500">{label}</p>
      <p className={`mt-2 text-3xl font-semibold tracking-tight ${accent}`}>{value.toLocaleString()}</p>
    </div>
  );
}
