import React, { useState, useEffect } from 'react';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/common/Navbar';
import { DemoControlBar } from './components/common/DemoControlBar';
import { CitizenPortal } from './pages/citizen/CitizenPortal';
import { OperationsBoard } from './pages/municipal/OperationsBoard';
import { AnalyticsDashboard } from './pages/analytics/AnalyticsDashboard';
import { AdminGovernance } from './pages/admin/AdminGovernance';

export const AppContent: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'citizen' | 'municipal' | 'analytics' | 'admin'>('citizen');
  const [activeTracking, setActiveTracking] = useState<string>('CF-2026-08912');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  const handleSelectComplaint = (tracking: string) => {
    setActiveTracking(tracking);
    setCurrentTab('citizen');
  };

  // Setup Server-Sent Events (SSE) for live platform updates (safeguarded for serverless)
  useEffect(() => {
    let eventSource: EventSource | null = null;
    try {
      if (typeof window !== 'undefined' && 'EventSource' in window) {
        eventSource = new EventSource('/api/v1/events/stream');
        eventSource.onmessage = (event) => {
          try {
            const payload = JSON.parse(event.data);
            handleRefresh();
          } catch (e) {
            // Ping or malformed payload
          }
        };
        eventSource.onerror = () => {
          // Gracefully close on serverless timeout to avoid reconnect loop
          eventSource?.close();
        };
      }
    } catch (e) {
      console.warn('Realtime SSE stream not active:', e);
    }

    return () => {
      try {
        eventSource?.close();
      } catch {}
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#f8fafc] text-slate-900 selection:bg-blue-600 selection:text-white">
      {/* Presentation Demo Bar */}
      <DemoControlBar 
        onRefreshData={handleRefresh} 
        onSelectComplaint={handleSelectComplaint}
      />

      {/* Main Header / Navigation */}
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        onSearchTracking={handleSelectComplaint}
      />

      {/* Main View Portals */}
      <main className="flex-1">
        {currentTab === 'citizen' && (
          <CitizenPortal key={refreshTrigger} initialTracking={activeTracking} />
        )}
        {currentTab === 'municipal' && (
          <OperationsBoard key={refreshTrigger} />
        )}
        {currentTab === 'analytics' && (
          <AnalyticsDashboard key={refreshTrigger} />
        )}
        {currentTab === 'admin' && (
          <AdminGovernance key={refreshTrigger} />
        )}
      </main>

      {/* SaaS Footer */}
      <footer className="border-t border-slate-200/80 bg-white py-6 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-slate-800 tracking-tight">CIVICFLOW AI</span>
            <span>— Community Grievance Resolution Orchestrator</span>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <span>National Hackathon 2026</span>
            <span>•</span>
            <span className="text-blue-600 font-semibold">6 Autonomous AI Agents</span>
            <span>•</span>
            <span className="text-emerald-600 font-medium">Deterministic SLA Engine Active</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;
