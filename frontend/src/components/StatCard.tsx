export function StatCard({ label, value, color }:
    { label: string; value: number | string; color: string }) {
    return (
        <div className={`bg-slate-900 rounded-lg p-4 border ${color}`}>
            <div className="text-3xl font-bold">{value}</div>
            <div className="text-slate-400 text-sm mt-1">{label}</div>
        </div>
    );
}