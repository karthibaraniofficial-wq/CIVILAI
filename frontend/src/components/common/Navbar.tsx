import React from 'react';
import { 
  Building2, ShieldCheck, Activity, Search, 
  Sparkles, Compass, AlertTriangle, Layers, BarChart3, User 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { UserRole } from '../../types';

interface NavbarProps {
  currentTab: 'citizen' | 'municipal' | 'analytics' | 'admin';
  setCurrentTab: (tab: 'citizen' | 'municipal' | 'analytics' | 'admin') => void;
  onSearchTracking?: (tracking: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentTab, setCurrentTab, onSearchTracking }) => {
  const [searchInput, setSearchInput] = React.useState('');
  const { user, role, switchDemoRole } = useAuth();

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim() && onSearchTracking) {
      onSearchTracking(searchInput.trim());
      setCurrentTab('citizen');
    }
  };

  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-200/80 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 via-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
            <Building2 className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-slate-900 tracking-tight text-lg">CIVICFLOW</span>
              <span className="px-1.5 py-0.5 text-[10px] font-bold bg-blue-100 text-blue-800 rounded-md tracking-wider">AI ORCHESTRATOR</span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">National Civic Grievance Triage & SLA Engine</p>
          </div>
        </div>

        {/* Portal Switcher Tabs */}
        <nav className="flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200 text-sm font-medium text-slate-600">
          <button
            onClick={() => setCurrentTab('citizen')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              currentTab === 'citizen'
                ? 'bg-white text-blue-700 shadow-sm font-semibold'
                : 'hover:text-slate-900'
            }`}
          >
            <Compass className="w-4 h-4" />
            <span className="hidden sm:inline">Citizen Portal</span>
          </button>

          <button
            onClick={() => setCurrentTab('municipal')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              currentTab === 'municipal'
                ? 'bg-white text-blue-700 shadow-sm font-semibold'
                : 'hover:text-slate-900'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span className="hidden sm:inline">Operations Center</span>
          </button>

          <button
            onClick={() => setCurrentTab('analytics')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              currentTab === 'analytics'
                ? 'bg-white text-blue-700 shadow-sm font-semibold'
                : 'hover:text-slate-900'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span className="hidden sm:inline">Analytics</span>
          </button>

          <button
            onClick={() => setCurrentTab('admin')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg transition-all ${
              currentTab === 'admin'
                ? 'bg-white text-blue-700 shadow-sm font-semibold'
                : 'hover:text-slate-900'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span className="hidden sm:inline">Governance</span>
          </button>
        </nav>

        {/* Search, Persona Switcher & Live Status */}
        <div className="flex items-center gap-3">
          <form onSubmit={handleSearchSubmit} className="relative hidden xl:block">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Track CF-2026-..."
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              className="pl-9 pr-3 py-1.5 bg-white border border-slate-200 rounded-lg text-xs w-36 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
          </form>

          {/* Active Role Switcher Badge */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 border border-slate-200 text-xs">
            <User className="w-3.5 h-3.5 text-slate-500" />
            <select
              value={role}
              onChange={(e) => switchDemoRole(e.target.value as UserRole)}
              className="bg-transparent font-semibold text-slate-800 text-[11px] focus:outline-none cursor-pointer"
              title="Switch demo persona"
            >
              <option value="CITIZEN">Citizen</option>
              <option value="OPERATOR">Operator</option>
              <option value="SUPERVISOR">Supervisor</option>
              <option value="ADMIN">Commissioner</option>
            </select>
          </div>

          <div className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-emerald-50 border border-emerald-200/60 text-emerald-700 text-xs font-medium">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="hidden lg:inline text-[11px] font-semibold">6 Agents Live</span>
          </div>
        </div>
      </div>
    </header>
  );
};
