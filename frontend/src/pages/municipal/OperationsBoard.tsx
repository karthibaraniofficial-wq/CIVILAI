import React, { useState, useEffect } from 'react';
import { 
  Building2, AlertOctagon, CheckCircle2, Clock, Filter, 
  MapPin, UserCheck, ChevronRight, Activity, Sparkles, 
  ShieldAlert, Map as MapIcon, List, Eye, ShieldCheck 
} from 'lucide-react';
import { Complaint, DepartmentWorkload, ComplaintStatus, PriorityLevel, Escalation } from '../../types';
import { 
  fetchComplaints, fetchDepartmentWorkloads, 
  updateComplaintStatus, fetchComplaintById, fetchEscalations 
} from '../../services/api';
import { CivicMap } from '../../components/map/CivicMap';

export const OperationsBoard: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [workloads, setWorkloads] = useState<DepartmentWorkload[]>([]);
  const [escalations, setEscalations] = useState<Escalation[]>([]);
  const [selectedComplaint, setSelectedComplaint] = useState<Complaint | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [priorityFilter, setPriorityFilter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'split' | 'map' | 'list'>('split');
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [comps, wls, escs] = await Promise.all([
        fetchComplaints({ status: statusFilter || undefined, priority: priorityFilter || undefined }),
        fetchDepartmentWorkloads(),
        fetchEscalations(),
      ]);
      setComplaints(comps);
      setWorkloads(wls);
      setEscalations(escs);
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
            <span className="text-[11px] text-emerald-600 font-medium">Autonomous Triage Active</span>
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
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Statutory Escalations</span>
            <div className="text-2xl font-extrabold text-amber-600 mt-1">
              {escalations.length}
            </div>
            <span className="text-[11px] text-amber-600 font-medium">Zonal & Commissioner Tiers</span>
          </div>
          <div className="w-11 h-11 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">SLA Compliance</span>
            <div className="text-2xl font-extrabold text-slate-900 mt-1">94.8%</div>
            <span className="text-[11px] text-emerald-600 font-medium">Deterministic Engine</span>
          </div>
          <div className="w-11 h-11 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <CheckCircle2 className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* View Switcher & Filters Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm">
        <div className="flex items-center gap-2 bg-slate-100 p-1 rounded-xl text-xs font-medium text-slate-600">
          <button
            onClick={() => setViewMode('split')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              viewMode === 'split' ? 'bg-white text-blue-700 shadow-sm font-semibold' : 'hover:text-slate-900'
            }`}
          >
            <List className="w-3.5 h-3.5" />
            <span>Split Triage</span>
          </button>
          <button
            onClick={() => setViewMode('map')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition ${
              viewMode === 'map' ? 'bg-white text-blue-700 shadow-sm font-semibold' : 'hover:text-slate-900'
            }`}
          >
            <MapIcon className="w-3.5 h-3.5" />
            <span>Spatial Map Only</span>
          </button>
        </div>

        {/* Filter Dropdowns */}
        <div className="flex items-center gap-3">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700 focus:outline-none"
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
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700 focus:outline-none"
          >
            <option value="">All Priorities</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>
        </div>
      </div>

      {/* Map Section (if in map or split mode) */}
      {(viewMode === 'map' || viewMode === 'split') && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <MapIcon className="w-4 h-4 text-blue-600" />
              Spatial GIS Incident Heatmap & Live GPS Coordinates
            </h2>
            <span className="text-xs text-slate-500 font-mono">
              {complaints.length} Pinned Grievances
            </span>
          </div>
          <CivicMap
            complaints={complaints}
            selectedComplaint={selectedComplaint}
            onSelectComplaint={(c) => setSelectedComplaint(c)}
            height={viewMode === 'map' ? '560px' : '360px'}
          />
        </div>
      )}

      {/* Main Split Layout: Triage List & Live Details */}
      {viewMode !== 'map' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left: Complaint Queue (7 cols) */}
          <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h2 className="text-base font-bold text-slate-900">Municipal Dispatch Queue</h2>
              <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md">
                Live Feed
              </span>
            </div>

            {/* Cards List */}
            <div className="space-y-3 max-h-[620px] overflow-y-auto pr-1">
              {complaints.length === 0 ? (
                <div className="p-8 text-center text-slate-400 text-xs">
                  No grievances matching the selected filters.
                </div>
              ) : (
                complaints.map((c) => (
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
                ))
              )}
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
                        Multi-Agent Decision Rationale
                      </span>
                      <span className="font-bold text-indigo-700">
                        Sev: {selectedComplaint.analysis.visual_severity_score}/10
                      </span>
                    </div>
                    <p className="text-indigo-900/80 text-[11px] leading-relaxed">
                      {selectedComplaint.analysis.routing_rationale}
                    </p>
                    {selectedComplaint.analysis.detected_hazards?.length > 0 && (
                      <div className="flex flex-wrap gap-1 pt-1">
                        {selectedComplaint.analysis.detected_hazards.map((h, i) => (
                          <span key={i} className="px-2 py-0.5 bg-white border border-indigo-200 text-indigo-800 text-[10px] rounded font-medium">
                            ⚠ {h.replace(/_/g, ' ')}
                          </span>
                        ))}
                      </div>
                    )}
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
                Select a grievance from the queue or map to inspect autonomous agent findings and dispatch field personnel.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
