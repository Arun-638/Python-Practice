import React, { useState, useEffect } from 'react';

const GaugeRing = ({ value, label, color = 'var(--cyan)', size = 56 }) => {
  const r = (size - 8) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;

  return (
    <div className="hud-gauge">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="3" />
        <circle
          cx={size/2} cy={size/2} r={r}
          fill="none"
          stroke={color}
          strokeWidth="3"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size/2} ${size/2})`}
          style={{ transition: 'stroke-dashoffset 1s ease', filter: `drop-shadow(0 0 4px ${color})` }}
        />
      </svg>
      <div className="hud-gauge-inner">
        <span className="hud-gauge-value" style={{ color }}>{value}%</span>
        <span className="hud-gauge-label">{label}</span>
      </div>
    </div>
  );
};

const ThreatBar = ({ level = 'LOW' }) => {
  const levels = ['LOW', 'MED', 'HIGH', 'CRIT'];
  const activeIdx = levels.indexOf(level);
  const colors = ['#34d399', '#fbbf24', '#f97316', '#ef4444'];

  return (
    <div className="hud-threat">
      <span className="hud-stat-label">THREAT ASSESSMENT</span>
      <div className="hud-threat-bars">
        {levels.map((l, i) => (
          <div key={l} className="hud-threat-segment">
            <div
              className={`hud-threat-fill ${i <= activeIdx ? 'active' : ''}`}
              style={{ background: i <= activeIdx ? colors[i] : 'rgba(255,255,255,0.06)' }}
            />
            <span className="hud-threat-label" style={{ color: i <= activeIdx ? colors[i] : 'rgba(255,255,255,0.15)' }}>{l}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const SkillsPanel = ({ skills, systemStats, weatherData }) => {
  const [uptime, setUptime] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setUptime(u => u + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const fmtUptime = (s) => {
    const h = String(Math.floor(s / 3600)).padStart(2, '0');
    const m = String(Math.floor((s % 3600) / 60)).padStart(2, '0');
    const sec = String(s % 60).padStart(2, '0');
    return `${h}:${m}:${sec}`;
  };

  const cpu = systemStats?.cpu ?? 12;
  const ram = systemStats?.ram ?? 48;
  const weatherStr = weatherData || '32°C · Partly Cloudy · Kochi';

  const activeSkills = skills && skills.length > 0 ? skills : [
    'time_date', 'system_info', 'open_app', 'web_search'
  ];

  return (
    <div className="flex flex-col gap-3 h-full">

      {/* Atmospherics Panel */}
      <div className="hud-panel" style={{ flex: '0 0 auto' }}>
        <div className="hud-panel-header">
          <div className="hud-panel-header-bar" />
          <div className="hud-panel-header-content">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--cyan)" strokeWidth="1.5">
              <path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
              <circle cx="12" cy="12" r="4" />
            </svg>
            <span className="hud-panel-title">ATMOSPHERICS</span>
          </div>
          <div className="hud-panel-header-bar" />
        </div>
        <div className="px-3 pb-3">
          <div className="hud-readout-row">
            <span className="hud-readout-key">ENV</span>
            <span className="hud-readout-val">{weatherStr}</span>
          </div>
        </div>
      </div>

      {/* System Diagnostics Main Panel */}
      <div className="hud-panel flex-1 flex flex-col overflow-hidden">
        <div className="hud-panel-header">
          <div className="hud-panel-header-bar" />
          <div className="hud-panel-header-content">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--cyan)" strokeWidth="1.5">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
            <span className="hud-panel-title">SYSTEM DIAGNOSTICS</span>
            <span className="hud-panel-tag">REAL-TIME</span>
          </div>
          <div className="hud-panel-header-bar" />
        </div>

        <div className="flex-1 overflow-y-auto px-3 pb-3">
          {/* Gauge Row */}
          <div className="flex justify-center gap-6 py-3">
            <GaugeRing value={cpu} label="CPU" color={cpu > 80 ? '#ef4444' : cpu > 50 ? '#fbbf24' : 'var(--cyan)'} />
            <GaugeRing value={ram} label="RAM" color={ram > 80 ? '#ef4444' : ram > 50 ? '#fbbf24' : '#60a5fa'} />
          </div>

          {/* Stats Readouts */}
          <div className="hud-readout-grid">
            <div className="hud-readout-row">
              <span className="hud-readout-key">UPTIME</span>
              <span className="hud-readout-val hud-readout-mono">{fmtUptime(uptime)}</span>
            </div>
            <div className="hud-readout-row">
              <span className="hud-readout-key">SHIELDS</span>
              <span className="hud-readout-val" style={{ color: '#34d399' }}>● ACTIVE</span>
            </div>
            <div className="hud-readout-row">
              <span className="hud-readout-key">LATENCY</span>
              <span className="hud-readout-val hud-readout-mono">4ms</span>
            </div>
            <div className="hud-readout-row">
              <span className="hud-readout-key">POWER</span>
              <span className="hud-readout-val hud-readout-mono">3.2 GW</span>
            </div>
          </div>

          {/* Threat Assessment */}
          <ThreatBar level="LOW" />

          {/* Active Skills */}
          <div className="mt-3">
            <div className="hud-sub-header">
              <span className="hud-sub-title">LOADED MODULES</span>
              <span className="hud-sub-count">{activeSkills.length}</span>
            </div>
            <div className="hud-skill-grid">
              {activeSkills.map(s => (
                <div key={s} className="hud-skill-item">
                  <span className="hud-skill-dot" />
                  <span className="hud-skill-name">{s.replace(/_/g, ' ')}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Upcoming */}
          <div className="mt-3">
            <div className="hud-sub-header">
              <span className="hud-sub-title">SCHEDULE</span>
            </div>
            <div className="hud-schedule-item">
              <div className="hud-schedule-time">14:00</div>
              <div className="hud-schedule-detail">
                <div className="hud-schedule-name">Project Sync</div>
                <div className="hud-schedule-loc">Lab 4 · Conference</div>
              </div>
            </div>
          </div>
        </div>

        <div className="hud-panel-footer">
          <span>DIAG: NOMINAL</span>
          <span className="hud-panel-footer-blink">▐</span>
        </div>
      </div>
    </div>
  );
};

export default SkillsPanel;
