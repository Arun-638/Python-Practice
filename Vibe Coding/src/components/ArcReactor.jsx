import React, { useMemo } from 'react';

const ArcReactor = ({ state = 'idle' }) => {
  const stateColors = {
    idle:      { primary: '#00f2ff', secondary: '#0066ff' },
    listening: { primary: '#3b82f6', secondary: '#6366f1' },
    thinking:  { primary: '#f59e0b', secondary: '#ef4444' },
    speaking:  { primary: '#22d3ee', secondary: '#06b6d4' },
  };

  const { primary, secondary } = stateColors[state] || stateColors.idle;

  /* ── Outer tick marks: 72 ticks at 5° intervals ── */
  const outerTicks = useMemo(() =>
    Array.from({ length: 72 }, (_, i) => {
      const deg   = i * 5 - 90;
      const angle = deg * Math.PI / 180;
      const isMajor = i % 6 === 0;          // every 30°
      const isMid   = i % 3 === 0 && !isMajor;
      const innerR  = isMajor ? 126 : isMid ? 131 : 134;
      const outerR  = 139;
      return {
        x1: 150 + innerR * Math.cos(angle),
        y1: 150 + innerR * Math.sin(angle),
        x2: 150 + outerR * Math.cos(angle),
        y2: 150 + outerR * Math.sin(angle),
        isMajor, isMid, i,
      };
    }), []);

  /* ── Inner tick marks: 36 ticks at 10° intervals ── */
  const innerTicks = useMemo(() =>
    Array.from({ length: 36 }, (_, i) => {
      const deg   = i * 10 - 90;
      const angle = deg * Math.PI / 180;
      const isMajor = i % 3 === 0;
      return {
        x1: 150 + 72 * Math.cos(angle),
        y1: 150 + 72 * Math.sin(angle),
        x2: 150 + (isMajor ? 64 : 67) * Math.cos(angle),
        y2: 150 + (isMajor ? 64 : 67) * Math.sin(angle),
        isMajor, i,
      };
    }), []);

  /* ── Orbital dots: small circles orbiting on ring 3 ── */
  const orbitalDots = useMemo(() =>
    Array.from({ length: 8 }, (_, i) => {
      const deg   = i * 45 - 90;
      const angle = deg * Math.PI / 180;
      return {
        cx: 150 + 100 * Math.cos(angle),
        cy: 150 + 100 * Math.sin(angle),
        i,
      };
    }), []);

  /* ── Helper: SVG arc path ── */
  const describeArc = (r, startAngle, endAngle) => {
    const s  = (startAngle - 90) * Math.PI / 180;
    const e  = (endAngle - 90) * Math.PI / 180;
    const x1 = 150 + r * Math.cos(s);
    const y1 = 150 + r * Math.sin(s);
    const x2 = 150 + r * Math.cos(e);
    const y2 = 150 + r * Math.sin(e);
    const lg = endAngle - startAngle > 180 ? 1 : 0;
    return `M ${x1} ${y1} A ${r} ${r} 0 ${lg} 1 ${x2} ${y2}`;
  };

  return (
    <div className={`arc-reactor-container arc-state-${state}`}>
      {/* ── Ambient circular glow ── */}
      <div className="arc-ambient-glow" />

      {/* ── Energy pulse ripples ── */}
      <div className="arc-energy-pulse pulse-1" />
      <div className="arc-energy-pulse pulse-2" />
      <div className="arc-energy-pulse pulse-3" />

      {/* ── Main SVG ── */}
      <svg viewBox="0 0 300 300" className="arc-svg" width="280" height="280">
        <defs>
          <radialGradient id="coreGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%"   stopColor="#ffffff" stopOpacity="0.95" />
            <stop offset="25%"  stopColor={primary}  stopOpacity="0.85" />
            <stop offset="60%"  stopColor={secondary} stopOpacity="0.4" />
            <stop offset="100%" stopColor={secondary} stopOpacity="0" />
          </radialGradient>
          <filter id="coreGlow">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="softGlow">
            <feGaussianBlur stdDeviation="2" />
            <feMerge>
              <feMergeNode />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="thinGlow">
            <feGaussianBlur stdDeviation="1.2" />
            <feMerge>
              <feMergeNode />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* ═══ RING 1 ─ Outermost tick-mark ring ═══ (clockwise) */}
        <g className="arc-ring-1">
          <circle cx="150" cy="150" r="140" fill="none" stroke={primary} strokeWidth="0.5" opacity="0.2" />
          {outerTicks.map(t => (
            <line key={t.i}
              x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
              stroke={primary}
              strokeWidth={t.isMajor ? 1.5 : t.isMid ? 0.8 : 0.4}
              opacity={t.isMajor ? 0.9 : t.isMid ? 0.5 : 0.25}
            />
          ))}
          {/* Data readouts at cardinal positions */}
          <text x="150" y="116" textAnchor="middle" fill={primary} fontSize="5"
            fontFamily="'JetBrains Mono', monospace" opacity="0.5" className="arc-data-text">
            SYS:ONLINE
          </text>
          <text x="150" y="190" textAnchor="middle" fill={primary} fontSize="5"
            fontFamily="'JetBrains Mono', monospace" opacity="0.5" className="arc-data-text">
            NEURAL:ACTIVE
          </text>
          <text x="195" y="153" textAnchor="start" fill={primary} fontSize="4.5"
            fontFamily="'JetBrains Mono', monospace" opacity="0.35" className="arc-data-text">
            λ 2.4G
          </text>
          <text x="105" y="153" textAnchor="end" fill={primary} fontSize="4.5"
            fontFamily="'JetBrains Mono', monospace" opacity="0.35" className="arc-data-text">
            MK-III
          </text>
        </g>

        {/* ═══ RING 2 ─ Arc segments ═══ (counter-clockwise) */}
        <g className="arc-ring-2" filter="url(#softGlow)">
          <path d={describeArc(118, 5, 80)}   fill="none" stroke={primary} strokeWidth="2.5" strokeLinecap="round" opacity="0.5" />
          <path d={describeArc(118, 95, 170)}  fill="none" stroke={primary} strokeWidth="2.5" strokeLinecap="round" opacity="0.5" />
          <path d={describeArc(118, 185, 260)} fill="none" stroke={primary} strokeWidth="2.5" strokeLinecap="round" opacity="0.5" />
          <path d={describeArc(118, 275, 350)} fill="none" stroke={primary} strokeWidth="2.5" strokeLinecap="round" opacity="0.5" />
          {/* Tiny dots at arc endpoints */}
          {[5,80,95,170,185,260,275,350].map(a => {
            const rad = (a - 90) * Math.PI / 180;
            return <circle key={a} cx={150 + 118 * Math.cos(rad)} cy={150 + 118 * Math.sin(rad)} r="1.5" fill={primary} opacity="0.6" />;
          })}
        </g>

        {/* ═══ RING 3 ─ Dashed mid-ring with orbital dots ═══ (clockwise, slow) */}
        <g className="arc-ring-3">
          <circle cx="150" cy="150" r="100" fill="none" stroke={primary} strokeWidth="0.6" strokeDasharray="8 4 2 4" opacity="0.2" />
          {orbitalDots.map(d => (
            <circle key={d.i} cx={d.cx} cy={d.cy} r="1.8" fill={primary} opacity="0.25" />
          ))}
        </g>

        {/* ═══ RING 4 ─ Inner ring with notch marks ═══ (counter-clockwise) */}
        <g className="arc-ring-4">
          <circle cx="150" cy="150" r="75" fill="none" stroke={primary} strokeWidth="0.8" opacity="0.35" />
          {innerTicks.map(t => (
            <line key={t.i}
              x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
              stroke={primary}
              strokeWidth={t.isMajor ? 1 : 0.4}
              opacity={t.isMajor ? 0.7 : 0.3}
            />
          ))}
          {/* Triangular cardinal markers */}
          <polygon points="150,73 147.5,79 152.5,79" fill={primary} opacity="0.6" />
          <polygon points="227,150 221,147.5 221,152.5" fill={primary} opacity="0.6" />
          <polygon points="150,227 147.5,221 152.5,221" fill={primary} opacity="0.6" />
          <polygon points="73,150 79,147.5 79,152.5" fill={primary} opacity="0.6" />
        </g>

        {/* ═══ RING 5 ─ Thin accent ring ═══ (clockwise, fast) */}
        <g className="arc-ring-5">
          <circle cx="150" cy="150" r="55" fill="none" stroke={primary} strokeWidth="0.3" strokeDasharray="3 8" opacity="0.2" />
        </g>

        {/* ═══ RING 6 ─ Inner arc accents ═══ (counter-clockwise, fast) */}
        <g className="arc-ring-6" filter="url(#thinGlow)">
          <path d={describeArc(88, 20, 70)}   fill="none" stroke={primary} strokeWidth="1.2" strokeLinecap="round" opacity="0.25" />
          <path d={describeArc(88, 110, 160)}  fill="none" stroke={primary} strokeWidth="1.2" strokeLinecap="round" opacity="0.25" />
          <path d={describeArc(88, 200, 250)}  fill="none" stroke={primary} strokeWidth="1.2" strokeLinecap="round" opacity="0.25" />
          <path d={describeArc(88, 290, 340)}  fill="none" stroke={primary} strokeWidth="1.2" strokeLinecap="round" opacity="0.25" />
        </g>

        {/* ═══ CORE ═══ */}
        <g className="arc-core-group">
          <circle cx="150" cy="150" r="42" fill="url(#coreGrad)" filter="url(#coreGlow)" className="arc-core" />
          <circle cx="150" cy="150" r="28" fill="none" stroke={primary} strokeWidth="0.5" opacity="0.4" className="arc-core-ring" />
          <circle cx="150" cy="150" r="15" fill={primary} opacity="0.15" />
          <circle cx="150" cy="150" r="5"  fill="#ffffff" opacity="0.9" filter="url(#coreGlow)" />
        </g>

        {/* ═══ SCANNING BEAM ═══ */}
        <g className="arc-scan-beam">
          <line x1="150" y1="150" x2="150" y2="12" stroke={primary} strokeWidth="0.8" opacity="0.1" />
          <circle cx="150" cy="12" r="2" fill={primary} opacity="0.35" />
        </g>

        {/* ═══ Cross-hair reference lines ═══ */}
        <g opacity="0.2">
          <line x1="150" y1="45" x2="150" y2="58" stroke={primary} strokeWidth="0.3" />
          <line x1="150" y1="242" x2="150" y2="255" stroke={primary} strokeWidth="0.3" />
          <line x1="45" y1="150" x2="58" y2="150" stroke={primary} strokeWidth="0.3" />
          <line x1="242" y1="150" x2="255" y2="150" stroke={primary} strokeWidth="0.3" />
        </g>

        {/* ═══ Diagonal accent lines ═══ */}
        <g opacity="0.1">
          <line x1="53" y1="53" x2="66" y2="66" stroke={primary} strokeWidth="0.3" />
          <line x1="247" y1="53" x2="234" y2="66" stroke={primary} strokeWidth="0.3" />
          <line x1="53" y1="247" x2="66" y2="234" stroke={primary} strokeWidth="0.3" />
          <line x1="247" y1="247" x2="234" y2="234" stroke={primary} strokeWidth="0.3" />
        </g>
      </svg>

      {/* ── State label ── */}
      <div className="arc-state-label">
        <span className="arc-state-dot" />
        <span>{state.toUpperCase()}</span>
      </div>
    </div>
  );
};

export default ArcReactor;
