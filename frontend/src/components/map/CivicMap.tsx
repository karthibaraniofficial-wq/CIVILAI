import React, { useEffect, useRef } from 'react';
import { Complaint } from '../../types';
import L from 'leaflet';

interface CivicMapProps {
  complaints: Complaint[];
  selectedComplaint?: Complaint | null;
  onSelectComplaint?: (complaint: Complaint) => void;
  height?: string;
}

export const CivicMap: React.FC<CivicMapProps> = ({
  complaints,
  selectedComplaint,
  onSelectComplaint,
  height = '420px',
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersRef = useRef<L.Marker[]>([]);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      // Initialize map centered around default municipal coordinates (e.g. 28.6139, 77.2090)
      const map = L.map(mapContainerRef.current, {
        center: [28.6139, 77.2090],
        zoom: 13,
        zoomControl: true,
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;

    // Clear existing markers
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    // Helper for custom SVG colored pin
    const getMarkerIcon = (priority: string, isSelected: boolean) => {
      const color =
        priority === 'CRITICAL' ? '#e11d48' :
        priority === 'HIGH' ? '#d97706' :
        priority === 'MEDIUM' ? '#2563eb' : '#64748b';

      const size = isSelected ? 36 : 28;

      const svgHtml = `
        <div style="
          width: ${size}px; 
          height: ${size}px; 
          background-color: ${color}; 
          border: 2px solid #ffffff; 
          border-radius: 50% 50% 50% 0; 
          transform: rotate(-45deg); 
          box-shadow: 0 4px 10px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <div style="
            width: ${size / 2.8}px; 
            height: ${size / 2.8}px; 
            background: white; 
            border-radius: 50%;
          "></div>
        </div>
      `;

      return L.divIcon({
        className: 'custom-civic-marker',
        html: svgHtml,
        iconSize: [size, size],
        iconAnchor: [size / 2, size],
        popupAnchor: [0, -size],
      });
    };

    // Add markers
    complaints.forEach((c) => {
      if (c.latitude && c.longitude) {
        const isSelected = selectedComplaint?.id === c.id;
        const icon = getMarkerIcon(c.priority, isSelected);

        const marker = L.marker([c.latitude, c.longitude], { icon })
          .addTo(map)
          .bindPopup(`
            <div style="font-family: inherit; font-size: 12px; max-width: 220px;">
              <div style="font-weight: 700; color: #2563eb; font-family: monospace;">${c.tracking_number}</div>
              <div style="font-weight: 600; color: #0f172a; margin-top: 2px;">${c.title}</div>
              <div style="color: #64748b; font-size: 11px; margin-top: 4px;">📍 ${c.location_address}</div>
              <div style="margin-top: 6px; display: flex; gap: 4px;">
                <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-weight: 600; font-size: 10px;">${c.priority}</span>
                <span style="background: #eff6ff; color: #1e40af; padding: 2px 6px; border-radius: 4px; font-weight: 600; font-size: 10px;">${c.status}</span>
              </div>
            </div>
          `);

        marker.on('click', () => {
          if (onSelectComplaint) onSelectComplaint(c);
        });

        markersRef.current.push(marker);
      }
    });

    // Pan to selected complaint if present
    if (selectedComplaint && selectedComplaint.latitude && selectedComplaint.longitude) {
      map.setView([selectedComplaint.latitude, selectedComplaint.longitude], 14, {
        animate: true,
      });
    }

    return () => {
      // Map stays alive across renders
    };
  }, [complaints, selectedComplaint]);

  return (
    <div className="relative rounded-2xl overflow-hidden border border-slate-200 shadow-sm bg-slate-100">
      <div 
        ref={mapContainerRef} 
        style={{ height, width: '100%' }}
        className="z-10"
      />
      {/* Map Legend */}
      <div className="absolute bottom-3 left-3 z-20 bg-white/90 backdrop-blur-md px-3 py-2 rounded-xl border border-slate-200 shadow-md text-[11px] flex items-center gap-3">
        <span className="font-semibold text-slate-700">Priority:</span>
        <span className="flex items-center gap-1 font-medium text-rose-600">
          <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Critical
        </span>
        <span className="flex items-center gap-1 font-medium text-amber-600">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span> High
        </span>
        <span className="flex items-center gap-1 font-medium text-blue-600">
          <span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span> Medium
        </span>
        <span className="flex items-center gap-1 font-medium text-slate-500">
          <span className="w-2.5 h-2.5 rounded-full bg-slate-400 inline-block"></span> Low
        </span>
      </div>
    </div>
  );
};
