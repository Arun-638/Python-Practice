import React from 'react';
import { motion } from 'framer-motion';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 12, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className={`hud-msg ${isUser ? 'hud-msg-user' : 'hud-msg-jarvis'}`}
    >
      {/* Header line */}
      <div className={`hud-msg-header ${isUser ? 'hud-msg-header-user' : ''}`}>
        <span className="hud-msg-indicator" />
        <span className="hud-msg-sender">{isUser ? 'OPERATOR' : 'J.A.R.V.I.S'}</span>
        <span className="hud-msg-time">{new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })}</span>
      </div>

      {/* Content */}
      <div className="hud-msg-body">
        {message.content}
        {message.streaming && (
          <span className="hud-msg-cursor" />
        )}
      </div>

      {/* Skill tag */}
      {message.skill && (
        <div className="hud-msg-skill">
          <span className="hud-msg-skill-dot" />
          MODULE: {message.skill}
        </div>
      )}
    </motion.div>
  );
};

export const TypingIndicator = () => (
  <motion.div
    initial={{ opacity: 0, y: 8 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: 8 }}
    className="hud-msg hud-msg-jarvis"
  >
    <div className="hud-msg-header">
      <span className="hud-msg-indicator" />
      <span className="hud-msg-sender">J.A.R.V.I.S</span>
    </div>
    <div className="hud-msg-body">
      <div className="hud-typing">
        <span className="hud-typing-bar" style={{ animationDelay: '0s' }} />
        <span className="hud-typing-bar" style={{ animationDelay: '0.15s' }} />
        <span className="hud-typing-bar" style={{ animationDelay: '0.3s' }} />
        <span className="hud-typing-text">PROCESSING</span>
      </div>
    </div>
  </motion.div>
);

export default MessageBubble;
