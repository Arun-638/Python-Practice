import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Radio } from 'lucide-react';
import StatusBar from './components/StatusBar';
import SystemLogs from './components/SystemLogs';
import SkillsPanel from './components/SkillsPanel';
import MessageBubble, { TypingIndicator } from './components/MessageBubble';
import ArcReactor from './components/ArcReactor';

// ── Floating Holographic Particles ──────────────────────────────────────────
const HoloParticles = () => {
  const particles = useMemo(() =>
    Array.from({ length: 30 }, (_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      delay: `${Math.random() * 8}s`,
      duration: `${4 + Math.random() * 6}s`,
      size: Math.random() > 0.7 ? 3 : 2,
    })), []);

  return (
    <div className="holo-particles">
      {particles.map(p => (
        <div key={p.id} className="holo-particle" style={{
          left: p.left,
          top: p.top,
          width: p.size,
          height: p.size,
          animationDelay: p.delay,
          animationDuration: p.duration,
        }} />
      ))}
    </div>
  );
};

// ── Main App ────────────────────────────────────────────────────────────────
const BACKEND = '/api';

export default function JarvisHUD() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'System initialized. All subsystems nominal. Welcome back, Sir.' }
  ]);
  const [input, setInput] = useState('');
  const [orbState, setOrbState] = useState('idle');
  const [isTyping, setIsTyping] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [continuousMode, setContinuousMode] = useState(true);
  const [requiresInteraction, setRequiresInteraction] = useState(false);
  const [sessionActive, setSessionActive] = useState(false);
  const [showCinematic, setShowCinematic] = useState(false);
  const [silentMode, setSilentMode] = useState(false);
  const [skills, setSkills] = useState([]);
  const [systemStats, setSystemStats] = useState(null);
  const [weatherData, setWeatherData] = useState(null);

  const chatEndRef = useRef(null);
  const inputRef = useRef(null);
  const recognitionRef = useRef(null);
  const abortControllerRef = useRef(null);
  const pendingCallRef = useRef(false);
  const silentModeRef = useRef(false);

  // Keep track of state for event handlers
  const orbStateRef = useRef(orbState);
  const continuousModeRef = useRef(continuousMode);
  const sessionActiveRef = useRef(sessionActive);
  const isOnlineRef = useRef(isOnline);
  useEffect(() => { orbStateRef.current = orbState; }, [orbState]);
  useEffect(() => { continuousModeRef.current = continuousMode; }, [continuousMode]);
  useEffect(() => { sessionActiveRef.current = sessionActive; }, [sessionActive]);
  useEffect(() => { isOnlineRef.current = isOnline; }, [isOnline]);
  useEffect(() => { silentModeRef.current = silentMode; }, [silentMode]);

  // ── Health check ──────────────────────────────────────────────────────────
  useEffect(() => {
    const check = async () => {
      try {
        const r = await fetch(`${BACKEND}/health`, { signal: AbortSignal.timeout(2000) });
        setIsOnline(r.ok);
      } catch {
        setIsOnline(false);
      }
    };
    check();
    const id = setInterval(check, 10000);
    return () => clearInterval(id);
  }, []);

  // ── Background SSE Events listener ──────────────────────────────────────────
  useEffect(() => {
    const es = new EventSource(`${BACKEND}/events`);
    es.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data.event === 'WHATSAPP_CALL' && !pendingCallRef.current) {

          // ── SILENT MODE AUTO-HANDLER ──────────────────────────────────
          if (silentModeRef.current) {
            // Auto-handle: accept → play silent.wav → hang up after 5.5s
            pendingCallRef.current = true;
            setOrbState('speaking');
            speakText("Silent mode active. Handling the call automatically, Sir.");
            fetch(`${BACKEND}/whatsapp/accept`, { method: 'POST' }).then(() => {
              setTimeout(() => {
                fetch(`${BACKEND}/whatsapp/speak-silent`, { method: 'POST' });
                setTimeout(() => {
                  fetch(`${BACKEND}/whatsapp/decline`, { method: 'POST' });
                  pendingCallRef.current = false;
                }, 2500);
              }, 1000);
            });
            return;
          }

          // ── NORMAL MODE: Ask user what to do ──────────────────────────
          pendingCallRef.current = true;

          // Interrupt any active TTS
          window.speechSynthesis.cancel();
          if (abortControllerRef.current) abortControllerRef.current.abort();

          setOrbState('speaking');
          speakText("Sir, incoming WhatsApp call. Should I attend and tell them you are busy?");

          // Automatically reopen mic to listen for Yes/No
          setTimeout(() => {
            setOrbState('listening');
            try { recognitionRef.current?.stop(); } catch (e) { }
            setTimeout(() => {
              try {
                recognitionRef.current?.start();
                setIsListening(true);
              } catch (e) { }
            }, 500);
          }, 4500);
        }
      } catch (err) { }
    };
    return () => es.close();
  }, []);

  // ── Load skills & stats ───────────────────────────────────────────────────
  useEffect(() => {
    if (!isOnline) return;
    fetch(`${BACKEND}/skills`).then(r => r.json()).then(d => setSkills(d.skills || [])).catch(() => { });

    const fetchStats = () => {
      fetch(`${BACKEND}/system`).then(r => r.json()).then(setSystemStats).catch(() => { });
      fetch(`${BACKEND}/weather`).then(r => r.json()).then(d => setWeatherData(d.weather)).catch(() => { });
    };

    fetchStats();
    const statId = setInterval(fetchStats, 10000);
    return () => clearInterval(statId);
  }, [isOnline]);

  // ── Clap Detection Engine ─────────────────────────────────────────────────
  const triggerCinematicRoutine = useCallback(() => {
    speakText("Welcome, Sir. Initializing sequence protocols.");
    fetch(`${BACKEND}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'open vs code' }),
    }).catch(() => { });

    setTimeout(() => {
      fetch(`${BACKEND}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'open whatsapp' }),
      }).catch(() => { });
    }, 1000);

    setShowCinematic(true);
    setTimeout(() => {
      setShowCinematic(false);
    }, 20000);
  }, []);

  const triggerCinematicRef = useRef(triggerCinematicRoutine);
  useEffect(() => { triggerCinematicRef.current = triggerCinematicRoutine; }, [triggerCinematicRoutine]);

  // Automatically start background listening once system awakens if hands-free was saved
  useEffect(() => {
    if (!requiresInteraction && continuousMode) {
      startListening();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [requiresInteraction]);

  // ── Auto-scroll ───────────────────────────────────────────────────────────
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const latestTranscriptRef = useRef('');

  // ── Web Speech API ────────────────────────────────────────────────────────
  const startListening = () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser.');
      return;
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SR();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
      if (orbStateRef.current !== 'speaking') {
        setOrbState('listening');
      }
      latestTranscriptRef.current = '';
    };

    recognition.onresult = (e) => {
      const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
      setInput(transcript);
      latestTranscriptRef.current = transcript;

      // Barge-in detection (interrupt TTS if user speaks during response)
      if (orbStateRef.current === 'speaking' || orbStateRef.current === 'thinking') {
        window.speechSynthesis.cancel();
        if (abortControllerRef.current) abortControllerRef.current.abort();
        setOrbState('listening');
        orbStateRef.current = 'listening';
      }
    };

    recognition.onend = () => {
      setIsListening(false);
      const rawTranscript = latestTranscriptRef.current.trim();
      const finalTranscript = rawTranscript.toLowerCase();
      latestTranscriptRef.current = '';

      let shouldProcess = false;
      let textToProcess = rawTranscript;

      // ── OPEN COMMAND MODE ─────────────────────────────────────────────
      // No wake-word required! All speech gets processed directly.
      if (continuousModeRef.current) {
        // Exit commands
        if ((finalTranscript.includes('bye bye') || finalTranscript.includes('goodbye') || finalTranscript.includes('sleep') || finalTranscript.includes('exit')) && !finalTranscript.includes('silent')) {
          setOrbState('idle');
          speakText("Goodbye, Sir.");
          return;
        }
        if (finalTranscript) {
          shouldProcess = true;
        }
      } else {
        shouldProcess = !!finalTranscript;
      }

      if (shouldProcess && textToProcess) {

        // --- SILENT MODE TOGGLE (voice command, anytime) ---
        if (finalTranscript.includes('silent mode') && !finalTranscript.includes('exit')) {
          setSilentMode(true);
          silentModeRef.current = true;
          setOrbState('speaking');
          speakText("Silent mode activated, Sir. All incoming WhatsApp calls will be handled automatically. Say exit from silent mode to disable.");
          if (continuousModeRef.current) setTimeout(() => { try { recognitionRef.current.start(); } catch (e) { } }, 6000);
          return;
        }
        if (finalTranscript.includes('exit') && finalTranscript.includes('silent')) {
          setSilentMode(false);
          silentModeRef.current = false;
          setOrbState('speaking');
          speakText("Silent mode deactivated, Sir. I will ask you before handling calls.");
          if (continuousModeRef.current) setTimeout(() => { try { recognitionRef.current.start(); } catch (e) { } }, 5000);
          return;
        }

        // --- WHATSAPP CALL HANDLER ---
        if (pendingCallRef.current) {
          pendingCallRef.current = false; // Reset lock

          // ── ATTEND / YES ───────────────────────────────────────────────
          if (finalTranscript.includes("yes") || finalTranscript.includes("attend") || finalTranscript.includes("accept") || finalTranscript.includes("sure")) {
            setOrbState('idle');
            // Connect to call locally
            fetch(`${BACKEND}/whatsapp/accept`, { method: 'POST' }).then(() => {
              // Wait 1s for hardware audio sync, then tell Python to blast audio into the VB-Cable device
              setTimeout(() => {
                fetch(`${BACKEND}/whatsapp/speak`, { method: 'POST' });
                // Give Jarvis 5.5 seconds (approx length of the wav file), then hang up natively
                setTimeout(() => {
                  fetch(`${BACKEND}/whatsapp/decline`, { method: 'POST' });
                }, 5500);
              }, 1000);
            });
          } else {
            setOrbState('idle');
            speakText("Ignoring the call, Sir.");
            fetch(`${BACKEND}/whatsapp/decline`, { method: 'POST' }); // Decline outright
          }

          if (continuousModeRef.current) setTimeout(() => { try { recognitionRef.current.start(); } catch (e) { } }, 5000);
          return;
        }

        // --- CINEMATIC VOICE COMMAND IMMUNITY ---
        if (finalTranscript.includes('clap') || finalTranscript.includes('cinematic')) {
          triggerCinematicRef.current();
          setOrbState('idle');
          // Wait 20.5 seconds for the YouTube video to finish playing before reopening the Microphone!
          setTimeout(() => {
            if (continuousModeRef.current) {
              try { recognitionRef.current.start(); } catch (e) { }
            }
          }, 20500);
          return;
        }

        setOrbState('thinking');
        sendMessage(textToProcess);
      } else {
        if (orbStateRef.current !== 'thinking' && orbStateRef.current !== 'speaking') {
          setOrbState('idle');
        }
        // Always auto-restart in continuous mode
        if (continuousModeRef.current) {
          try { recognitionRef.current.start(); } catch (e) { }
        }
      }
    };
    recognition.onerror = () => {
      setIsListening(false);
      if (continuousModeRef.current) {
        setTimeout(() => { try { recognitionRef.current?.start(); } catch (e) { } }, 1000);
      } else {
        setOrbState('idle');
      }
    };

    recognitionRef.current = recognition;
    try {
      recognition.start();
    } catch (err) {
      alert("Microphone error: " + err.message + "\n\nMake sure your browser has microphone permissions allowed.");
      setIsListening(false);
      setContinuousMode(false);
      setOrbState('idle');
    }
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setIsListening(false);
    setContinuousMode(false);
    continuousModeRef.current = false;
    setSessionActive(false);
    sessionActiveRef.current = false;
    setOrbState('idle');
    orbStateRef.current = 'idle';
  };

  const toggleContinuous = () => {
    if (continuousMode) {
      localStorage.setItem('jarvisHandsFree', 'false');
      setContinuousMode(false);
      continuousModeRef.current = false;
      stopListening();
    } else {
      localStorage.setItem('jarvisHandsFree', 'true');
      setContinuousMode(true);
      continuousModeRef.current = true;
      setSessionActive(false);
      sessionActiveRef.current = false;
      startListening();
    }
  };

  // ── Text-to-Speech ────────────────────────────────────────────────────────
  const speakText = (text) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    // remove skill tags or markdown if present for speech
    const cleanText = text.replace(/\[SKILL:.*?\]/g, '').replace(/[\*\#\`]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'en-GB';
    utterance.pitch = 0.9;
    utterance.rate = 1.0;

    // Attempt to select a male British voice if available
    const voices = window.speechSynthesis.getVoices();
    const jarvisVoice = voices.find(v => v.lang === 'en-GB' && v.name.toLowerCase().includes('male'));
    if (jarvisVoice) utterance.voice = jarvisVoice;

    window.speechSynthesis.speak(utterance);

    utterance.onend = () => {
      setOrbState('idle');

      if (continuousModeRef.current) {
        try { recognitionRef.current?.start(); } catch (e) { }
      }
    };
  };

  // ── Send message ──────────────────────────────────────────────────────────
  const sendMessage = async (overrideText) => {
    const text = typeof overrideText === 'string' ? overrideText.trim() : input.trim();
    if (!text) return;

    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setOrbState('thinking');
    setIsTyping(true);

    if (!isOnlineRef.current) {
      // Offline mock
      await new Promise(r => setTimeout(r, 1200));
      setIsTyping(false);
      setOrbState('speaking');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `[Offline mode] Backend not running. Start the FastAPI server to enable AI responses.`
      }]);
      setTimeout(() => setOrbState('idle'), 2000);
      return;
    }

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`${BACKEND}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const contentType = response.headers.get('content-type') || '';

      // ── Streaming SSE ──────────────────────────────────────────────────
      if (contentType.includes('text/event-stream')) {
        setIsTyping(false);
        setOrbState('speaking');
        const msgId = Date.now();
        setMessages(prev => [...prev, { id: msgId, role: 'assistant', content: '', streaming: true }]);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let spokenResponse = '';

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop();

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6).trim();
              if (data === '[DONE]') continue;
              try {
                const parsed = JSON.parse(data);
                if (parsed.token) {
                  setMessages(prev => prev.map(m =>
                    m.id === msgId ? { ...m, content: m.content + parsed.token, skill: parsed.skill } : m
                  ));
                  spokenResponse += parsed.token;
                }
              } catch { }
            }
          }
        }
        setMessages(prev => prev.map(m =>
          m.id === msgId ? { ...m, streaming: false } : m
        ));

        // Only speak if not aborted
        if (!abortControllerRef.current?.signal.aborted) {
          speakText(spokenResponse);
        }

      } else {
        // ── JSON response ─────────────────────────────────────────────────
        const data = await response.json();
        setIsTyping(false);
        setOrbState('speaking');
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.response || data.message || 'No response.',
          skill: data.skill,
        }]);
        if (!abortControllerRef.current?.signal.aborted) {
          speakText(data.response || data.message || '');
        }
      }

    } catch (err) {
      if (err.name === 'AbortError') {
        setIsTyping(false);
        return; // User barged in, silently swallow error
      }
      setIsTyping(false);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `System error: ${err.message}. Please check if the backend is running.`
      }]);
      setOrbState('idle');
    } finally {
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="relative w-full h-screen overflow-hidden p-5 select-none" style={{ fontFamily: "'Inter', sans-serif" }}>
      {/* Background layers */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="bg-grid" />
        <div className="hex-overlay" />
        <div className="scanner-line" />
        <div className="vignette" />
        <div className="edge-glow-top" />
        <div className="edge-glow-bottom" />
      </div>

      {/* HUD Corner Brackets */}
      <div className="hud-corner hud-corner-tl" />
      <div className="hud-corner hud-corner-tr" />
      <div className="hud-corner hud-corner-bl" />
      <div className="hud-corner hud-corner-br" />

      {/* Holographic Particles */}
      <HoloParticles />

      {/* Status Bar */}
      <StatusBar isOnline={isOnline} />

      {/* Cinematic YouTube Overlay */}
      <AnimatePresence>
        {showCinematic && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 50, x: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 50 }}
            className="absolute bottom-8 left-8 w-[400px] rounded-xl overflow-hidden glass-panel z-50 shadow-[0_0_50px_rgba(34,211,238,0.25)] border border-cyan-400/30"
          >
            <div className="absolute top-2 left-3 z-10">
              <div className="px-2 py-0.5 rounded-full bg-cyan-900/60 backdrop-blur-md text-[10px] uppercase font-bold tracking-widest text-cyan-300 border border-cyan-500/50 shadow-[0_0_10px_rgba(6,182,212,0.6)] animate-pulse">
                CINEMATIC OVERRIDE
              </div>
            </div>
            <iframe
              width="100%"
              height="225"
              src="https://www.youtube.com/embed/hEIexwwiKKU?autoplay=1&controls=0&modestbranding=1"
              title="Iron Man Routine"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="pointer-events-none"
            ></iframe>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Grid */}
      <div className="relative z-10 grid grid-cols-12 gap-4 h-[calc(100vh-100px)]">

        {/* LEFT — System Logs */}
        <motion.div
          className="col-span-3 h-full min-h-0"
          initial={{ opacity: 0, x: -24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
        >
          <div className="h-full overflow-hidden flex flex-col">
            <SystemLogs events={messages} />
          </div>
        </motion.div>

        {/* CENTER — Arc Reactor + Chat + Input */}
        <div className="col-span-6 flex flex-col items-center gap-3 h-full min-h-0">
          {/* Arc Reactor */}
          <motion.div
            className="flex-shrink-0 pt-1 h-72 flex items-center justify-center"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <ArcReactor state={orbState} />
          </motion.div>

          {/* Chat Terminal */}
          <motion.div
            className="flex-1 w-full hud-panel rounded-md overflow-hidden flex flex-col min-h-0"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.35 }}
          >
            {/* Panel Header */}
            <div className="hud-panel-header">
              <div className="hud-panel-header-bar" />
              <div className="hud-panel-header-content">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--cyan)" strokeWidth="1.5">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
                <span className="hud-panel-title">COMM CHANNEL</span>
                <span className="hud-panel-tag">ENCRYPTED</span>
              </div>
              <div className="hud-panel-header-bar" />
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-3 min-h-0 scroll-smooth" style={{ position: 'relative', zIndex: 3 }}>
              <AnimatePresence initial={false}>
                {messages.map((msg, i) => (
                  <MessageBubble key={msg.id || i} message={msg} />
                ))}
                {isTyping && <TypingIndicator key="typing" />}
              </AnimatePresence>
              <div ref={chatEndRef} />
            </div>

            {/* Input */}
            <div className="px-4 py-3 border-t border-cyan-400/5" style={{ position: 'relative', zIndex: 3 }}>
              <div className="input-glow-wrapper">
                <div className="input-bar glass-panel flex items-center border border-white/5 rounded-md transition-all focus-within:border-cyan-500/30">
                  <input
                    ref={inputRef}
                    id="jarvis-input"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={continuousMode ? '// VOICE ACTIVE — SPEAK FREELY' : isListening ? '// LISTENING...' : '// AWAITING INPUT, SIR'}
                    disabled={isListening || continuousMode}
                    className="flex-1 bg-transparent px-4 py-2.5 outline-none text-slate-200 placeholder-slate-600"
                  />
                  <div className="flex items-center gap-2 pr-3">
                    <button
                      onClick={toggleContinuous}
                      title="Toggle Hands-Free Mode"
                      className={`p-2 rounded transition-all duration-300 ${continuousMode ? 'bg-rose-500/20 text-rose-400 shadow-[0_0_12px_rgba(244,63,94,0.3)]' : 'hover:bg-white/5 text-slate-500'}`}
                    >
                      <Radio size={14} className={continuousMode ? "animate-pulse" : ""} />
                    </button>
                    <div className="w-[1px] h-5 bg-white/8" />
                    <button
                      onClick={isListening && !continuousMode ? stopListening : startListening}
                      title="Push to Talk"
                      className={`p-2 rounded transition-all ${isListening && !continuousMode ? 'bg-cyan-500/15 text-cyan-400 animate-pulse' : 'hover:bg-white/5 text-slate-500'}`}
                    >
                      {isListening && !continuousMode ? <MicOff size={14} /> : <Mic size={14} />}
                    </button>
                    <button
                      onClick={() => sendMessage()}
                      disabled={!input.trim()}
                      className="p-2 rounded bg-cyan-600/60 hover:bg-cyan-500/80 text-white transition-all disabled:opacity-20 disabled:hover:bg-cyan-600/60"
                    >
                      <Send size={14} />
                    </button>
                  </div>
                </div>
              </div>
              <div className="flex justify-between items-center px-1 mt-2 text-[8px] uppercase tracking-[0.2em] text-cyan-200/25" style={{ fontFamily: 'var(--hud-font)' }}>
                <span className="flex items-center gap-2">
                  {isOnline ? <><span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.6)] animate-pulse" /> UPLINK ACTIVE</> : <><span className="w-1.5 h-1.5 rounded-full bg-rose-500" /> UPLINK SEVERED</>}
                </span>
                <span>STARK SEC · AES-256-GCM</span>
              </div>
            </div>
          </motion.div>
        </div>

        {/* RIGHT — System Status + Skills */}
        <motion.div
          className="col-span-3 h-full min-h-0"
          initial={{ opacity: 0, x: 24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, delay: 0.15 }}
        >
          <div className="h-full overflow-hidden flex flex-col">
            <SkillsPanel skills={skills} systemStats={systemStats} weatherData={weatherData} />
          </div>
        </motion.div>
      </div>

      {/* Silent Mode Indicator */}
      <AnimatePresence>
        {silentMode && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="absolute top-20 left-1/2 -translate-x-1/2 z-50"
          >
            <div className="flex items-center gap-3 px-5 py-2.5 rounded-full bg-rose-950/60 backdrop-blur-md border border-rose-500/40 shadow-[0_0_25px_rgba(244,63,94,0.3)]">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse shadow-[0_0_10px_rgba(244,63,94,0.8)]" />
              <span className="text-[11px] font-mono font-bold uppercase tracking-[0.2em] text-rose-400">
                Silent Mode Active
              </span>
              <span className="text-[9px] font-mono text-rose-400/50">say "exit from silent mode" to disable</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* HUD Bottom Data Ticker */}
      <div className="hud-ticker">
        <span><span className="ticker-dot" /> STARK INDUSTRIES</span>
        <span>ARC REACTOR: STABLE</span>
        <span>{silentMode ? 'CALL MODE: SILENT' : 'THREAT LEVEL: MINIMAL'}</span>
        <span><span className="ticker-dot" /> ENCRYPTION: AES-256</span>
        <span>UPLINK: ACTIVE</span>
      </div>
    </div>
  );
}
