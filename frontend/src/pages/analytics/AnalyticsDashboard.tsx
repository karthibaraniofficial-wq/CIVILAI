import React, { useState, useEffect } from 'react';
import { 
  BarChart3, PieChart, TrendingUp, AlertTriangle, 
  CheckCircle2, Clock, Filter, MapPin, Building2 
} from 'lucide-react';

interface AnalyticsData {
  total_complaints: number;
  active_complaints: number;
  resolved_complaints: number;
  escalated_complaints: number;
  sla_compliance_rate: number;
  escalation_rate: number;
  average_resolution_hours: number;
  category_distribution: Record<string, number>;
  priority_distribution: Record<string, number>;
  department_workload: Array<{
    department_id: string;
    department_code: string;
    department_name: string;
    total: number;
    active: number;
    critical: number;
  }>;
  geographic_density: Record<string, number>;
  complaints_over_time: Array<{ date: string; count: number }>;
}

export const AnalyticsDashboard: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const query = new URLSearchParams();
      if (startDate) query.set('start_date', startDate);
      if (endDate) query.set('end_date', endDate);
      const res = await fetch(`/api/v1/analytics?${query.toString()}`);
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (e) {
      console.error('Failed to fetch analytics', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, [startDate, endDate]);

  if (loading && !data) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-xs text-slate-400">
        Aggregating operational analytics from municipal database...
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Header with Date Filter */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-blue-600" />
            Civic Performance & Intelligence Analytics
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time telemetry, SLA resolution trends, and jurisdictional ward density computed from live database records.
          </p>
        </div>

        {/* Date Filter Controls */}
        <div className="flex items-center gap-2 text-xs">
          <Filter className="w-4 h-4 text-slate-400" />
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-xs text-slate-700"
          />
          <span className="text-slate-400">to</span>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-xs text-slate-700"
          />
          {(startDate || endDate) && (
            <button
              onClick={() => { setStartDate(''); setEndDate(''); }}
              className="text-[11px] text-blue-600 font-semibold hover:underline"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Top KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>SLA Compliance Rate</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-2">
            {data.sla_compliance_rate}%
          </div>
          <div className="w-full bg-slate-100 rounded-full h-1.5 mt-3 overflow-hidden">
            <div 
              className="bg-emerald-500 h-1.5 rounded-full" 
              style={{ width: `${data.sla_compliance_rate}%` }}
            />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>Avg. Resolution Time</span>
            <Clock className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-2">
            {data.average_resolution_hours} hrs
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">From grievance submission to field sign-off</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>Escalation Rate</span>
            <AlertTriangle className="w-4 h-4 text-amber-600" />
          </div>
          <div className="text-2xl font-extrabold text-amber-600 mt-2">
            {data.escalation_rate}%
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">
            {data.escalated_complaints} statutory breaches escalated
          </span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>Total Ingested Grievances</span>
            <TrendingUp className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-2xl font-extrabold text-slate-900 mt-2">
            {data.total_complaints}
          </div>
          <span className="text-[11px] text-emerald-600 mt-1 block font-medium">
            {data.resolved_complaints} successfully closed
          </span>
        </div>
      </div>

      {/* Middle Grid: Category Breakdown & Priority Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Category Breakdown (7 cols) */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <PieChart className="w-4 h-4 text-blue-600" />
            Grievance Category Distribution
          </h2>
          <div className="space-y-3 pt-2">
            {Object.entries(data.category_distribution).map(([cat, count]) => {
              const pct = data.total_complaints > 0 ? Math.round((count / data.total_complaints) * 100) : 0;
              return (
                <div key={cat} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-800 capitalize">{cat.replace(/_/g, ' ')}</span>
                    <span className="text-slate-500 font-mono">{count} ({pct}%)</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-500" 
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Priority Distribution & Geographic Density (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          {/* Priority Tiers */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <h2 className="text-sm font-bold text-slate-900">Priority Tier Allocation</h2>
            <div className="grid grid-cols-2 gap-3 text-xs">
              {['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((p) => {
                const count = data.priority_distribution[p] || 0;
                const badgeColor =
                  p === 'CRITICAL' ? 'bg-rose-50 border-rose-200 text-rose-800' :
                  p === 'HIGH' ? 'bg-amber-50 border-amber-200 text-amber-800' :
                  p === 'MEDIUM' ? 'bg-blue-50 border-blue-200 text-blue-800' :
                  'bg-slate-50 border-slate-200 text-slate-800';
                return (
                  <div key={p} className={`p-3 rounded-xl border ${badgeColor}`}>
                    <span className="font-bold block text-[11px]">{p}</span>
                    <div className="text-xl font-extrabold mt-1">{count}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Geographic Density by Ward */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
            <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-blue-600" />
              Geographic Ward Concentration
            </h2>
            <div className="space-y-2 text-xs">
              {Object.entries(data.geographic_density).map(([ward, count]) => (
                <div key={ward} className="flex items-center justify-between p-2 rounded-lg bg-slate-50">
                  <span className="font-medium text-slate-700">{ward}</span>
                  <span className="font-bold text-slate-900 font-mono">{count} cases</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Department Workload Table */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <Building2 className="w-4 h-4 text-blue-600" />
          Municipal Department Workloads & Critical Load
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-slate-600 font-semibold">
                <th className="py-2.5 px-3">Department</th>
                <th className="py-2.5 px-3">Code</th>
                <th className="py-2.5 px-3">Total Assigned</th>
                <th className="py-2.5 px-3">Active In-Progress</th>
                <th className="py-2.5 px-3">Critical Cases</th>
                <th className="py-2.5 px-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {data.department_workload.map((dept) => (
                <tr key={dept.department_id} className="hover:bg-slate-50/50">
                  <td className="py-3 px-3 font-semibold text-slate-900">{dept.department_name}</td>
                  <td className="py-3 px-3 font-mono text-slate-500">{dept.department_code}</td>
                  <td className="py-3 px-3 font-bold text-slate-900">{dept.total}</td>
                  <td className="py-3 px-3 font-medium text-blue-600">{dept.active}</td>
                  <td className="py-3 px-3 font-bold text-rose-600">{dept.critical}</td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                      OPERATIONAL
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
