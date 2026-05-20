---
name: Jarvis System Automation
description: A hybrid voice/chat assistant with an adaptive modular orchestrator for system automation.
type: design-spec
date: 2026-04-12
---

# Jarvis Design Specification

## 1. Overview
Jarvis is an advanced system automation agent designed to control the host OS, automate workflows, and retrieve information through a hybrid interface. It employs a "Modular Orchestrator" architecture, allowing it to learn and expand its capabilities dynamically.

## 2. Core Architecture: Modular Orchestrator
The system is divided into a central brain and a library of executable skills.

### 2.1 The Brain (Orchestrator)
- **Role:** Intent analysis and module routing.
- **Flow:** `User Input` $\rightarrow$ `LLM Intent Analysis` $\rightarrow$ `Skill Lookup` $\rightarrow$ `Module Execution` $\rightarrow$ `Feedback`.
- **Memory:** 
    - **Short-term:** 5-minute rolling conversation window.
    - **Long-term:** SQLite database for user preferences and skill metadata.

### 2.2 Action Modules (Skills)
- **Storage:** Standalone Python files in `skills/`.
- **Interface:** Each module must implement:
    - `execute(params)`: The core logic.
    - `metadata`: Description used by the Brain for routing.
- **Learning Engine:**
    - **Interactive:** LLM generates Python code from natural language descriptions.
    - **Example-based:** Records user action sequences and converts them into a module.
    - **Observation-based:** Monitors frequent patterns and suggests new modules proactively.

## 3. Interface & User Experience

### 3.1 Hybrid Input Layer
- **Chat:** CLI or floating window for text interaction.
- **Voice:** 
    - Wake-word detection ("Hey Jarvis").
    - STT (Speech-to-Text) and Neural TTS (Text-to-Speech).

### 3.2 UX Elements
- **Visual Cues:** Status indicators (Listening, Thinking, Executing).
- **Proactive Learning:** Notifications suggesting new automations based on observed behavior.
- **Teaching Mode:** A guided state where Jarvis records actions to create a new skill.

## 4. System Integration & Safety

### 4.1 Integration (The "Hands")
- **OS Control:** `pyautogui` (UI), `os`/`subprocess` (Shell), `psutil` (Monitoring).
- **Web:** `playwright` for browser-based automation.
- **External:** REST APIs for info retrieval (Weather, News, etc.).

### 4.2 Safety Guardrails
- **Permission Tiers:**
    - **Tier 1 (Low Risk):** Immediate execution (e.g., open app).
    - **Tier 2 (Medium Risk):** Requires confirmation (e.g., move files).
    - **Tier 3 (High Risk):** Explicit "Yes" confirmation required (e.g., delete files).
- **Verification:** All learned scripts are presented to the user for review before being committed to the `skills/` library.
- **Isolation:** New modules undergo a "dry run" or isolated test before full deployment.

## 5. Data & Privacy
- **Local First:** Observation data and long-term memory are stored locally.
- **Privacy:** Raw screen/keystroke logs are processed locally; only high-level intents are sent to the LLM.
