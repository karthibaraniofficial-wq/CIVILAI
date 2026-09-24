import React, { useState, useEffect } from 'react';
import { 
  Building2, AlertOctagon, CheckCircle2, Clock, Filter, 
  MapPin, UserCheck, ChevronRight, Activity, Sparkles, ShieldAlert 
} from 'lucide-react';
import { Complaint, DepartmentWorkload, ComplaintStatus, PriorityLevel } from '../../types';
import { 
  fetchComplaints, fetchDepartmentWorkloads, 
  updateComplaintStatus, fetchComplaintById 
} from '../../services/api';

export const OperationsBoard: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [workloads, setWorkloads] = useState<DepartmentWorkload[]>([]);
  const [selectedComplaint, setSelectedComplaint] = useState<Complaint | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [priorityFilter, setPriorityFilter] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [comps, wls] = await Promise.all([
        fetchComplaints({ status: statusFilter || undefined, priority: priorityFilter || undefined }),
        fetchDepartmentWorkloads(),
      ]);
      setComplaints(comps);
      setWorkloads(wls);
      if (comps.length > 0 && !selectedComplaint) {
        setSelectedComplaint(comps[0]);
      }
    } catch (e) {
      console.error('Failed to load operations data', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [statusFilter, priorityFilter]);

  const handleStatusChange = async (newStatus: ComplaintStatus) => {
    if (!selectedComplaint) return;
    try {
      const updated = await updateComplaintStatus(selectedComplaint.id, newStatus);
      setSelectedComplaint(updated);
      loadData();
    } catch (e) {
      alert('Failed to update status');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Workload Metric Counters */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Grievances</span>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">{complaints.length}</div>
            <span className="text-[11px] text-emerald-600 font-medium">Auto-dispatched via AI</span>
          </div>
          <div className="w-11 h-11 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
            <Building2 className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Critical Emergencies</span>
            <div className="text-2xl font-extrabold text-rose-600 mt-1">
              {complaints.filter(c => c.priority === 'CRITICAL').length}
            </div>
            <span className="text-[11px] text-rose-600 font-medium">4h Target SLA</span>
          </div>
          <div className="w-11 h-11 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
            <AlertOctagon className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Escalated Cases</span>
            <div className="text-2xl font-extrabold text-amber-600 mt-1">
              {complaints.filter(c => c.status === 'ESCALATED').length}
            </div>
            <span className="text-[11px] text-amber-600 font-medium">Notified to Zonal Officer</span>
          </div>
          <div className="w-11 h-11 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">SLA Compliance</span>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">94.8%</div>
            <span className="text-[11px] text-emerald-600 font-medium">+1.4% this week</span>
          </div>
          <div className="w-11 h-11 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <CheckCircle2 className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Main Split Layout: Triage List & Live Details */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Complaint Queue (7 cols) */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100">
            <div>
              <h2 className="text-base font-bold text-slate-900">Municipal Dispatch Queue</h2>
              <p className="text-xs text-slate-500">Autonomous multi-agent triaged citizen cases</p>
            </div>

            {/* Filter Pills */}
            <div className="flex items-center gap-2">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700"
              >
                <option value="">All Statuses</option>
                <option value="SUBMITTED">SUBMITTED</option>
                <option value="ASSIGNED">ASSIGNED</option>
                <option value="IN_PROGRESS">IN PROGRESS</option>
                <option value="ESCALATED">ESCALATED</option>
                <option value="RESOLVED">RESOLVED</option>
              </select>

              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700"
              >
                <option value="">All Priorities</option>
                <option value="CRITICAL">CRITICAL</option>
                <option value="HIGH">HIGH</option>
                <option value="MEDIUM">MEDIUM</option>
                <option value="LOW">LOW</option>
              </select>
            </div>
          </div>

          {/* Cards List */}
          <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1">
            {complaints.map((c) => (
              <div
                key={c.id}
                onClick={() => setSelectedComplaint(c)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  selectedComplaint?.id === c.id
                    ? 'border-blue-500 bg-blue-50/40 ring-2 ring-blue-500/10'
                    : 'border-slate-200 hover:border-slate-300 bg-white'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-blue-700">{c.tracking_number}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        c.priority === 'CRITICAL' ? 'bg-rose-100 text-rose-800' :
                        c.priority === 'HIGH' ? 'bg-amber-100 text-amber-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {c.priority}
                      </span>
                      <span className="text-[11px] text-slate-400 font-medium">
                        {c.ward_number || 'Ward 3'}
                      </span>
                    </div>
                    <h4 className="font-semibold text-slate-900 text-xs mt-1.5 line-clamp-1">{c.title}</h4>
                  </div>
                  <span className="text-[11px] font-bold px-2 py-1 bg-slate-100 text-slate-700 rounded-md">
                    {c.status}
                  </span>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500 mt-3 pt-2 border-t border-slate-100">
                  <span className="truncate max-w-[240px]">
                    🏢 {c.department_name || 'Roads & Infrastructure'}
                  </span>
                  <span className="font-mono text-slate-400">
                    {new Date(c.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Selected Complaint Operations Console (5 cols) */}
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm space-y-5">
          {selectedComplaint ? (
            <>
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-blue-600">
                    {selectedComplaint.tracking_number}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">
                    ID: {selectedComplaint.id.slice(0, 8)}...
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 text-base mt-1">{selectedComplaint.title}</h3>
                <p className="text-xs text-slate-600 mt-2 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
                  {selectedComplaint.description}
                </p>
              </div>

              {/* Photo Proof if present */}
              {selectedComplaint.media && selectedComplaint.media.length > 0 && (
                <div>
                  <span className="text-xs font-semibold text-slate-700 block mb-1.5">Submitted Evidence</span>
                  <img
                    src={selectedComplaint.media[0].media_url}
                    alt="Proof"
                    className="w-full h-44 object-cover rounded-xl border border-slate-200"
                  />
                  {selectedComplaint.media[0].caption && (
                    <p className="text-[11px] text-slate-500 mt-1 italic">{selectedComplaint.media[0].caption}</p>
                  )}
                </div>
              )}

              {/* AI Agent Triage Findings */}
              {selectedComplaint.analysis && (
                <div className="p-3.5 bg-indigo-50/70 border border-indigo-100 rounded-xl space-y-2 text-xs">
                  <div className="flex items-center justify-between text-indigo-950 font-semibold text-[11px]">
                    <span className="flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                      Agent Decision Rationale
                    </span>
                    <span className="font-bold text-indigo-700">
                      Conf: {Math.round((selectedComplaint.analysis.routing_confidence || 0.95) * 100)}%
                    </span>
                  </div>
                  <p className="text-indigo-900/80 text-[11px] leading-relaxed">
                    {selectedComplaint.analysis.routing_rationale}
                  </p>
                </div>
              )}

              {/* Operator Action Bar */}
              <div className="pt-3 border-t border-slate-100 space-y-2">
                <span className="text-xs font-semibold text-slate-700 block">Operator Workflow Actions</span>
                <div className="grid grid-cols-3 gap-2">
                  <button
                    onClick={() => handleStatusChange('ACKNOWLEDGED')}
                    className="py-2 px-3 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-lg text-xs font-semibold transition"
                  >
                    Acknowledge
                  </button>
                  <button
                    onClick={() => handleStatusChange('IN_PROGRESS')}
                    className="py-2 px-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-sm transition"
                  >
                    Dispatch Crew
                  </button>
                  <button
                    onClick={() => handleStatusChange('RESOLVED')}
                    className="py-2 px-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold shadow-sm transition"
                  >
                    Mark Resolved
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="p-8 text-center text-slate-400 text-xs">
              Select a grievance from the queue to view full multi-agent triage logs and take dispatch actions.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
