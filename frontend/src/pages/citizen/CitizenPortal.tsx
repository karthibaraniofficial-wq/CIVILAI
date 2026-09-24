import React, { useState, useEffect } from 'react';
import { 
  Send, Camera, MapPin, CheckCircle, Clock, AlertTriangle, 
  Search, Shield, FileText, Sparkles, ArrowRight, UserCheck 
} from 'lucide-react';
import { Complaint, ComplaintEvent } from '../../types';
import { createComplaint, trackComplaint, fetchComplaintEvents } from '../../services/api';

interface CitizenPortalProps {
  initialTracking?: string;
}

export const CitizenPortal: React.FC<CitizenPortalProps> = ({ initialTracking }) => {
  // Form State
  const [citizenName, setCitizenName] = useState('Ananya Verma');
  const [citizenContact, setCitizenContact] = useState('+91-98101-23456');
  const [title, setTitle] = useState('Severe water leakage and road collapse near Central Market');
  const [description, setDescription] = useState('Main distribution pipe burst this afternoon causing continuous high-pressure flooding. The road surface has collapsed creating a large sinkhole approximately 1.5m deep near shop #14.');
  const [category, setCategory] = useState('water_supply');
  const [address, setAddress] = useState('Shop 14, Main Central Market Road, Ward 3');
  const [landmark, setLandmark] = useState('Near Central Bank ATM');
  const [lat, setLat] = useState(28.6185);
  const [lng, setLng] = useState(77.2120);
  const [photoUrl, setPhotoUrl] = useState('https://images.unsplash.com/photo-1541888946425-d0fbb1861564?auto=format&fit=crop&w=1000&q=80');

  // Tracking State
  const [trackingInput, setTrackingInput] = useState(initialTracking || 'CF-2026-08912');
  const [activeGrievance, setActiveGrievance] = useState<Complaint | null>(null);
  const [events, setEvents] = useState<ComplaintEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    if (initialTracking) {
      setTrackingInput(initialTracking);
      handleTrack(initialTracking);
    } else {
      handleTrack('CF-2026-08912');
    }
  }, [initialTracking]);

  const handleTrack = async (trackingNo?: string) => {
    const target = (trackingNo || trackingInput).trim();
    if (!target) return;
    setLoading(true);
    setErrorMsg(null);
    try {
      const c = await trackComplaint(target);
      setActiveGrievance(c);
      const evs = await fetchComplaintEvents(c.id);
      setEvents(evs);
    } catch (e: any) {
      setErrorMsg(e.message || 'Grievance not found');
      setActiveGrievance(null);
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setErrorMsg(null);
    setSuccessMsg(null);
    try {
      const created = await createComplaint({
        citizen_name: citizenName,
        citizen_contact: citizenContact,
        title,
        description,
        raw_category: category,
        location_address: address,
        landmark,
        latitude: lat,
        longitude: lng,
        media_urls: photoUrl ? [photoUrl] : [],
      });
      setSuccessMsg(`Grievance lodged! Tracking Code: ${created.tracking_number}. Autonomous triage agents activated.`);
      setTrackingInput(created.tracking_number);
      // Wait a moment for background agents to run and track it
      setTimeout(() => handleTrack(created.tracking_number), 1200);
    } catch (err: any) {
      setErrorMsg(err.message || 'Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Hero Banner */}
      <div className="relative rounded-2xl bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-8 overflow-hidden shadow-xl">
        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-semibold border border-blue-400/30">
            <Sparkles className="w-3.5 h-3.5" />
            AI-POWERED CIVIC TRIAGE & DISPATCH
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl text-white">
            Report Civic Issues. <br className="hidden sm:inline" />
            <span className="text-blue-300">Resolved Autonomously with SLA Guarantees.</span>
          </h1>
          <p className="text-sm text-slate-300">
            Submit road craters, sanitation dumps, pipe bursts, or electrical hazards. 
            Our 6-agent AI engine verifies proof, routes directly to municipal field units, and enforces strict SLA resolution deadlines.
          </p>
        </div>
      </div>

      {/* Grid: Submit Form & Tracking View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Complaint Submission Wizard (7 cols) */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-sm">
          <div className="flex items-center justify-between pb-5 border-b border-slate-100">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <FileText className="w-5 h-5 text-blue-600" />
                Lodge Grievance
              </h2>
              <p className="text-xs text-slate-500">Provide details and photo evidence for autonomous agent triage</p>
            </div>
            <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md">
              Ward 3 / Delhi NCR
            </span>
          </div>

          {successMsg && (
            <div className="mt-4 p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>{successMsg}</span>
            </div>
          )}

          {errorMsg && (
            <div className="mt-4 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Your Full Name</label>
                <input
                  type="text"
                  required
                  value={citizenName}
                  onChange={(e) => setCitizenName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Contact Phone</label>
                <input
                  type="text"
                  required
                  value={citizenContact}
                  onChange={(e) => setCitizenContact(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Issue Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
              >
                <option value="pothole">Road Crater / Pothole / Footpath Damage</option>
                <option value="garbage">Sanitation / Garbage Dump / Bio-waste</option>
                <option value="water_supply">Drinking Water Supply / Pipeline Leak</option>
                <option value="drainage">Drainage Overflow / Sewage Clog</option>
                <option value="streetlights">Streetlight Dark / Malfunction</option>
                <option value="electricity">Live Electrical Wire / Sparking Transformer</option>
                <option value="park">Fallen Tree Branch / Park Maintenance</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Grievance Title</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Comprehensive Description</label>
              <textarea
                rows={3}
                required
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Location Address / Street</label>
                <input
                  type="text"
                  required
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Nearest Landmark</label>
                <input
                  type="text"
                  value={landmark}
                  onChange={(e) => setLandmark(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1 flex items-center justify-between">
                <span>Visual Evidence Photo URL</span>
                <span className="text-[11px] font-normal text-slate-400">Processed by Vision Analysis Agent</span>
              </label>
              <div className="flex gap-2">
                <input
                  type="url"
                  value={photoUrl}
                  onChange={(e) => setPhotoUrl(e.target.value)}
                  placeholder="https://..."
                  className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                />
                {photoUrl && (
                  <img 
                    src={photoUrl} 
                    alt="Preview" 
                    className="w-9 h-9 rounded-lg object-cover border border-slate-200" 
                  />
                )}
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold text-xs shadow-md shadow-blue-500/20 transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {submitting ? (
                <span>Autonomous Agents Ingesting...</span>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Submit & Trigger Multi-Agent Triage</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Column: Grievance Tracker & Timeline (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          {/* Tracker Input Box */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
            <h2 className="text-sm font-bold text-slate-900 mb-2 flex items-center gap-2">
              <Search className="w-4 h-4 text-blue-600" />
              Live Grievance Tracking
            </h2>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Enter CF-2026-..."
                value={trackingInput}
                onChange={(e) => setTrackingInput(e.target.value)}
                className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs uppercase font-mono tracking-wider focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
              />
              <button
                onClick={() => handleTrack()}
                disabled={loading}
                className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold transition"
              >
                {loading ? 'Fetching...' : 'Track'}
              </button>
            </div>
          </div>

          {/* Active Grievance Card */}
          {activeGrievance ? (
            <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm space-y-4">
              <div className="flex items-start justify-between gap-2 border-b border-slate-100 pb-3">
                <div>
                  <div className="font-mono text-xs font-bold text-blue-600">{activeGrievance.tracking_number}</div>
                  <h3 className="font-semibold text-slate-900 text-sm mt-0.5">{activeGrievance.title}</h3>
                </div>
                <span className={`px-2.5 py-1 rounded-full text-[11px] font-bold ${
                  activeGrievance.priority === 'CRITICAL' ? 'bg-rose-100 text-rose-800' :
                  activeGrievance.priority === 'HIGH' ? 'bg-amber-100 text-amber-800' :
                  'bg-blue-100 text-blue-800'
                }`}>
                  {activeGrievance.priority}
                </span>
              </div>

              {/* Status and Department */}
              <div className="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-xl text-xs">
                <div>
                  <span className="text-slate-500 block text-[11px]">Current Status</span>
                  <span className="font-bold text-slate-800">{activeGrievance.status}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[11px]">Dispatched Dept</span>
                  <span className="font-bold text-slate-800 truncate block">
                    {activeGrievance.department_name || 'Triage In Progress'}
                  </span>
                </div>
              </div>

              {/* AI Agent Structured Insights */}
              {activeGrievance.analysis && (
                <div className="p-3.5 bg-blue-50/70 border border-blue-100 rounded-xl space-y-2 text-xs">
                  <div className="flex items-center justify-between text-blue-900 font-semibold text-[11px]">
                    <span className="flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                      Multi-Agent Analysis Verified
                    </span>
                    <span className="font-mono font-bold">
                      Sev: {activeGrievance.analysis.visual_severity_score}/10
                    </span>
                  </div>
                  <p className="text-slate-600 text-[11px] leading-relaxed">
                    {activeGrievance.analysis.routing_rationale}
                  </p>
                  {activeGrievance.analysis.detected_hazards?.length > 0 && (
                    <div className="flex flex-wrap gap-1 pt-1">
                      {activeGrievance.analysis.detected_hazards.map((h, i) => (
                        <span key={i} className="px-2 py-0.5 bg-white border border-blue-200 text-blue-800 text-[10px] rounded font-medium">
                          ⚠ {h.replace(/_/g, ' ')}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Timeline Events */}
              <div>
                <h4 className="text-xs font-bold text-slate-900 mb-3 flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-slate-500" />
                  Resolution Lifecycle Timeline
                </h4>
                <div className="space-y-3 pl-2 border-l-2 border-blue-200">
                  {events.map((ev) => (
                    <div key={ev.id} className="relative pl-4 text-xs">
                      <div className="absolute -left-[13px] top-1 w-2.5 h-2.5 rounded-full bg-blue-600 ring-4 ring-white" />
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-900">{ev.title}</span>
                        <span className="text-[10px] text-slate-400 font-mono">
                          {new Date(ev.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <p className="text-slate-500 text-[11px] mt-0.5">{ev.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center bg-white rounded-2xl border border-slate-200 text-slate-400 text-xs">
              No grievance selected. Enter tracking number or submit a new grievance above.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
