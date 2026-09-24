import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, Cpu, Database, Activity, FileSpreadsheet, 
  Clock, CheckCircle, AlertTriangle 
} from 'lucide-react';
import { AuditLog, Department } from '../../types';
import { fetchAuditLogs, fetchDepartments, fetchHealth } from '../../services/api';

export const AdminGovernance: React.FC = () => {
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [healthData, setHealthData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [logs, depts, health] = await Promise.all([
          fetchAuditLogs(),
          fetchDepartments(),
          fetchHealth(),
        ]);
        setAuditLogs(logs);
        setDepartments(depts);
        setHealthData(health);
      } catch (e) {
        console.error('Failed to load governance data', e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <ShieldCheck className="w-6 h-6 text-blue-600" />
          Municipal Governance & AI Agent Governance
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          System telemetry, multi-agent health matrix, SLA rules, and immutable compliance audit logs.
        </p>
      </div>

      {/* Agents Health Matrix */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <h2 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Cpu className="w-4 h-4 text-blue-600" />
          Autonomous Multi-Agent Fleet Status
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { name: 'Complaint Understanding Agent', role: 'NLP, Sentiment & Entity Parsing', model: 'gemini-3.8-flash', status: 'ACTIVE' },
            { name: 'Vision Analysis Agent', role: 'Proof Verification & Hazard Detection', model: 'gemini-3.8-flash', status: 'ACTIVE' },
            { name: 'Department Routing Agent', role: 'Jurisdictional Ward & Dept Matching', model: 'gemini-3.8-flash', status: 'ACTIVE' },
            { name: 'Priority & SLA Agent', role: 'Urgency Matrix & Dynamic SLA Calculation', model: 'gemini-3.8-flash', status: 'ACTIVE' },
            { name: 'Follow-up Agent', role: 'Continuous SLA Monitoring & Reminders', model: 'gemini-3.8-flash', status: 'ACTIVE' },
            { name: 'Escalation Agent', role: 'Administrative Breach Escalations', model: 'gemini-3.8-flash', status: 'ACTIVE' },
          ].map((agent, i) => (
            <div key={i} className="p-4 rounded-xl border border-slate-200 bg-slate-50/60 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-slate-900 text-xs">{agent.name}</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                  {agent.status}
                </span>
              </div>
              <p className="text-[11px] text-slate-500">{agent.role}</p>
              <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 pt-1 border-t border-slate-200">
                <span>Model: {agent.model}</span>
                <span>Latency: ~45ms</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* SLA Policy Standard Matrix */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <h2 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Clock className="w-4 h-4 text-blue-600" />
          Statutory SLA Resolution Policies
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-slate-600 font-semibold">
                <th className="py-2.5 px-3">Priority Tier</th>
                <th className="py-2.5 px-3">Standard Hazard Profile</th>
                <th className="py-2.5 px-3">Target SLA</th>
                <th className="py-2.5 px-3">Warning Alert Threshold</th>
                <th className="py-2.5 px-3">Escalation Authority</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr>
                <td className="py-2.5 px-3 font-bold text-rose-600">CRITICAL</td>
                <td className="py-2.5 px-3 text-slate-600">Live wires, major gas/water main burst, active collapse</td>
                <td className="py-2.5 px-3 font-semibold text-slate-900">4 Hours</td>
                <td className="py-2.5 px-3 text-slate-600">2 Hours (50%)</td>
                <td className="py-2.5 px-3 font-medium text-slate-800">Municipal Commissioner</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-bold text-amber-600">HIGH</td>
                <td className="py-2.5 px-3 text-slate-600">Deep road craters near schools, sewage overflow</td>
                <td className="py-2.5 px-3 font-semibold text-slate-900">24 Hours</td>
                <td className="py-2.5 px-3 text-slate-600">16 Hours (66%)</td>
                <td className="py-2.5 px-3 font-medium text-slate-800">Zonal Officer</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-bold text-blue-600">MEDIUM</td>
                <td className="py-2.5 px-3 text-slate-600">Garbage piles, localized drainage clogs</td>
                <td className="py-2.5 px-3 font-semibold text-slate-900">48 Hours</td>
                <td className="py-2.5 px-3 text-slate-600">32 Hours (66%)</td>
                <td className="py-2.5 px-3 font-medium text-slate-800">Ward Supervisor</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-bold text-slate-600">LOW</td>
                <td className="py-2.5 px-3 text-slate-600">Cosmetic damage, non-hazardous park pruning</td>
                <td className="py-2.5 px-3 font-semibold text-slate-900">96 Hours</td>
                <td className="py-2.5 px-3 text-slate-600">72 Hours (75%)</td>
                <td className="py-2.5 px-3 font-medium text-slate-800">Ward Desk Officer</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Immutable Audit Trail */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Database className="w-4 h-4 text-blue-600" />
              Immutable Compliance Audit Logs
            </h2>
            <p className="text-xs text-slate-500">Append-only audit ledger recording every citizen and agent state transition</p>
          </div>
          <span className="font-mono text-xs font-semibold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-md">
            {auditLogs.length} Records
          </span>
        </div>

        <div className="space-y-2 max-h-96 overflow-y-auto font-mono text-[11px]">
          {auditLogs.map((log) => (
            <div key={log.id} className="p-3 bg-slate-50 border border-slate-200/80 rounded-lg flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-3">
                <span className="font-bold text-blue-700 uppercase">{log.action}</span>
                <span className="text-slate-500">[{log.entity_type}]</span>
                <span className="text-slate-800">{log.notes || `Entity: ${log.entity_id.slice(0, 8)}...`}</span>
              </div>
              <div className="flex items-center gap-3 text-slate-400">
                <span>By: {log.actor_id || 'SYSTEM'}</span>
                <span>{new Date(log.created_at).toLocaleTimeString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
