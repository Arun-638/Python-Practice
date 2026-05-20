import os
import json
import asyncio
import psutil
import threading
import pyttsx3
import sounddevice as sd
import scipy.io.wavfile as wav
from datetime import datetime
import requests
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()

from jarvis.skills.manager import SkillManager
from jarvis.memory import MemorySystem
from jarvis.brain import Brain
from jarvis.whatsapp_hook import WhatsAppHook

# ── App init ──────────────────────────────────────────────────────────────
app = FastAPI(title="J.A.R.V.I.S API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Boot Jarvis ───────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
skills_dir = os.path.join(BASE_DIR, "skills")

skill_manager = SkillManager(skills_dir)
skill_manager.load_skills()

memory = MemorySystem(os.path.join(os.path.dirname(BASE_DIR), "jarvis_memory.db"))
brain  = Brain(skill_manager, memory)


# ── Request models ─────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str

# ── Global state ─────────────────────────────────────────────────────────
whatsapp_hook = WhatsAppHook()
sse_queues = []

async def whatsapp_monitor():
    loop = asyncio.get_event_loop()
    last_call_state = False
    
    while True:
        try:
            # Poll UI using a thread pool to avoid blocking the async event loop
            is_calling = await loop.run_in_executor(None, whatsapp_hook.is_call_active)
            if is_calling and not last_call_state:
                # Fire an SSE event down to the React HUD
                for q in sse_queues:
                    await q.put({"event": "WHATSAPP_CALL"})
            last_call_state = is_calling
        except Exception:
            pass
        await asyncio.sleep(2)

def generate_busy_audio():
    try:
        busy_path = os.path.join(os.path.dirname(BASE_DIR), "busy.wav")
        if not os.path.exists(busy_path):
            engine = pyttsx3.init()
            engine.save_to_file("Sir, Arun is busy right now, please try again later. Automatically ending call.", busy_path)
            engine.runAndWait()
    except Exception as e:
        print(f"[JARVIS] Audio Generation Error: {e}")

@app.on_event("startup")
async def startup_event():
    generate_busy_audio()
    asyncio.create_task(whatsapp_monitor())


# ── Routes ────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/events")
async def get_events():
    q = asyncio.Queue()
    sse_queues.append(q)
    
    async def event_generator():
        try:
            while True:
                data = await q.get()
                yield f"data: {json.dumps(data)}\n\n"
        except asyncio.CancelledError:
            if q in sse_queues:
                sse_queues.remove(q)
                
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

@app.post("/whatsapp/accept")
def whatsapp_accept():
    res = whatsapp_hook.accept_call()
    return {"success": res}

@app.post("/whatsapp/decline")
def whatsapp_decline():
    res = whatsapp_hook.decline_or_end_call()
    return {"success": res}

@app.get("/skills")
def get_skills():
    return {"skills": list(skill_manager.skills.keys())}


@app.get("/system")
def get_system():
    cpu = psutil.cpu_percent(interval=0.3)
    ram = psutil.virtual_memory()
    return {
        "cpu": round(cpu, 1),
        "ram": round(ram.percent, 1),
        "ram_used_gb": round(ram.used / 1e9, 1),
        "ram_total_gb": round(ram.total / 1e9, 1),
    }


@app.get("/weather")
def get_weather():
    try:
        response = requests.get("https://wttr.in/?format=%t+·+%C+·+%l", timeout=3)
        if response.status_code == 200:
            return {"weather": response.text.strip()}
    except:
        pass
    return {"weather": "Offline · No Data"}


@app.post("/chat")
async def chat(req: ChatRequest):
    """
    Streams Jarvis response as Server-Sent Events.
    Each event: data: {"token": "...", "skill": "..."|null}
    Final event: data: [DONE]
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    async def event_generator():
        loop = asyncio.get_event_loop()

        # Run blocking generator in thread pool
        def run_brain():
            return list(brain.process_stream(req.message))

        chunks = await loop.run_in_executor(None, run_brain)

        for chunk in chunks:
            if not chunk['done']:
                payload = json.dumps({"token": chunk['token'], "skill": chunk.get('skill')})
                yield f"data: {payload}\n\n"
                await asyncio.sleep(0)  # Let event loop breathe

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

PROJECT_ROOT = os.path.dirname(BASE_DIR)

def _find_vb_cable():
    """Locate the VB-Audio Virtual Cable output device."""
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if 'cable' in dev['name'].lower() and dev['max_output_channels'] > 0:
            return i
    print("[JARVIS] CRITICAL WARNING: Could not find VB-Audio Cable! Falling back to Sys Default.")
    return sd.default.device[1]

def _play_wav_to_cable(wav_filename):
    """Play a wav file strictly into the Virtual Audio Cable."""
    try:
        device_id = _find_vb_cable()
        wav_path = os.path.join(PROJECT_ROOT, wav_filename)
        if not os.path.exists(wav_path):
            print(f"[JARVIS] ERROR: '{wav_filename}' not found at {wav_path}")
            return
        fs, data = wav.read(wav_path)
        print(f"[JARVIS] Routing '{wav_filename}' into VB Cable (Device: {device_id})...")
        sd.play(data, fs, device=device_id)
        sd.wait()
        print(f"[JARVIS] VB Cable Transmission of '{wav_filename}' Complete.")
    except Exception as e:
        print(f"[JARVIS] Playback Error: {e}")

@app.post("/whatsapp/speak")
def whatsapp_speak():
    """Plays the busy message strictly into the Virtual Audio Cable"""
    threading.Thread(target=_play_wav_to_cable, args=("busy.wav",)).start()
    return {"status": "speaking"}

@app.post("/whatsapp/speak-silent")
def whatsapp_speak_silent():
    """Plays the silent audio strictly into the Virtual Audio Cable (Silent Mode)"""
    threading.Thread(target=_play_wav_to_cable, args=("silent.wav",)).start()
    return {"status": "speaking-silent"}
