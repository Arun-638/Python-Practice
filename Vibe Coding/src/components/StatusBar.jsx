import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const StatusBar = ({ isOnline }) => {
  const [time, setTime] = useState('');
  const [date, setDate] = useState('');
  const [seconds, setSeconds] = useState('');

  useEffect(() => {
    const tick = () => {
      const now = new Date();
      setTime(now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }));
      setSeconds(String(now.getSeconds()).padStart(2, '0'));
      setDate(now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }));
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <motion.div
      className="relative z-20 mb-4"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="hud-status-bar">
        {/* Left Wing */}
        <div className="hud-bar-wing hud-bar-wing-left">
          <div className="hud-bar-data-group">
            <div className="hud-bar-label">LOCAL</div>
            <div className="hud-bar-value-lg">{time}<span className="hud-bar-value-blink">:{seconds}</span></div>
          </div>
          <div className="hud-bar-separator" />
          <div className="hud-bar-data-group">
            <div className="hud-bar-label">DATE</div>
            <div className="hud-bar-value">{date}</div>
          </div>
          <div className="hud-bar-separator" />
          <div className="hud-bar-data-group">
            <div className="hud-bar-label">LINK</div>
            <div className={`hud-bar-status ${isOnline ? 'active' : 'offline'}`}>
              <span className="hud-bar-status-dot" />
              {isOnline ? 'NEURAL-LINK' : 'OFFLINE'}
            </div>
          </div>
        </div>

        {/* Center Crest */}
        <div className="hud-bar-center">
          <div className="hud-bar-center-diamond" />
          <div className="hud-bar-title">
            <span className="hud-bar-title-pre">STARK INDUSTRIES</span>
            <span className="hud-bar-title-main">J.A.R.V.I.S</span>
            <span className="hud-bar-title-sub">MARK III · INTERFACE v3.2.1</span>
          </div>
          <div className="hud-bar-center-diamond" />
        </div>

        {/* Right Wing */}
        <div className="hud-bar-wing hud-bar-wing-right">
          <div className="hud-bar-data-group">
            <div className="hud-bar-label">OPERATOR</div>
            <div className="hud-bar-value">ARUN A RAJ</div>
          </div>
          <div className="hud-bar-separator" />
          <div className="hud-bar-data-group">
            <div className="hud-bar-label">CLEARANCE</div>
            <div className="hud-bar-value" style={{ color: 'rgba(52, 211, 153, 0.8)' }}>LEVEL 10</div>
          </div>
          <div className="hud-bar-separator" />
          <div className="hud-bar-data-group">
            <div className="hud-bar-label">CORE</div>
            <div className={`hud-bar-status ${isOnline ? 'active' : 'offline'}`}>
              <span className="hud-bar-status-dot" />
              {isOnline ? 'STABLE' : 'DOWN'}
            </div>
          </div>
        </div>
      </div>

      {/* Thin horizontal accent line below */}
      <div className="hud-bar-accent-line" />
    </motion.div>
  );
};

export default StatusBar;
