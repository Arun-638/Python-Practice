import React, { useState, useEffect, useRef, useMemo } from 'react';

const BOOT_SEQUENCE = [
  { type: 'sys',  text: 'BOOT SEQUENCE INITIATED' },
  { type: 'ok',   text: 'Kernel image loaded ............... OK' },
  { type: 'ok',   text: 'Memory buffer initialized ......... OK' },
  { type: 'ok',   text: 'Neural network core ............... OK' },
  { type: 'ok',   text: 'Gemini language model ............. OK' },
  { type: 'ok',   text: 'Skill manager registry ............ OK' },
  { type: 'info', text: 'Holographic HUD subsystem rendered' },
  { type: 'info', text: 'Network stack → IPv6 tunnel open' },
  { type: 'warn', text: 'Latency spike detected on Node-7 (12ms)' },
  { type: 'ok',   text: 'Neural-Link handshake ............. OK' },
  { type: 'ok',   text: 'WhatsApp hook daemon started' },
  { type: 'sys',  text: 'ALL SYSTEMS NOMINAL' },
];

const SystemLogs = ({ events }) => {
  const bottomRef = useRef(null);
  const [logs, setLogs] = useState([]);
  const bootDoneRef = useRef(false);
  const prevLenRef = useRef(0);
  const lineCounter = useRef(0);

  // Boot sequence typewriter effect
  useEffect(() => {
    if (bootDoneRef.current) return;
    bootDoneRef.current = true;
    let i = 0;
    const id = setInterval(() => {
      if (i < BOOT_SEQUENCE.length) {
        const entry = BOOT_SEQUENCE[i];
        lineCounter.current++;
        i++;
        setLogs(prev => [...prev, {
          line: lineCounter.current,
          type: entry.type,
          text: entry.text,
          time: performance.now(),
        }]);
      } else {
        clearInterval(id);
      }
    }, 200);
    return () => clearInterval(id);
  }, []); // eslint-disable-line

  // Live event feed from chat
  useEffect(() => {
    if (!Array.isArray(events) || events.length === 0) return;
    if (events.length <= prevLenRef.current) return;
    prevLenRef.current = events.length;
    const latest = events[events.length - 1];
    if (!latest || typeof latest !== 'object') return;
    const role = latest.role || 'system';
    const content = typeof latest.content === 'string' ? latest.content : '';
    const preview = content.length > 48 ? content.slice(0, 48) + '…' : content;
    if (!preview) return;
    lineCounter.current++;
    setLogs(prev => [...prev, {
      line: lineCounter.current,
      type: role === 'user' ? 'input' : 'output',
      text: `${role === 'user' ? 'USR' : 'AI '} :: ${preview}`,
      time: performance.now(),
    }]);
  }, [events]); // eslint-disable-line

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const getTypeColor = (type) => {
    switch (type) {
      case 'ok':     return 'var(--cyan)';
      case 'warn':   return '#fbbf24';
      case 'error':  return '#ef4444';
      case 'sys':    return '#a78bfa';
      case 'input':  return '#60a5fa';
      case 'output': return 'var(--cyan)';
      default:       return 'rgba(148, 163, 184, 0.5)';
    }
  };

  const getPrefix = (type) => {
    switch (type) {
      case 'ok':     return '✓';
      case 'warn':   return '⚠';
      case 'error':  return '✗';
      case 'sys':    return '»';
      case 'input':  return '▸';
      case 'output': return '◂';
      default:       return '·';
    }
  };

  return (
    <div className="hud-panel h-full flex flex-col">
      {/* Panel Header */}
      <div className="hud-panel-header">
        <div className="hud-panel-header-bar" />
        <div className="hud-panel-header-content">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--cyan)" strokeWidth="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <path d="M3 9h18M9 21V9" />
          </svg>
          <span className="hud-panel-title">DIAGNOSTIC FEED</span>
          <span className="hud-panel-tag">LIVE</span>
        </div>
        <div className="hud-panel-header-bar" />
      </div>

      {/* Log Entries */}
      <div className="hud-log-container">
        {logs.map((log, i) => (
          <div
            key={i}
            className="hud-log-entry"
            style={{ '--entry-color': getTypeColor(log.type) }}
          >
            <span className="hud-log-line">{String(log.line).padStart(3, '0')}</span>
            <span className="hud-log-prefix" style={{ color: getTypeColor(log.type) }}>{getPrefix(log.type)}</span>
            <span className="hud-log-text" style={{
              color: log.type === 'sys' ? '#a78bfa' : undefined,
              fontWeight: log.type === 'sys' ? 700 : undefined,
            }}>
              {log.text}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Panel Footer */}
      <div className="hud-panel-footer">
        <span>{logs.length} entries</span>
        <span className="hud-panel-footer-blink">▐</span>
      </div>
    </div>
  );
};

export default SystemLogs;
