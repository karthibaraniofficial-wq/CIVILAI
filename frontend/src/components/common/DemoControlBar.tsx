import React from 'react';
import { Play, FastForward, RotateCcw, Sparkles, CheckCircle2, AlertOctagon } from 'lucide-react';
import { loadDemoScenario, accelerateSla, resetDemoState } from '../../services/api';

interface DemoControlBarProps {
  onRefreshData: () => void;
  activeComplaintId?: string;
  onSelectComplaint?: (trackingNumber: string) => void;
}

export const DemoControlBar: React.FC<DemoControlBarProps> = ({ 
  onRefreshData, 
  activeComplaintId,
  onSelectComplaint 
}) => {
  const [loading, setLoading] = React.useState(false);
  const [bannerMsg, setBannerMsg] = React.useState<string | null>(null);

  const showFeedback = (msg: string) => {
    setBannerMsg(msg);
    setTimeout(() => setBannerMsg(null), 4000);
  };

  const handleLoadScenario = async () => {
    try {
      setLoading(true);
      const res = await loadDemoScenario();
      showFeedback(`Loaded Canonical Scenario: ${res.scenario_code} (${res.complaint.tracking_number})`);
      onRefreshData();
      if (onSelectComplaint) {
        onSelectComplaint(res.complaint.tracking_number);
      }
    } catch (e: any) {
      showFeedback(`Failed to load scenario: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleAccelerateSla = async () => {
    const targetId = activeComplaintId || 'c1111111-1111-1111-1111-111111111111';
    try {
      setLoading(true);
      const res = await accelerateSla(targetId);
      showFeedback(`SLA Time Accelerated: Status -> ${res.health_status} (${res.action_taken})`);
      onRefreshData();
    } catch (e: any) {
      showFeedback(`Failed to accelerate SLA: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (!window.confirm('Reset platform data to clean baseline?')) return;
    try {
      setLoading(true);
      await resetDemoState();
      showFeedback('Platform state reset to initial seed baseline.');
      onRefreshData();
    } catch (e: any) {
      showFeedback(`Failed to reset: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 text-white text-xs border-b border-slate-800 py-2 px-4 shadow-inner">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        {/* Left: Indicator */}
        <div className="flex items-center gap-2">
          <div className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-400/30 flex items-center gap-1.5 font-mono text-[11px] font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            HACKATHON DEMO CONTROLLER
          </div>
          <span className="text-slate-400 hidden sm:inline">
            Zero-risk simulation harness for interactive judge demonstration
          </span>
        </div>

        {/* Center: Live feedback toast */}
        {bannerMsg && (
          <div className="flex items-center gap-1.5 px-3 py-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 animate-pulse text-[11px]">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>{bannerMsg}</span>
          </div>
        )}

        {/* Right: Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleLoadScenario}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded font-medium transition disabled:opacity-50"
            title="Load the hazardous school road pothole scenario"
          >
            <Play className="w-3 h-3 fill-current" />
            <span>Load Demo Case</span>
          </button>

          <button
            onClick={handleAccelerateSla}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1 bg-amber-600 hover:bg-amber-500 text-white rounded font-medium transition disabled:opacity-50"
            title="Advance simulated time to breach SLA and trigger Escalation Agent"
          >
            <FastForward className="w-3 h-3 fill-current" />
            <span>Accelerate SLA (Breach)</span>
          </button>

          <button
            onClick={handleReset}
            disabled={loading}
            className="flex items-center gap-1.5 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded border border-slate-700 transition disabled:opacity-50"
            title="Reset repository to initial seed data"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset</span>
          </button>
        </div>
      </div>
    </div>
  );
};
