import React, { useState, useEffect } from 'react';
import { Navbar } from './components/common/Navbar';
import { DemoControlBar } from './components/common/DemoControlBar';
import { CitizenPortal } from './pages/citizen/CitizenPortal';
import { OperationsBoard } from './pages/municipal/OperationsBoard';
import { AdminGovernance } from './pages/admin/AdminGovernance';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<'citizen' | 'municipal' | 'admin'>('citizen');
  const [activeTracking, setActiveTracking] = useState<string>('CF-2026-08912');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  const handleSelectComplaint = (tracking: string) => {
    setActiveTracking(tracking);
    setCurrentTab('citizen');
  };

  // Setup Server-Sent Events (SSE) for live agent activity updates
  useEffect(() => {
    const eventSource = new EventSource('/api/v1/events/stream');

    eventSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        console.log('Realtime Event Received:', payload);
        handleRefresh();
      } catch (e) {
        // Ping or malformed payload
      }
    };

    eventSource.onerror = () => {
      // EventSource reconnects automatically
    };

    return () => {
      eventSource.close();
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
        {currentTab === 'admin' && (
          <AdminGovernance key={refreshTrigger} />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200/80 bg-white py-6 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-slate-700">CIVICFLOW AI</span>
            <span>— Autonomous Community Grievance Resolution Orchestrator</span>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <span>National Hackathon 2026</span>
            <span>•</span>
            <span>6-Agent AI Architecture</span>
            <span>•</span>
            <span className="text-emerald-600 font-medium">System Operational</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
