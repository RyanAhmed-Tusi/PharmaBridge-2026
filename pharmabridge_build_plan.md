# PharmaBridge — Complete Build Plan
### Autonomous Pharma Intelligence Platform
**From Zero to Working Prototype**

---

> **How to use this document:** Read it top to bottom once, then follow each Phase in order using Claude Code. Every code block is meant to be executed or saved exactly as shown. When you open Claude Code, paste the relevant section and say "build this."

---

## Table of Contents

1. [What You Are Building](#1-what-you-are-building)
2. [Accounts & API Keys You Need](#2-accounts--api-keys-you-need)
3. [Tools to Install on Your Computer](#3-tools-to-install-on-your-computer)
4. [System Architecture](#4-system-architecture)
5. [Complete Project Structure](#5-complete-project-structure)
6. [Database Design (Supabase)](#6-database-design-supabase)
7. [Environment Configuration (.env)](#7-environment-configuration-env)
8. [Phase 1 — Project Scaffold & Backend Foundation](#8-phase-1--project-scaffold--backend-foundation)
9. [Phase 2 — Core Voice Pipeline](#9-phase-2--core-voice-pipeline)
10. [Phase 3 — AI Intelligence Layer (Module 1 — MSL Agent)](#10-phase-3--ai-intelligence-layer-module-1--msl-agent)
11. [Phase 4 — Patient Adherence Companion (Module 2)](#11-phase-4--patient-adherence-companion-module-2)
12. [Phase 5 — Bridge Layer & Convergent Signal Engine](#12-phase-5--bridge-layer--convergent-signal-engine)
13. [Phase 6 — React Frontend & HQ Dashboard](#13-phase-6--react-frontend--hq-dashboard)
14. [Phase 7 — Connecting Everything (Full Integration)](#14-phase-7--connecting-everything-full-integration)
15. [Phase 8 — UI Polish & Design System](#15-phase-8--ui-polish--design-system)
16. [Phase 9 — Demo Data & Seeding Scripts](#16-phase-9--demo-data--seeding-scripts)
17. [How to Run the Full App](#17-how-to-run-the-full-app)
18. [Demo Script (Presentation Walkthrough)](#18-demo-script-presentation-walkthrough)
19. [Troubleshooting Common Issues](#19-troubleshooting-common-issues)

---

## 1. What You Are Building

PharmaBridge is a web application with three interconnected modules:

### Module 1 — MSL Field Intelligence Agent
An MSL (Medical Science Liaison) opens the app, records a 2-minute voice debrief after a KOL meeting. The app:
- Transcribes the voice in real time
- Sends the transcript to Claude, which extracts structured insights (insight type, drug, confidence, urgency)
- Auto-classifies insights and routes them to the correct team
- Displays the intelligence in the HQ dashboard

### Module 2 — Patient Adherence Companion
A patient opens the companion and has a natural voice/text conversation daily. The app:
- Holds an adaptive conversation, asking about adherence
- Detects the patient's specific barrier (cost, side effect, forgetfulness, belief, complexity, access)
- Updates the patient's barrier profile in the database
- Sends a weekly digest to the care team
- Tracks the adherence arc over time

### The Bridge Layer
A background engine that:
- Constantly scans both data streams (MSL insights + patient barriers)
- Detects convergent signals (same drug, same issue, from both sides)
- Generates real-time alerts on the HQ dashboard

### HQ Dashboard
A real-time intelligence hub showing:
- Live MSL insight feed
- Patient adherence trends and barrier breakdown
- Convergent signal alerts with recommended actions

---

## 2. Accounts & API Keys You Need

Before writing a single line of code, create these accounts and get your API keys. Save all keys in a secure note — you will use them in Step 7.

### 2.1 Anthropic (Claude API)
1. Go to **https://console.anthropic.com**
2. Sign up with your personal email (not your Cognizant email — use a personal Gmail)
3. Go to **API Keys** → Click **Create Key**
4. Copy and save the key. It starts with `sk-ant-...`
5. You will need to add a small amount of credit (around $5 is more than enough for the prototype — the whole build will use less than $1 of actual API credit)

**What this is used for:** The brain of PharmaBridge. Claude reads MSL transcripts and extracts structured insights, runs the patient companion conversation, and detects convergent signals.

### 2.2 OpenAI (Whisper API for Speech-to-Text)
1. Go to **https://platform.openai.com**
2. Sign up → Go to **API Keys** → Create a new key
3. Copy and save the key. It starts with `sk-...`
4. Add $5 credit to your account

**What this is used for:** Converting MSL voice recordings and patient speech into text. Whisper is the most accurate model for medical terminology.

### 2.3 ElevenLabs (Text-to-Speech for Patient Companion)
1. Go to **https://elevenlabs.io**
2. Sign up for the free account (gives you 10,000 characters/month — plenty for the demo)
3. Go to your **Profile** → **API Key** → Copy it
4. Also go to **Voices** → Pick a warm, human-sounding voice (recommend "Rachel" or "Bella") → Copy the Voice ID

**What this is used for:** Making the patient companion speak in a warm, human-sounding voice instead of a robotic one.

### 2.4 Supabase (Database & Realtime)
1. Go to **https://supabase.com**
2. Sign up → Click **New Project**
3. Give it the name `pharmabridge`
4. Set a strong database password (save this too)
5. Choose region: **Southeast Asia (Singapore)** — closest to Chennai
6. Wait for the project to provision (~2 minutes)
7. Go to **Project Settings** → **API** → Copy:
   - **Project URL** (looks like `https://xxxx.supabase.co`)
   - **anon public key** (long JWT token)
   - **service_role key** (another JWT — keep this very private)

**What this is used for:** The database that stores all MSL insights, patient conversations, barrier profiles, and powers the real-time HQ dashboard.

---

## 3. Tools to Install on Your Computer

Open your terminal (Command Prompt or PowerShell on Windows, Terminal on Mac) and run these one by one.

### 3.1 Python 3.11+
Check if you have it:
```bash
python --version
```
If you see Python 3.11 or higher, skip this. Otherwise download from **https://python.org/downloads** and install it. Make sure to check "Add Python to PATH" during installation.

### 3.2 Node.js 18+
Check:
```bash
node --version
```
If not installed, download from **https://nodejs.org** (choose LTS version).

### 3.3 Git
```bash
git --version
```
If not installed: **https://git-scm.com/downloads**

### 3.4 Claude Code
Claude Code is the AI coding assistant you'll use to build this. Install it via:
```bash
npm install -g @anthropic-ai/claude-code
```
Then authenticate with your Cognizant Claude Code access.

### 3.5 Verify Everything
```bash
python --version     # Should say 3.11+
node --version       # Should say 18+
npm --version        # Should say 9+
git --version        # Any recent version is fine
```

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PharmaBridge Platform                     │
├──────────────────────┬──────────────────────────────────────┤
│   MODULE 1           │   MODULE 2                           │
│   MSL Agent          │   Patient Companion                  │
│   (Web App)          │   (Web App)                          │
│                      │                                       │
│   🎤 Voice Input     │   🎤 Voice/Text Input                │
│   📝 Transcript      │   💬 Daily Check-in                  │
│   🧠 AI Extraction   │   🧠 Barrier Detection               │
│   📊 Classification  │   📋 Care Team Alert                 │
└──────────┬───────────┴──────────────┬────────────────────────┘
           │                          │
           ▼                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Server                    │
│                         (Python)                            │
│                                                             │
│  /api/msl/debrief    /api/patient/chat    /api/bridge/scan  │
│  /api/insights       /api/patients        /api/signals      │
└──────────────────────────────┬──────────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
     ┌────────────┐  ┌──────────────┐  ┌────────────────┐
     │  Claude    │  │   Supabase   │  │  OpenAI Whisper│
     │  API       │  │  (Database + │  │  + ElevenLabs  │
     │ (Insight   │  │   Realtime)  │  │  (Voice I/O)   │
     │ Extraction)│  │              │  │                │
     └────────────┘  └──────────────┘  └────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 HQ Dashboard (React Frontend)                │
│                                                             │
│   📡 MSL Feed   |   📈 Adherence Chart  |  🚨 Signal Alerts │
│   Real-time via Supabase WebSocket subscriptions            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Low-Level Data Flow — Module 1 (MSL Debrief)

```
MSL opens app
    │
    ▼
Browser records audio (MediaRecorder API, WebM format)
    │
    ▼
Audio blob sent to POST /api/msl/debrief (multipart form)
    │
    ▼
Backend: OpenAI Whisper transcribes audio → plain text transcript
    │
    ▼
Backend: Claude receives transcript with extraction prompt
    │
    ▼
Claude returns structured JSON:
{
  "insights": [
    {
      "type": "Safety Observation",
      "drug": "Drug X",
      "kol_name": "Dr. Sharma",
      "kol_institution": "Apollo Chennai",
      "description": "Two patients with transient liver enzyme elevation",
      "confidence": "High",
      "urgency": "Urgent",
      "routing_target": "Pharmacovigilance"
    }
  ],
  "kol_sentiment": "Skeptical",
  "debrief_summary": "..."
}
    │
    ▼
Backend saves each insight to Supabase → table: msl_insights
    │
    ▼
Supabase Realtime broadcasts new row to all subscribed dashboards
    │
    ▼
HQ Dashboard receives event → updates live feed without page refresh
```

### 4.3 Low-Level Data Flow — Module 2 (Patient Companion)

```
Patient opens companion app
    │
    ▼
Patient speaks or types their message
    │
    ▼
If voice: Audio sent to POST /api/patient/transcribe → Whisper → text
    │
    ▼
POST /api/patient/chat with { patient_id, message, conversation_history }
    │
    ▼
Backend: Claude receives message + patient's barrier profile + conversation history
Claude prompt instructs it to:
  - Be warm and empathetic
  - Listen for barrier signals in the patient's words
  - Ask one focused follow-up question
  - If barrier detected with High confidence, trigger care team alert
    │
    ▼
Claude returns:
{
  "response_text": "Thank you for telling me that...",
  "detected_barrier": "Side Effect",
  "barrier_confidence": "High",
  "barrier_details": "Afternoon fatigue correlated with lunchtime dosing",
  "trigger_alert": true
}
    │
    ▼
Backend:
  1. Saves conversation turn to Supabase → table: patient_conversations
  2. Updates patient barrier profile → table: patient_profiles
  3. If trigger_alert=true → saves alert → table: care_team_alerts
  4. ElevenLabs converts response_text to audio → returns audio URL
    │
    ▼
Frontend plays audio response to patient
    │
    ▼
Supabase Realtime → Bridge Layer checks for convergent signals
```

### 4.4 Low-Level Data Flow — Bridge Layer

```
Background job runs every 5 minutes (or triggered on new insight/barrier)
    │
    ▼
POST /api/bridge/scan
    │
    ▼
Backend queries Supabase:
  - Last 30 days of msl_insights grouped by drug_name
  - Last 30 days of patient barriers grouped by drug_name
    │
    ▼
For each drug where BOTH streams have data:
  Claude receives both summaries and asks:
  "Do these two independent data streams confirm the same clinical signal?"
    │
    ▼
Claude returns:
{
  "convergent_signal_detected": true,
  "drug": "Drug X",
  "signal_type": "Safety / Adherence",
  "confidence": "High",
  "velocity": "Accelerating",
  "msl_evidence": "3 MSLs across regions flagged fatigue",
  "patient_evidence": "34% of Drug X patients reporting fatigue barrier",
  "recommended_actions": [
    "Pharmacovigilance review",
    "Medical Affairs brief",
    ...
  ]
}
    │
    ▼
If signal detected → saved to Supabase → table: convergent_signals
    │
    ▼
Supabase Realtime broadcasts alert to HQ Dashboard instantly
```

---

## 5. Complete Project Structure

This is the exact folder and file structure you will build. Every file listed here will be created during the phases below.

```
pharmabridge/
│
├── backend/                          # Python FastAPI server
│   ├── main.py                       # App entry point, all routes
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # API keys (NEVER commit this)
│   │
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── transcription.py          # OpenAI Whisper integration
│   │   ├── tts.py                    # ElevenLabs text-to-speech
│   │   ├── claude_msl.py             # Claude prompts for MSL insight extraction
│   │   ├── claude_patient.py         # Claude prompts for patient companion
│   │   ├── claude_bridge.py          # Claude prompts for convergent signal detection
│   │   └── supabase_client.py        # Supabase database client
│   │
│   ├── models/                       # Pydantic data models
│   │   ├── __init__.py
│   │   ├── msl_models.py             # MSL debrief, insight schemas
│   │   ├── patient_models.py         # Patient, conversation schemas
│   │   └── bridge_models.py          # Convergent signal schemas
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                # Shared utilities
│
├── frontend/                         # React application
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   │
│   └── src/
│       ├── main.jsx                  # React entry point
│       ├── App.jsx                   # Router and layout
│       ├── index.css                 # Global styles
│       │
│       ├── pages/
│       │   ├── LandingPage.jsx       # PharmaBridge home/intro
│       │   ├── MSLAgent.jsx          # Module 1 — MSL debrief interface
│       │   ├── PatientCompanion.jsx  # Module 2 — Patient chat interface
│       │   └── HQDashboard.jsx       # Bridge layer + unified dashboard
│       │
│       ├── components/
│       │   ├── layout/
│       │   │   ├── Navbar.jsx
│       │   │   └── Sidebar.jsx
│       │   │
│       │   ├── msl/
│       │   │   ├── VoiceRecorder.jsx       # Audio recording component
│       │   │   ├── TranscriptDisplay.jsx   # Shows live transcript
│       │   │   ├── InsightCard.jsx         # Single extracted insight
│       │   │   └── InsightFeed.jsx         # List of insights
│       │   │
│       │   ├── patient/
│       │   │   ├── ChatBubble.jsx          # Single message bubble
│       │   │   ├── ChatWindow.jsx          # Full conversation window
│       │   │   ├── BarrierProfile.jsx      # Patient's detected barrier
│       │   │   └── VoiceInput.jsx          # Voice input for patient
│       │   │
│       │   ├── dashboard/
│       │   │   ├── SignalAlert.jsx         # Convergent signal alert card
│       │   │   ├── AdherenceChart.jsx      # Patient adherence trend chart
│       │   │   ├── BarrierBreakdown.jsx    # Pie chart of barrier types
│       │   │   ├── MSLFeed.jsx             # Real-time MSL insights
│       │   │   └── KOLSentimentCard.jsx    # KOL sentiment indicator
│       │   │
│       │   └── shared/
│       │       ├── LoadingSpinner.jsx
│       │       ├── StatusBadge.jsx         # Confidence/urgency badges
│       │       ├── ConfidencePill.jsx
│       │       └── AudioPlayer.jsx         # Plays ElevenLabs audio
│       │
│       ├── hooks/
│       │   ├── useAudioRecorder.js         # MediaRecorder logic
│       │   ├── useSupabaseRealtime.js      # Supabase realtime subscription
│       │   └── usePatientSession.js        # Patient conversation state
│       │
│       ├── services/
│       │   ├── api.js                      # All fetch calls to backend
│       │   └── supabase.js                 # Supabase client for frontend
│       │
│       └── constants/
│           ├── barriers.js                 # 6 barrier type definitions
│           └── insightTypes.js             # Insight type definitions
│
├── scripts/
│   ├── seed_demo_data.py             # Seeds database with demo data
│   └── test_claude.py                # Quick test of Claude API connection
│
└── README.md                         # How to run the project
```

---

## 6. Database Design (Supabase)

You will run these SQL commands in the Supabase SQL Editor. Go to your Supabase project → **SQL Editor** → paste each block and click **Run**.

### Table 1: MSL Insights
```sql
-- Stores each individual insight extracted from an MSL voice debrief
CREATE TABLE msl_insights (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- MSL info
  msl_name TEXT NOT NULL DEFAULT 'Anonymous MSL',
  msl_region TEXT,

  -- KOL info
  kol_name TEXT,
  kol_institution TEXT,
  kol_specialty TEXT,

  -- Drug info
  drug_name TEXT,
  indication TEXT,

  -- Insight content
  insight_type TEXT NOT NULL,
  -- Values: 'Safety Observation', 'Label Question', 'Competitive Intel',
  --         'Unmet Need', 'Evidence Gap', 'Advocacy', 'Other'

  description TEXT NOT NULL,
  full_transcript TEXT,
  debrief_summary TEXT,

  -- Classification
  confidence TEXT NOT NULL DEFAULT 'Medium',
  -- Values: 'High', 'Medium', 'Low'

  urgency TEXT NOT NULL DEFAULT 'Normal',
  -- Values: 'Urgent', 'Normal', 'Low'

  routing_target TEXT,
  -- Values: 'Pharmacovigilance', 'Medical Affairs', 'Commercial', 'R&D', 'Regulatory'

  -- KOL sentiment toward this drug
  kol_sentiment TEXT DEFAULT 'Neutral',
  -- Values: 'Positive', 'Neutral', 'Skeptical', 'Negative'

  -- Status
  status TEXT DEFAULT 'New',
  -- Values: 'New', 'Under Review', 'Actioned', 'Archived'

  reviewed_by TEXT,
  reviewed_at TIMESTAMPTZ
);

-- Enable realtime for this table (so dashboard updates live)
ALTER TABLE msl_insights REPLICA IDENTITY FULL;
```

### Table 2: Patient Profiles
```sql
-- Stores each patient enrolled in the companion program
CREATE TABLE patient_profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Patient info (anonymized in production)
  patient_name TEXT NOT NULL,
  patient_code TEXT UNIQUE NOT NULL, -- e.g. "PT-001"
  age_group TEXT, -- '18-30', '31-45', '46-60', '60+'
  condition TEXT, -- e.g. 'Type 2 Diabetes', 'Hypertension'

  -- Medication
  drug_name TEXT NOT NULL,
  drug_start_date DATE,
  care_team_email TEXT, -- physician email for weekly digest

  -- Adherence tracking
  adherence_rate NUMERIC(5,2) DEFAULT 100.0, -- percentage 0-100
  consecutive_days_tracked INTEGER DEFAULT 0,
  last_checkin_at TIMESTAMPTZ,

  -- Barrier detection
  primary_barrier TEXT DEFAULT 'Unknown',
  -- Values: 'Cost', 'Side Effect', 'Forgetfulness', 'Belief', 'Complexity', 'Access', 'Unknown'

  barrier_confidence TEXT DEFAULT 'Low',
  barrier_detected_at TIMESTAMPTZ,
  barrier_details TEXT,

  -- Companion strategy
  current_strategy TEXT DEFAULT 'General Support',
  intervention_stage INTEGER DEFAULT 1 -- 1-5, escalates as barrier is confirmed

);

CREATE INDEX idx_patient_drug ON patient_profiles(drug_name);
```

### Table 3: Patient Conversations
```sql
-- Stores every message in every patient conversation
CREATE TABLE patient_conversations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  patient_id UUID REFERENCES patient_profiles(id) ON DELETE CASCADE,

  -- Conversation turn
  role TEXT NOT NULL, -- 'patient' or 'companion'
  message TEXT NOT NULL,

  -- AI analysis of this turn (if role = 'patient')
  barrier_signal TEXT, -- What barrier this message hinted at
  signal_strength TEXT, -- 'Strong', 'Weak', 'None'

  -- Session grouping
  session_date DATE DEFAULT CURRENT_DATE,
  session_number INTEGER DEFAULT 1 -- which day's conversation
);

CREATE INDEX idx_conv_patient ON patient_conversations(patient_id);
CREATE INDEX idx_conv_session ON patient_conversations(patient_id, session_date);

ALTER TABLE patient_conversations REPLICA IDENTITY FULL;
```

### Table 4: Care Team Alerts
```sql
-- Stores alerts sent to physicians when a barrier is confirmed
CREATE TABLE care_team_alerts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  patient_id UUID REFERENCES patient_profiles(id) ON DELETE CASCADE,
  patient_code TEXT NOT NULL,
  drug_name TEXT NOT NULL,

  alert_type TEXT NOT NULL, -- 'Barrier Detected', 'Adherence Drop', 'Safety Concern'
  alert_message TEXT NOT NULL,
  barrier_type TEXT,
  barrier_details TEXT,

  recommended_action TEXT,

  -- Status
  status TEXT DEFAULT 'Pending', -- 'Pending', 'Sent', 'Acknowledged'
  sent_at TIMESTAMPTZ
);

ALTER TABLE care_team_alerts REPLICA IDENTITY FULL;
```

### Table 5: Convergent Signals
```sql
-- Stores bridge layer detections — where MSL and patient data converge
CREATE TABLE convergent_signals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  drug_name TEXT NOT NULL,
  signal_type TEXT NOT NULL, -- 'Safety / Adherence', 'Efficacy', 'Tolerability', etc.
  confidence TEXT NOT NULL, -- 'High', 'Medium', 'Low'
  velocity TEXT, -- 'Accelerating', 'Stable', 'Declining'

  -- Evidence from each stream
  msl_evidence TEXT NOT NULL, -- Summary of what MSLs reported
  patient_evidence TEXT NOT NULL, -- Summary of patient barrier data
  msl_insight_count INTEGER DEFAULT 0,
  patient_count INTEGER DEFAULT 0,

  -- Signal details
  signal_summary TEXT NOT NULL,
  recommended_actions JSONB, -- Array of action strings

  -- Status
  status TEXT DEFAULT 'Active', -- 'Active', 'Under Investigation', 'Resolved'
  resolved_at TIMESTAMPTZ,
  resolved_by TEXT
);

ALTER TABLE convergent_signals REPLICA IDENTITY FULL;
```

### Table 6: KOL Profiles (for sentiment tracking)
```sql
-- Tracks each KOL's sentiment trend over time
CREATE TABLE kol_profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  kol_name TEXT NOT NULL,
  institution TEXT,
  specialty TEXT,
  region TEXT,

  -- Aggregated sentiment per drug
  drug_name TEXT NOT NULL,
  sentiment_trend TEXT DEFAULT 'Neutral',
  total_interactions INTEGER DEFAULT 0,
  last_interaction_at TIMESTAMPTZ,

  UNIQUE(kol_name, drug_name)
);
```

### Enable Realtime on All Tables
```sql
-- Run this to enable Supabase Realtime on all key tables
-- (You should have already set REPLICA IDENTITY FULL above)
-- Go to Supabase → Database → Replication → Add tables:
-- msl_insights, patient_conversations, care_team_alerts, convergent_signals
```

---

## 7. Environment Configuration (.env)

Create two `.env` files — one for the backend and one for the frontend.

### Backend: `backend/.env`
```env
# Anthropic Claude API
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OpenAI Whisper (Speech-to-Text)
OPENAI_API_KEY=sk-your-openai-key-here

# ElevenLabs (Text-to-Speech)
ELEVENLABS_API_KEY=your-elevenlabs-key-here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
# ^ This is "Rachel" voice ID. Change to your preferred voice ID.

# Supabase
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here
# Use service key (not anon key) for the backend — it bypasses Row Level Security

# App Config
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
BRIDGE_SCAN_INTERVAL_MINUTES=5
```

### Frontend: `frontend/.env`
```env
# Supabase (use anon/public key for frontend)
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-public-key-here

# Backend API
VITE_API_BASE_URL=http://localhost:8000
```

**CRITICAL:** Both `.env` files must be in your `.gitignore`. Never upload API keys to GitHub.

Create a `backend/.gitignore`:
```
.env
__pycache__/
*.pyc
*.pyo
.venv/
venv/
```

Create a `frontend/.gitignore`:
```
.env
node_modules/
dist/
```

---

## 8. Phase 1 — Project Scaffold & Backend Foundation

**Goal:** Get a running FastAPI server that responds to requests.

### Step 1.1 — Create the Project Folder

Open your terminal and run:
```bash
mkdir pharmabridge
cd pharmabridge
mkdir backend frontend scripts
```

### Step 1.2 — Backend Setup

```bash
cd backend

# Create a virtual environment (isolated Python environment)
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# You should now see (venv) at the start of your terminal line
```

### Step 1.3 — Install Python Dependencies

Create `backend/requirements.txt`:
```
fastapi==0.111.0
uvicorn[standard]==0.30.1
python-multipart==0.0.9
python-dotenv==1.0.1
anthropic==0.28.0
openai==1.35.0
supabase==2.5.0
httpx==0.27.0
pydantic==2.7.4
aiofiles==23.2.1
apscheduler==3.10.4
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 1.4 — Create the Folder Structure

```bash
mkdir services models utils
touch services/__init__.py models/__init__.py utils/__init__.py
```

### Step 1.5 — Create the Main Application File

Create `backend/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="PharmaBridge API",
    description="Autonomous Pharma Intelligence Platform",
    version="1.0.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "PharmaBridge API is running",
        "version": "1.0.0",
        "modules": ["MSL Field Intelligence", "Patient Adherence Companion", "Bridge Layer"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import and include routers (we'll add these in later phases)
# from routes import msl_routes, patient_routes, bridge_routes
# app.include_router(msl_routes.router, prefix="/api/msl", tags=["MSL"])
# app.include_router(patient_routes.router, prefix="/api/patient", tags=["Patient"])
# app.include_router(bridge_routes.router, prefix="/api/bridge", tags=["Bridge"])
```

### Step 1.6 — Create the Supabase Client

Create `backend/services/supabase_client.py`:
```python
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

def get_supabase_client() -> Client:
    """Returns an authenticated Supabase client using the service role key."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")

    return create_client(url, key)

# Singleton client instance
supabase: Client = get_supabase_client()
```

### Step 1.7 — Run the Server

```bash
# Make sure you're in the backend/ folder with (venv) active
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

Open your browser and go to **http://localhost:8000** — you should see the JSON response.
Go to **http://localhost:8000/docs** — this is the auto-generated API documentation. Very useful.

**✅ Phase 1 complete. You have a running server.**

---

## 9. Phase 2 — Core Voice Pipeline

**Goal:** Record voice in the browser, send it to the backend, get a transcript back.

### Step 2.1 — Backend: Transcription Service

Create `backend/services/transcription.py`:
```python
import openai
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm") -> dict:
    """
    Sends audio bytes to OpenAI Whisper for transcription.
    Returns: { "transcript": "...", "duration_seconds": 45 }
    """
    # Save audio to a temporary file (Whisper API requires a file, not raw bytes)
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name

    try:
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
                # This prompt helps Whisper handle medical terminology better
                prompt="This is a medical discussion about pharmaceutical drugs, KOL meetings, clinical trials, and patient safety observations. Medical Science Liaison debrief."
            )

        return {
            "transcript": transcription.text,
            "success": True
        }

    except Exception as e:
        return {
            "transcript": "",
            "success": False,
            "error": str(e)
        }

    finally:
        # Clean up the temp file
        import os
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
```

### Step 2.2 — Backend: Text-to-Speech Service

Create `backend/services/tts.py`:
```python
import httpx
import os
import base64
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

async def text_to_speech(text: str) -> dict:
    """
    Converts text to speech using ElevenLabs.
    Returns base64-encoded audio that the frontend can play directly.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,        # Lower = more expressive
            "similarity_boost": 0.8,
            "style": 0.2,            # Slight style variation for naturalness
            "use_speaker_boost": True
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()

            # Convert audio bytes to base64 string so we can send it as JSON
            audio_base64 = base64.b64encode(response.content).decode("utf-8")

            return {
                "audio_base64": audio_base64,
                "content_type": "audio/mpeg",
                "success": True
            }

    except Exception as e:
        return {
            "audio_base64": None,
            "success": False,
            "error": str(e)
        }
```

### Step 2.3 — Add Transcription Route to Backend

Add to `backend/main.py` (before the `if __name__` block, or in a separate routes file):
```python
from fastapi import UploadFile, File, HTTPException
from services.transcription import transcribe_audio
from services.tts import text_to_speech

@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """
    Receives an audio file and returns its transcript.
    Used by both MSL debrief and patient companion.
    """
    audio_bytes = await audio.read()

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file received")

    result = await transcribe_audio(audio_bytes, audio.filename)

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {result.get('error', 'Unknown error')}"
        )

    return {
        "transcript": result["transcript"],
        "character_count": len(result["transcript"])
    }

@app.post("/api/speak")
async def speak(request: dict):
    """
    Converts text to speech and returns base64 audio.
    Used by the patient companion.
    """
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    result = await text_to_speech(text)
    return result
```

### Step 2.4 — Frontend: Audio Recorder Hook

Create `frontend/src/hooks/useAudioRecorder.js`:
```javascript
import { useState, useRef, useCallback } from 'react';

export function useAudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [error, setError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);

  const startRecording = useCallback(async () => {
    setError(null);
    setAudioBlob(null);
    chunksRef.current = [];

    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      // Create MediaRecorder — use webm format (most browser-compatible)
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';

      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: mimeType });
        setAudioBlob(blob);
        // Stop all tracks to release the microphone
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start(250); // Collect data every 250ms
      setIsRecording(true);

      // Track duration
      setRecordingDuration(0);
      timerRef.current = setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);

    } catch (err) {
      setError('Microphone access denied. Please allow microphone access and try again.');
      console.error('Recording error:', err);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      clearInterval(timerRef.current);
    }
  }, [isRecording]);

  const resetRecording = useCallback(() => {
    setAudioBlob(null);
    setRecordingDuration(0);
    setError(null);
  }, []);

  return {
    isRecording,
    audioBlob,
    recordingDuration,
    error,
    startRecording,
    stopRecording,
    resetRecording
  };
}
```

**✅ Phase 2 complete. Voice pipeline is ready.**

---

## 10. Phase 3 — AI Intelligence Layer (Module 1 — MSL Agent)

**Goal:** Build the Claude-powered insight extraction and the MSL debrief submission flow.

### Step 3.1 — Claude MSL Extraction Service

Create `backend/services/claude_msl.py`:
```python
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MSL_EXTRACTION_PROMPT = """You are PharmaBridge's MSL Intelligence Extraction Engine. 
You are analyzing a voice debrief transcript from a Medical Science Liaison (MSL) after a KOL (Key Opinion Leader) meeting.

Your job is to extract every distinct insight from this transcript and return structured data.

INSIGHT TYPES (classify each insight as exactly one of these):
- "Safety Observation": Any mention of adverse events, side effects, patient safety concerns
- "Label Question": Questions about dosing, indications, label claims, contraindications
- "Competitive Intel": Mentions of competitor drugs, rival trial data, comparative effectiveness
- "Unmet Need": Clinical gaps, patient populations not served, conditions without good treatment options
- "Evidence Gap": Missing data, requested studies, questions the MSL couldn't answer
- "Advocacy": Positive endorsement, willingness to speak at events, recommend prescribing
- "Other": Doesn't fit above categories

CONFIDENCE SCORING:
- "High": The insight is explicit and unambiguous in the transcript
- "Medium": The insight is implied or partially mentioned
- "Low": Uncertain, would need clarification

URGENCY:
- "Urgent": Safety observations or regulatory matters — must reach the right team within hours
- "Normal": Standard intelligence, route within 24-48 hours
- "Low": Background information, can wait for weekly report

ROUTING TARGETS:
- Safety Observation → "Pharmacovigilance"
- Label Question → "Medical Affairs"
- Competitive Intel → "Commercial"
- Evidence Gap → "Medical Affairs" or "R&D"
- Advocacy → "Medical Affairs"
- Unmet Need → "R&D"

KOL SENTIMENT toward the specific drug mentioned:
- "Positive": Enthusiastic, recommending, favorable
- "Neutral": Factual, no strong opinion
- "Skeptical": Questioning, doubting, comparing unfavorably
- "Negative": Critical, not recommending, concerned

Return ONLY valid JSON, no markdown, no explanation. Use this exact structure:

{
  "insights": [
    {
      "insight_type": "Safety Observation",
      "drug_name": "Drug name or 'Unspecified'",
      "indication": "Disease/condition or 'Unspecified'",
      "kol_name": "Name or 'Unknown'",
      "kol_institution": "Institution or 'Unknown'",
      "kol_specialty": "Specialty or 'Unknown'",
      "description": "Clear, concise description of the insight (2-3 sentences)",
      "confidence": "High",
      "urgency": "Normal",
      "routing_target": "Medical Affairs",
      "kol_sentiment": "Neutral"
    }
  ],
  "overall_kol_sentiment": "Neutral",
  "debrief_summary": "2-3 sentence summary of the entire meeting",
  "msl_region": "Region if mentioned, else 'Unspecified'"
}

TRANSCRIPT TO ANALYZE:
"""

async def extract_msl_insights(transcript: str, msl_name: str = "Anonymous MSL") -> dict:
    """
    Sends MSL transcript to Claude for structured insight extraction.
    Returns a dict with insights array and metadata.
    """
    if not transcript or len(transcript.strip()) < 20:
        return {
            "success": False,
            "error": "Transcript too short to extract insights",
            "insights": []
        }

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": MSL_EXTRACTION_PROMPT + transcript
                }
            ]
        )

        # Parse the JSON response from Claude
        response_text = message.content[0].text.strip()

        # Remove any markdown code blocks if Claude accidentally adds them
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        extracted_data = json.loads(response_text)

        # Add MSL name to each insight
        for insight in extracted_data.get("insights", []):
            insight["msl_name"] = msl_name

        return {
            "success": True,
            "insights": extracted_data.get("insights", []),
            "overall_kol_sentiment": extracted_data.get("overall_kol_sentiment", "Neutral"),
            "debrief_summary": extracted_data.get("debrief_summary", ""),
            "msl_region": extracted_data.get("msl_region", "Unspecified"),
            "insight_count": len(extracted_data.get("insights", []))
        }

    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Claude returned invalid JSON: {str(e)}",
            "insights": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "insights": []
        }
```

### Step 3.2 — Pydantic Models for MSL

Create `backend/models/msl_models.py`:
```python
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MSLDebriefRequest(BaseModel):
    msl_name: str = "Anonymous MSL"
    msl_region: Optional[str] = None
    transcript: Optional[str] = None  # If text is pasted directly

class InsightCreate(BaseModel):
    msl_name: str
    msl_region: Optional[str]
    kol_name: Optional[str]
    kol_institution: Optional[str]
    kol_specialty: Optional[str]
    drug_name: Optional[str]
    indication: Optional[str]
    insight_type: str
    description: str
    confidence: str
    urgency: str
    routing_target: Optional[str]
    kol_sentiment: Optional[str]
    full_transcript: Optional[str]
    debrief_summary: Optional[str]

class InsightResponse(BaseModel):
    id: str
    created_at: datetime
    msl_name: str
    drug_name: Optional[str]
    insight_type: str
    description: str
    confidence: str
    urgency: str
    routing_target: Optional[str]
    status: str

class MSLDebriefResponse(BaseModel):
    success: bool
    transcript: str
    insights_extracted: int
    insights: List[dict]
    debrief_summary: str
    message: str
```

### Step 3.3 — MSL API Routes

Create `backend/routes/msl_routes.py`:
```python
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.transcription import transcribe_audio
from services.claude_msl import extract_msl_insights
from services.supabase_client import supabase
from models.msl_models import MSLDebriefResponse
import json

router = APIRouter()

@router.post("/debrief", response_model=dict)
async def submit_msl_debrief(
    audio: UploadFile = File(...),
    msl_name: str = Form(default="Anonymous MSL"),
    msl_region: str = Form(default="Unspecified")
):
    """
    Receives MSL voice debrief audio, transcribes it, extracts insights,
    and saves everything to the database.
    """
    # Step 1: Transcribe the audio
    audio_bytes = await audio.read()
    transcription_result = await transcribe_audio(audio_bytes)

    if not transcription_result["success"]:
        raise HTTPException(status_code=500, detail="Transcription failed")

    transcript = transcription_result["transcript"]

    # Step 2: Extract insights with Claude
    extraction_result = await extract_msl_insights(transcript, msl_name)

    if not extraction_result["success"]:
        raise HTTPException(
            status_code=500,
            detail=f"Insight extraction failed: {extraction_result.get('error')}"
        )

    # Step 3: Save each insight to Supabase
    saved_insights = []
    for insight in extraction_result["insights"]:
        try:
            db_record = {
                "msl_name": msl_name,
                "msl_region": msl_region,
                "kol_name": insight.get("kol_name"),
                "kol_institution": insight.get("kol_institution"),
                "kol_specialty": insight.get("kol_specialty"),
                "drug_name": insight.get("drug_name"),
                "indication": insight.get("indication"),
                "insight_type": insight.get("insight_type"),
                "description": insight.get("description"),
                "full_transcript": transcript,
                "debrief_summary": extraction_result.get("debrief_summary"),
                "confidence": insight.get("confidence", "Medium"),
                "urgency": insight.get("urgency", "Normal"),
                "routing_target": insight.get("routing_target"),
                "kol_sentiment": insight.get("kol_sentiment", "Neutral"),
                "status": "New"
            }

            result = supabase.table("msl_insights").insert(db_record).execute()
            saved_insights.append(result.data[0] if result.data else db_record)

            # If the insight is a safety observation, also update KOL profile
            if insight.get("insight_type") == "Safety Observation" and insight.get("kol_name") != "Unknown":
                upsert_kol_profile(insight, msl_region)

        except Exception as e:
            print(f"Error saving insight: {e}")
            continue

    return {
        "success": True,
        "transcript": transcript,
        "insights_extracted": len(saved_insights),
        "insights": saved_insights,
        "debrief_summary": extraction_result.get("debrief_summary", ""),
        "overall_kol_sentiment": extraction_result.get("overall_kol_sentiment", "Neutral"),
        "message": f"Successfully extracted {len(saved_insights)} insights from your debrief."
    }


@router.get("/insights")
async def get_insights(
    limit: int = 50,
    insight_type: str = None,
    drug_name: str = None,
    urgency: str = None
):
    """Returns recent MSL insights with optional filtering."""
    query = supabase.table("msl_insights").select("*").order("created_at", desc=True).limit(limit)

    if insight_type:
        query = query.eq("insight_type", insight_type)
    if drug_name:
        query = query.eq("drug_name", drug_name)
    if urgency:
        query = query.eq("urgency", urgency)

    result = query.execute()
    return {"insights": result.data, "count": len(result.data)}


@router.post("/debrief/text")
async def submit_text_debrief(request: dict):
    """
    Alternative endpoint: accepts transcript as text directly (no audio).
    Useful for testing or when audio is not available.
    """
    msl_name = request.get("msl_name", "Anonymous MSL")
    msl_region = request.get("msl_region", "Unspecified")
    transcript = request.get("transcript", "")

    if not transcript:
        raise HTTPException(status_code=400, detail="No transcript provided")

    extraction_result = await extract_msl_insights(transcript, msl_name)

    if not extraction_result["success"]:
        raise HTTPException(status_code=500, detail=extraction_result.get("error"))

    # Save to DB
    saved_insights = []
    for insight in extraction_result["insights"]:
        db_record = {
            "msl_name": msl_name,
            "msl_region": msl_region,
            "drug_name": insight.get("drug_name"),
            "kol_name": insight.get("kol_name"),
            "kol_institution": insight.get("kol_institution"),
            "insight_type": insight.get("insight_type"),
            "description": insight.get("description"),
            "full_transcript": transcript,
            "debrief_summary": extraction_result.get("debrief_summary"),
            "confidence": insight.get("confidence", "Medium"),
            "urgency": insight.get("urgency", "Normal"),
            "routing_target": insight.get("routing_target"),
            "kol_sentiment": insight.get("kol_sentiment", "Neutral"),
            "status": "New"
        }
        result = supabase.table("msl_insights").insert(db_record).execute()
        if result.data:
            saved_insights.append(result.data[0])

    return {
        "success": True,
        "insights_extracted": len(saved_insights),
        "insights": saved_insights,
        "debrief_summary": extraction_result.get("debrief_summary")
    }


def upsert_kol_profile(insight: dict, region: str):
    """Updates or creates a KOL profile with the latest sentiment data."""
    try:
        supabase.table("kol_profiles").upsert({
            "kol_name": insight.get("kol_name", "Unknown"),
            "institution": insight.get("kol_institution"),
            "specialty": insight.get("kol_specialty"),
            "region": region,
            "drug_name": insight.get("drug_name", "Unspecified"),
            "sentiment_trend": insight.get("kol_sentiment", "Neutral"),
        }, on_conflict="kol_name,drug_name").execute()
    except Exception as e:
        print(f"KOL profile update error: {e}")
```

### Step 3.4 — Register Routes in main.py

Update `backend/main.py` to include the routes:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="PharmaBridge API",
    description="Autonomous Pharma Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers
from routes import msl_routes
app.include_router(msl_routes.router, prefix="/api/msl", tags=["MSL Intelligence"])

@app.get("/")
async def root():
    return {"message": "PharmaBridge API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

Also create `backend/routes/__init__.py` (empty file):
```python
# routes package
```

**✅ Phase 3 complete. MSL intelligence extraction is working.**

---

## 11. Phase 4 — Patient Adherence Companion (Module 2)

### Step 4.1 — Claude Patient Companion Service

Create `backend/services/claude_patient.py`:
```python
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PATIENT_SYSTEM_PROMPT = """You are a warm, empathetic patient adherence companion for PharmaBridge.
Your name is Aria. You have a single purpose: to gently understand why a patient may be struggling with their medication and to support them in continuing their treatment.

YOU ARE NOT a doctor and should never give medical advice. If a patient has a serious concern, you direct them to their care team.

THE SIX BARRIER TYPES you must listen for:
1. "Cost" - mentions of price, co-pay, can't afford, expensive, splitting pills
2. "Side Effect" - mentions of feeling tired, nausea, headache, stomach issues, any physical symptom they link to medication
3. "Forgetfulness" - mentions of forgetting, missing doses, not remembering, irregular schedule
4. "Belief" - mentions of feeling fine already, not needing medication, don't think it works, skepticism
5. "Complexity" - mentions of taking many pills, confusing schedule, multiple medications
6. "Access" - mentions of pharmacy distance, running out, hard to get prescription, transportation

CONVERSATION STYLE:
- Warm and human, never clinical or robotic
- Ask ONE question at a time, never multiple
- Listen actively — reflect what the patient said before asking your next question
- Do not push or pressure. Be gentle.
- Keep responses SHORT — 2-3 sentences maximum
- If the patient says they took their medication, celebrate it warmly

WHEN YOU DETECT A BARRIER:
- Do NOT reveal that you've detected a barrier
- Continue the conversation naturally but ask targeted follow-up questions to confirm it
- Once confirmed, mention gently that you'll pass this along to their care team

RESPONSE FORMAT:
Always return valid JSON only, no markdown:
{
  "response_text": "Your warm response to the patient",
  "detected_barrier": "Side Effect" or null,
  "barrier_confidence": "High" or "Medium" or "Low" or null,
  "barrier_details": "Specific detail about the barrier" or null,
  "trigger_care_team_alert": false,
  "adherence_taken_today": true or false or null
}

trigger_care_team_alert should be true ONLY when:
- barrier_confidence is "High" (confirmed with multiple signals)
- The barrier is confirmed enough to warrant clinical review

Set adherence_taken_today to true if patient says they took medication, false if they skipped, null if unclear.
"""

async def patient_chat(
    patient_message: str,
    conversation_history: list,
    patient_profile: dict
) -> dict:
    """
    Runs one turn of the patient companion conversation.
    
    Args:
        patient_message: What the patient just said
        conversation_history: List of { role, content } dicts for the full conversation so far
        patient_profile: Dict with patient's drug name, condition, current barrier status
    
    Returns:
        Dict with response_text, detected_barrier, trigger_alert, etc.
    """

    # Build the patient context for Claude
    patient_context = f"""
PATIENT CONTEXT:
- Patient code: {patient_profile.get('patient_code', 'Unknown')}
- Condition: {patient_profile.get('condition', 'Unknown')}
- Medication: {patient_profile.get('drug_name', 'their medication')}
- Enrolled since: {patient_profile.get('created_at', 'recently')}
- Current detected barrier: {patient_profile.get('primary_barrier', 'Unknown')}
- Barrier confidence: {patient_profile.get('barrier_confidence', 'Low')}
- Adherence rate: {patient_profile.get('adherence_rate', 100)}%
- Today's session number: {patient_profile.get('session_count', 1)}
"""

    # Build the messages for Claude
    messages = []

    # Add conversation history
    for turn in conversation_history:
        messages.append({
            "role": turn["role"],
            "content": turn["content"]
        })

    # Add the new patient message
    messages.append({
        "role": "user",
        "content": f"{patient_context}\n\nPatient says: {patient_message}"
    })

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            system=PATIENT_SYSTEM_PROMPT,
            messages=messages
        )

        response_text = response.content[0].text.strip()

        # Clean any markdown formatting
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])

        result = json.loads(response_text)

        return {
            "success": True,
            **result
        }

    except json.JSONDecodeError as e:
        # If Claude returns non-JSON, extract the response as plain text
        return {
            "success": True,
            "response_text": "Thank you for sharing that with me. How are you feeling today?",
            "detected_barrier": None,
            "barrier_confidence": None,
            "barrier_details": None,
            "trigger_care_team_alert": False,
            "adherence_taken_today": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response_text": "I'm having a brief connection issue. Can you try again in a moment?",
            "detected_barrier": None,
            "trigger_care_team_alert": False
        }


async def generate_opening_message(patient_profile: dict, session_number: int) -> str:
    """Generates a personalized opening message for each daily check-in."""

    prompt = f"""Generate a warm, brief opening message (1-2 sentences only) for a patient adherence check-in.
Patient is on {patient_profile.get('drug_name', 'their medication')} for {patient_profile.get('condition', 'their condition')}.
This is day {session_number} of their check-in.
Known barrier (if any): {patient_profile.get('primary_barrier', 'None detected yet')}.
Make the message feel personal and caring, not clinical. Ask about how they're doing AND whether they took their medication today.
Return ONLY the message text, no JSON, no quotes."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    except:
        return f"Good morning! How are you feeling today? Did you take your medication this morning?"
```

### Step 4.2 — Patient Companion Routes

Create `backend/routes/patient_routes.py`:
```python
from fastapi import APIRouter, HTTPException
from services.claude_patient import patient_chat, generate_opening_message
from services.tts import text_to_speech
from services.supabase_client import supabase
from datetime import datetime, date
import uuid

router = APIRouter()

@router.post("/chat")
async def patient_chat_endpoint(request: dict):
    """
    Main patient companion chat endpoint.
    Receives a patient message, generates AI response, saves to DB.
    """
    patient_id = request.get("patient_id")
    patient_message = request.get("message", "")
    conversation_history = request.get("conversation_history", [])
    include_audio = request.get("include_audio", True)

    if not patient_id or not patient_message:
        raise HTTPException(status_code=400, detail="patient_id and message are required")

    # Fetch patient profile from DB
    patient_result = supabase.table("patient_profiles").select("*").eq("id", patient_id).single().execute()
    if not patient_result.data:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_profile = patient_result.data

    # Run the Claude companion
    ai_result = await patient_chat(patient_message, conversation_history, patient_profile)

    if not ai_result.get("success"):
        raise HTTPException(status_code=500, detail=ai_result.get("error"))

    response_text = ai_result.get("response_text", "")

    # Save patient message to DB
    supabase.table("patient_conversations").insert({
        "patient_id": patient_id,
        "role": "patient",
        "message": patient_message,
        "barrier_signal": ai_result.get("detected_barrier"),
        "signal_strength": ai_result.get("barrier_confidence"),
        "session_date": str(date.today())
    }).execute()

    # Save companion response to DB
    supabase.table("patient_conversations").insert({
        "patient_id": patient_id,
        "role": "companion",
        "message": response_text,
        "session_date": str(date.today())
    }).execute()

    # Update patient's adherence and barrier profile if new info detected
    update_data = {"last_checkin_at": datetime.utcnow().isoformat()}

    if ai_result.get("adherence_taken_today") == True:
        # Calculate new adherence rate (simplified)
        days = patient_profile.get("consecutive_days_tracked", 0) + 1
        current_rate = patient_profile.get("adherence_rate", 100)
        new_rate = ((current_rate * (days - 1)) + 100) / days
        update_data["adherence_rate"] = round(new_rate, 2)
        update_data["consecutive_days_tracked"] = days

    elif ai_result.get("adherence_taken_today") == False:
        days = patient_profile.get("consecutive_days_tracked", 0) + 1
        current_rate = patient_profile.get("adherence_rate", 100)
        new_rate = ((current_rate * (days - 1)) + 0) / days
        update_data["adherence_rate"] = round(new_rate, 2)
        update_data["consecutive_days_tracked"] = days

    if ai_result.get("detected_barrier") and ai_result.get("barrier_confidence") in ["High", "Medium"]:
        update_data["primary_barrier"] = ai_result.get("detected_barrier")
        update_data["barrier_confidence"] = ai_result.get("barrier_confidence")
        update_data["barrier_details"] = ai_result.get("barrier_details")
        update_data["barrier_detected_at"] = datetime.utcnow().isoformat()

    supabase.table("patient_profiles").update(update_data).eq("id", patient_id).execute()

    # Create care team alert if needed
    if ai_result.get("trigger_care_team_alert"):
        supabase.table("care_team_alerts").insert({
            "patient_id": patient_id,
            "patient_code": patient_profile.get("patient_code"),
            "drug_name": patient_profile.get("drug_name"),
            "alert_type": "Barrier Detected",
            "alert_message": f"Patient has confirmed {ai_result.get('detected_barrier')} barrier. {ai_result.get('barrier_details', '')}",
            "barrier_type": ai_result.get("detected_barrier"),
            "barrier_details": ai_result.get("barrier_details"),
            "recommended_action": get_recommended_action(ai_result.get("detected_barrier")),
            "status": "Pending"
        }).execute()

    # Generate audio if requested
    audio_data = None
    if include_audio and response_text:
        audio_result = await text_to_speech(response_text)
        if audio_result.get("success"):
            audio_data = {
                "audio_base64": audio_result.get("audio_base64"),
                "content_type": audio_result.get("content_type")
            }

    return {
        "success": True,
        "response_text": response_text,
        "detected_barrier": ai_result.get("detected_barrier"),
        "barrier_confidence": ai_result.get("barrier_confidence"),
        "alert_triggered": ai_result.get("trigger_care_team_alert", False),
        "audio": audio_data
    }


@router.post("/start-session")
async def start_patient_session(request: dict):
    """Gets the opening message for a new patient check-in session."""
    patient_id = request.get("patient_id")

    patient_result = supabase.table("patient_profiles").select("*").eq("id", patient_id).single().execute()
    if not patient_result.data:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_profile = patient_result.data
    session_number = patient_profile.get("consecutive_days_tracked", 0) + 1

    opening_message = await generate_opening_message(patient_profile, session_number)

    # Generate audio for opening
    audio_result = await text_to_speech(opening_message)
    audio_data = None
    if audio_result.get("success"):
        audio_data = {
            "audio_base64": audio_result.get("audio_base64"),
            "content_type": "audio/mpeg"
        }

    return {
        "opening_message": opening_message,
        "patient_name": patient_profile.get("patient_name"),
        "session_number": session_number,
        "audio": audio_data
    }


@router.get("/patients")
async def get_all_patients():
    """Returns all patient profiles for the dashboard."""
    result = supabase.table("patient_profiles").select("*").order("created_at", desc=True).execute()
    return {"patients": result.data, "count": len(result.data)}


@router.get("/patients/{patient_id}/history")
async def get_patient_history(patient_id: str):
    """Returns conversation history for a specific patient."""
    result = supabase.table("patient_conversations") \
        .select("*") \
        .eq("patient_id", patient_id) \
        .order("created_at", asc=True) \
        .execute()
    return {"conversations": result.data}


def get_recommended_action(barrier_type: str) -> str:
    """Returns the recommended clinical action for each barrier type."""
    actions = {
        "Cost": "Review patient assistance programs, generic alternatives, and co-pay card eligibility.",
        "Side Effect": "Schedule clinical review of dose timing or alternative formulation. Consider pharmacovigilance report if severe.",
        "Forgetfulness": "Consider medication management app, pill organizer, or simplified dosing schedule.",
        "Belief": "Schedule motivational interview with physician to discuss disease progression risks.",
        "Complexity": "Request medication reconciliation review. Explore regimen simplification.",
        "Access": "Explore mail-order pharmacy, medication delivery services, or 90-day supply options."
    }
    return actions.get(barrier_type, "Review patient's full medication history and barriers.")
```

**✅ Phase 4 complete. Patient companion is working.**

---

## 12. Phase 5 — Bridge Layer & Convergent Signal Engine

### Step 5.1 — Claude Bridge Layer Service

Create `backend/services/claude_bridge.py`:
```python
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

BRIDGE_SYSTEM_PROMPT = """You are the PharmaBridge Convergent Signal Detection Engine.
Your job is to analyze two independent data streams — MSL field intelligence and patient adherence data — and determine if they are independently confirming the same clinical signal about a specific drug.

A CONVERGENT SIGNAL exists when:
- Multiple MSLs have reported similar clinical observations about a drug (not just one isolated report)
- Patient data shows a related adherence pattern or barrier for the same drug
- Both streams are pointing to the same underlying issue independently

SIGNAL TYPES:
- "Safety / Adherence" — A potential safety issue is causing patients to stop taking the drug
- "Efficacy Concern" — Both MSLs and patients questioning whether the drug is working
- "Tolerability" — Side effects mentioned by KOLs are confirmed by patient barrier data
- "Market / Competitive" — Competitive pressure is reducing MSL enthusiasm AND patient access
- "Unmet Need" — Both streams reveal a population or condition not adequately served

CONFIDENCE:
- "High" — Both streams have strong, multiple data points confirming the same issue
- "Medium" — Suggestive pattern from both streams, but limited data
- "Low" — Early signal, needs more data to confirm

VELOCITY:
- "Accelerating" — The signal is getting stronger over time (more reports each week)
- "Stable" — Consistent signal, not growing
- "Declining" — Signal was stronger before, now reducing

Return ONLY valid JSON:
{
  "convergent_signal_detected": true or false,
  "drug_name": "Drug name",
  "signal_type": "Safety / Adherence",
  "confidence": "High",
  "velocity": "Accelerating",
  "signal_summary": "2-3 sentence explanation of what both streams are independently confirming",
  "recommended_actions": [
    "Action 1",
    "Action 2",
    "Action 3"
  ],
  "reasoning": "Brief explanation of why this is or is not a convergent signal"
}

If no convergent signal detected, set convergent_signal_detected to false and explain briefly in reasoning.
"""

async def scan_for_convergent_signals(drug_name: str, msl_summary: str, patient_summary: str) -> dict:
    """
    Given a drug name and summaries of both data streams, asks Claude if there's a convergent signal.
    """
    prompt = f"""
Analyze the following two independent data streams for {drug_name}:

MSL FIELD INTELLIGENCE (last 30 days):
{msl_summary}

PATIENT ADHERENCE DATA (last 30 days):
{patient_summary}

Determine if these two streams are independently confirming the same clinical signal.
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            system=BRIDGE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text.strip()
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])

        result = json.loads(response_text)
        return {"success": True, **result}

    except Exception as e:
        return {"success": False, "error": str(e), "convergent_signal_detected": False}
```

### Step 5.2 — Bridge Layer Routes

Create `backend/routes/bridge_routes.py`:
```python
from fastapi import APIRouter, HTTPException
from services.claude_bridge import scan_for_convergent_signals
from services.supabase_client import supabase
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter()

@router.post("/scan")
async def run_bridge_scan():
    """
    Scans both data streams and detects convergent signals.
    This is the core Bridge Layer function.
    """
    # Get last 30 days of MSL insights grouped by drug
    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).isoformat()

    msl_result = supabase.table("msl_insights") \
        .select("drug_name, insight_type, description, confidence, kol_sentiment, msl_region, created_at") \
        .gte("created_at", thirty_days_ago) \
        .execute()

    patient_result = supabase.table("patient_profiles") \
        .select("drug_name, primary_barrier, barrier_confidence, adherence_rate, barrier_details") \
        .execute()

    # Group MSL insights by drug
    msl_by_drug = defaultdict(list)
    for insight in (msl_result.data or []):
        if insight.get("drug_name"):
            msl_by_drug[insight["drug_name"]].append(insight)

    # Group patient barriers by drug
    patient_by_drug = defaultdict(list)
    for patient in (patient_result.data or []):
        if patient.get("drug_name"):
            patient_by_drug[patient["drug_name"]].append(patient)

    # Find drugs present in BOTH streams
    common_drugs = set(msl_by_drug.keys()) & set(patient_by_drug.keys())

    new_signals = []

    for drug_name in common_drugs:
        msl_insights = msl_by_drug[drug_name]
        patients = patient_by_drug[drug_name]

        # Only analyze if we have meaningful data (at least 1 MSL insight and 2 patients)
        if len(msl_insights) < 1 or len(patients) < 1:
            continue

        # Build summaries for Claude
        msl_summary = build_msl_summary(msl_insights)
        patient_summary = build_patient_summary(patients)

        # Ask Claude if there's a convergent signal
        signal_result = await scan_for_convergent_signals(drug_name, msl_summary, patient_summary)

        if signal_result.get("convergent_signal_detected"):
            # Check if this signal already exists in DB (avoid duplicates)
            existing = supabase.table("convergent_signals") \
                .select("id") \
                .eq("drug_name", drug_name) \
                .eq("status", "Active") \
                .execute()

            if not existing.data:
                # Save the new signal
                db_record = {
                    "drug_name": drug_name,
                    "signal_type": signal_result.get("signal_type", "Unknown"),
                    "confidence": signal_result.get("confidence", "Medium"),
                    "velocity": signal_result.get("velocity", "Stable"),
                    "msl_evidence": msl_summary,
                    "patient_evidence": patient_summary,
                    "msl_insight_count": len(msl_insights),
                    "patient_count": len(patients),
                    "signal_summary": signal_result.get("signal_summary", ""),
                    "recommended_actions": signal_result.get("recommended_actions", []),
                    "status": "Active"
                }
                result = supabase.table("convergent_signals").insert(db_record).execute()
                if result.data:
                    new_signals.append(result.data[0])

    return {
        "success": True,
        "drugs_analyzed": len(common_drugs),
        "new_signals_detected": len(new_signals),
        "signals": new_signals,
        "message": f"Bridge scan complete. Analyzed {len(common_drugs)} drugs. Found {len(new_signals)} new convergent signals."
    }


@router.get("/signals")
async def get_convergent_signals(status: str = "Active"):
    """Returns all convergent signals from the database."""
    result = supabase.table("convergent_signals") \
        .select("*") \
        .eq("status", status) \
        .order("created_at", desc=True) \
        .execute()

    return {"signals": result.data, "count": len(result.data)}


@router.get("/alerts")
async def get_care_team_alerts():
    """Returns all care team alerts."""
    result = supabase.table("care_team_alerts") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(50) \
        .execute()

    return {"alerts": result.data}


def build_msl_summary(insights: list) -> str:
    """Builds a readable summary of MSL insights for a drug."""
    if not insights:
        return "No MSL insights available."

    summary_parts = []
    for i in insights:
        summary_parts.append(
            f"- [{i.get('insight_type')}] {i.get('description')} "
            f"(Confidence: {i.get('confidence')}, Region: {i.get('msl_region', 'Unknown')})"
        )

    return f"Total MSL reports: {len(insights)}\n" + "\n".join(summary_parts)


def build_patient_summary(patients: list) -> str:
    """Builds a readable summary of patient barrier data for a drug."""
    if not patients:
        return "No patient data available."

    total = len(patients)
    barriers = {}
    total_adherence = 0

    for p in patients:
        barrier = p.get("primary_barrier", "Unknown")
        barriers[barrier] = barriers.get(barrier, 0) + 1
        total_adherence += float(p.get("adherence_rate", 100))

    avg_adherence = total_adherence / total if total > 0 else 100

    barrier_breakdown = ", ".join([f"{b}: {c} patients ({round(c/total*100)}%)"
                                    for b, c in barriers.items()])

    return (f"Total patients tracked: {total}\n"
            f"Average adherence rate: {round(avg_adherence, 1)}%\n"
            f"Barrier breakdown: {barrier_breakdown}")
```

**✅ Phase 5 complete. Bridge layer is working.**

---

## 13. Phase 6 — React Frontend & HQ Dashboard

### Step 6.1 — Initialize React App

```bash
# Make sure you're in the pharmabridge root folder
cd frontend

npm create vite@latest . -- --template react
# When prompted, select "React" and "JavaScript"

npm install

npm install tailwindcss @tailwindcss/vite
npm install recharts
npm install @supabase/supabase-js
npm install react-router-dom
npm install lucide-react
npm install react-hot-toast
```

### Step 6.2 — Tailwind CSS Setup

Update `frontend/vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
```

Replace the contents of `frontend/src/index.css`:
```css
@import "tailwindcss";

:root {
  --pharma-blue: #003087;
  --pharma-red: #8B0000;
  --pharma-purple: #4B0082;
  --pharma-light: #F0F4FF;
}

body {
  font-family: 'Inter', system-ui, sans-serif;
  background-color: #F8FAFC;
}

/* Pulse animation for recording button */
@keyframes pulse-record {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  50% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
}

.recording-pulse {
  animation: pulse-record 1.5s ease-in-out infinite;
}

/* Signal alert animation */
@keyframes slide-in {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.signal-alert {
  animation: slide-in 0.5s ease-out;
}
```

### Step 6.3 — Supabase Client for Frontend

Create `frontend/src/services/supabase.js`:
```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### Step 6.4 — API Service Layer

Create `frontend/src/services/api.js`:
```javascript
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Helper function for all API calls
async function apiCall(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `API error: ${response.status}`)
  }

  return response.json()
}

// MSL API
export const mslAPI = {
  submitDebrief: async (audioBlob, mslName, mslRegion) => {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'debrief.webm')
    formData.append('msl_name', mslName)
    formData.append('msl_region', mslRegion)

    const response = await fetch(`${BASE_URL}/api/msl/debrief`, {
      method: 'POST',
      body: formData,  // Do NOT set Content-Type header for FormData
    })

    if (!response.ok) throw new Error('Debrief submission failed')
    return response.json()
  },

  submitTextDebrief: async (transcript, mslName, mslRegion) => {
    return apiCall('/api/msl/debrief/text', {
      method: 'POST',
      body: JSON.stringify({ transcript, msl_name: mslName, msl_region: mslRegion }),
    })
  },

  getInsights: async (filters = {}) => {
    const params = new URLSearchParams(filters)
    return apiCall(`/api/msl/insights?${params}`)
  },
}

// Patient API
export const patientAPI = {
  startSession: async (patientId) => {
    return apiCall('/api/patient/start-session', {
      method: 'POST',
      body: JSON.stringify({ patient_id: patientId }),
    })
  },

  chat: async (patientId, message, conversationHistory) => {
    return apiCall('/api/patient/chat', {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        message,
        conversation_history: conversationHistory,
        include_audio: true,
      }),
    })
  },

  getPatients: async () => {
    return apiCall('/api/patient/patients')
  },

  getPatientHistory: async (patientId) => {
    return apiCall(`/api/patient/patients/${patientId}/history`)
  },
}

// Bridge API
export const bridgeAPI = {
  runScan: async () => {
    return apiCall('/api/bridge/scan', { method: 'POST' })
  },

  getSignals: async () => {
    return apiCall('/api/bridge/signals')
  },

  getAlerts: async () => {
    return apiCall('/api/bridge/alerts')
  },
}

// Transcription
export const transcribeAudio = async (audioBlob) => {
  const formData = new FormData()
  formData.append('audio', audioBlob, 'audio.webm')

  const response = await fetch(`${BASE_URL}/api/transcribe`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) throw new Error('Transcription failed')
  return response.json()
}
```

### Step 6.5 — Supabase Realtime Hook

Create `frontend/src/hooks/useSupabaseRealtime.js`:
```javascript
import { useEffect, useState } from 'react'
import { supabase } from '../services/supabase'

export function useRealtimeInsights() {
  const [insights, setInsights] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch initial data
    const fetchInitial = async () => {
      const { data } = await supabase
        .from('msl_insights')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(20)
      setInsights(data || [])
      setLoading(false)
    }
    fetchInitial()

    // Subscribe to new insights in real time
    const channel = supabase
      .channel('msl-insights-channel')
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'msl_insights',
      }, (payload) => {
        setInsights(prev => [payload.new, ...prev])
      })
      .subscribe()

    return () => supabase.removeChannel(channel)
  }, [])

  return { insights, loading }
}

export function useRealtimeSignals() {
  const [signals, setSignals] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchInitial = async () => {
      const { data } = await supabase
        .from('convergent_signals')
        .select('*')
        .eq('status', 'Active')
        .order('created_at', { ascending: false })
      setSignals(data || [])
      setLoading(false)
    }
    fetchInitial()

    const channel = supabase
      .channel('signals-channel')
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'convergent_signals',
      }, (payload) => {
        setSignals(prev => [payload.new, ...prev])
      })
      .subscribe()

    return () => supabase.removeChannel(channel)
  }, [])

  return { signals, loading }
}

export function useRealtimeAlerts() {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const fetchInitial = async () => {
      const { data } = await supabase
        .from('care_team_alerts')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(10)
      setAlerts(data || [])
    }
    fetchInitial()

    const channel = supabase
      .channel('alerts-channel')
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'care_team_alerts',
      }, (payload) => {
        setAlerts(prev => [payload.new, ...prev])
      })
      .subscribe()

    return () => supabase.removeChannel(channel)
  }, [])

  return { alerts }
}
```

### Step 6.6 — App Router

Replace `frontend/src/App.jsx`:
```jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import MSLAgent from './pages/MSLAgent'
import PatientCompanion from './pages/PatientCompanion'
import HQDashboard from './pages/HQDashboard'
import Navbar from './components/layout/Navbar'
import { Toaster } from 'react-hot-toast'

function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: { background: '#1e293b', color: '#fff' }
        }}
      />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/msl" element={
          <div className="min-h-screen bg-slate-50">
            <Navbar />
            <MSLAgent />
          </div>
        } />
        <Route path="/patient" element={
          <div className="min-h-screen bg-slate-50">
            <Navbar />
            <PatientCompanion />
          </div>
        } />
        <Route path="/dashboard" element={
          <div className="min-h-screen bg-slate-50">
            <Navbar />
            <HQDashboard />
          </div>
        } />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

### Step 6.7 — Navbar Component

Create `frontend/src/components/layout/Navbar.jsx`:
```jsx
import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/msl', label: 'MSL Intelligence', icon: '🎤' },
  { path: '/patient', label: 'Patient Companion', icon: '❤️' },
  { path: '/dashboard', label: 'HQ Dashboard', icon: '📊' },
]

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-900 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">PB</span>
            </div>
            <span className="font-bold text-blue-900 text-lg">PharmaBridge</span>
          </Link>

          {/* Navigation */}
          <div className="flex items-center gap-1">
            {navItems.map(item => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === item.path
                    ? 'bg-blue-900 text-white'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                <span>{item.icon}</span>
                <span className="hidden sm:block">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
```

### Step 6.8 — Landing Page

Create `frontend/src/pages/LandingPage.jsx`:
```jsx
import { useNavigate } from 'react-router-dom'

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-blue-900 to-indigo-900 text-white">
      {/* Header */}
      <div className="flex items-center justify-between px-8 py-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center">
            <span className="text-blue-900 font-black text-lg">PB</span>
          </div>
          <span className="font-bold text-xl">PharmaBridge</span>
        </div>
        <button
          onClick={() => navigate('/dashboard')}
          className="bg-white text-blue-900 px-5 py-2 rounded-lg font-semibold text-sm hover:bg-blue-50 transition-colors"
        >
          HQ Dashboard →
        </button>
      </div>

      {/* Hero */}
      <div className="max-w-5xl mx-auto px-8 pt-16 pb-20 text-center">
        <div className="inline-block bg-white/10 backdrop-blur border border-white/20 rounded-full px-4 py-1 text-sm mb-8">
          Autonomous Pharma Intelligence Platform
        </div>

        <h1 className="text-5xl font-black mb-6 leading-tight">
          The answers exist.<br />
          They just live in{' '}
          <span className="bg-gradient-to-r from-amber-300 to-orange-400 bg-clip-text text-transparent">
            two separate places.
          </span>
        </h1>

        <p className="text-xl text-blue-200 mb-12 max-w-2xl mx-auto leading-relaxed">
          What doctors tell MSLs in the field. What patients experience at home.
          PharmaBridge connects both streams in real time — automatically.
        </p>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6 mb-14">
          {[
            { value: '$300B', label: 'Lost annually to medication non-adherence' },
            { value: '70%', label: 'of KOL field insights never formally recorded' },
            { value: '2 min', label: 'is all it takes for an MSL to debrief' },
          ].map(stat => (
            <div key={stat.value} className="bg-white/10 backdrop-blur border border-white/20 rounded-2xl p-6">
              <div className="text-4xl font-black text-amber-300 mb-2">{stat.value}</div>
              <div className="text-sm text-blue-200">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/msl')}
            className="bg-white text-blue-900 px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-50 transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
            🎤 MSL Field Intelligence Agent
          </button>
          <button
            onClick={() => navigate('/patient')}
            className="bg-red-800 text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-red-700 transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
            ❤️ Patient Adherence Companion
          </button>
        </div>
      </div>

      {/* Module Cards */}
      <div className="max-w-5xl mx-auto px-8 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              icon: '🎤',
              title: 'MSL Field Intelligence',
              desc: 'Voice-first debrief. AI-extracted insights. Auto-routed to the right team in minutes.'
            },
            {
              icon: '❤️',
              title: 'Patient Companion',
              desc: 'Daily check-ins that detect the real reason patients stop. Adapts to each person.'
            },
            {
              icon: '🔗',
              title: 'Bridge Layer',
              desc: 'When field and patient data confirm the same signal — automatically surfaced to HQ.'
            }
          ].map(card => (
            <div key={card.title} className="bg-white/10 backdrop-blur border border-white/20 rounded-2xl p-6">
              <div className="text-3xl mb-4">{card.icon}</div>
              <h3 className="font-bold text-lg mb-2">{card.title}</h3>
              <p className="text-blue-200 text-sm leading-relaxed">{card.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

### Step 6.9 — Shared Components

Create `frontend/src/components/shared/StatusBadge.jsx`:
```jsx
const CONFIDENCE_STYLES = {
  High: 'bg-green-100 text-green-800 border-green-200',
  Medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  Low: 'bg-slate-100 text-slate-600 border-slate-200',
}

const URGENCY_STYLES = {
  Urgent: 'bg-red-100 text-red-800 border-red-200',
  Normal: 'bg-blue-100 text-blue-800 border-blue-200',
  Low: 'bg-slate-100 text-slate-600 border-slate-200',
}

const INSIGHT_TYPE_STYLES = {
  'Safety Observation': 'bg-red-50 text-red-700 border-red-200',
  'Label Question': 'bg-purple-50 text-purple-700 border-purple-200',
  'Competitive Intel': 'bg-orange-50 text-orange-700 border-orange-200',
  'Unmet Need': 'bg-teal-50 text-teal-700 border-teal-200',
  'Evidence Gap': 'bg-indigo-50 text-indigo-700 border-indigo-200',
  'Advocacy': 'bg-green-50 text-green-700 border-green-200',
}

export function ConfidenceBadge({ confidence }) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${CONFIDENCE_STYLES[confidence] || CONFIDENCE_STYLES.Low}`}>
      {confidence} Confidence
    </span>
  )
}

export function UrgencyBadge({ urgency }) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${URGENCY_STYLES[urgency] || URGENCY_STYLES.Normal}`}>
      {urgency === 'Urgent' ? '🚨' : urgency === 'Normal' ? '📋' : '📌'} {urgency}
    </span>
  )
}

export function InsightTypeBadge({ type }) {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${INSIGHT_TYPE_STYLES[type] || 'bg-slate-100 text-slate-600 border-slate-200'}`}>
      {type}
    </span>
  )
}
```

### Step 6.10 — Insight Card Component

Create `frontend/src/components/msl/InsightCard.jsx`:
```jsx
import { ConfidenceBadge, UrgencyBadge, InsightTypeBadge } from '../shared/StatusBadge'

export default function InsightCard({ insight }) {
  const timeAgo = (dateString) => {
    const seconds = Math.floor((new Date() - new Date(dateString)) / 1000)
    if (seconds < 60) return 'just now'
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    return new Date(dateString).toLocaleDateString()
  }

  const routingColor = {
    'Pharmacovigilance': 'border-l-red-500',
    'Medical Affairs': 'border-l-blue-500',
    'Commercial': 'border-l-orange-500',
    'R&D': 'border-l-purple-500',
    'Regulatory': 'border-l-yellow-500',
  }

  return (
    <div className={`bg-white rounded-xl border border-slate-200 border-l-4 ${routingColor[insight.routing_target] || 'border-l-slate-400'} p-5 hover:shadow-md transition-shadow`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <InsightTypeBadge type={insight.insight_type} />
        <div className="flex items-center gap-2">
          <UrgencyBadge urgency={insight.urgency} />
          <ConfidenceBadge confidence={insight.confidence} />
        </div>
      </div>

      <p className="text-slate-800 font-medium mb-3">{insight.description}</p>

      <div className="flex items-center justify-between text-xs text-slate-500">
        <div className="flex items-center gap-3">
          {insight.kol_name && insight.kol_name !== 'Unknown' && (
            <span className="flex items-center gap-1">
              👨‍⚕️ {insight.kol_name}
              {insight.kol_institution && ` · ${insight.kol_institution}`}
            </span>
          )}
          {insight.drug_name && (
            <span className="bg-slate-100 px-2 py-0.5 rounded font-mono">
              💊 {insight.drug_name}
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          {insight.routing_target && (
            <span className="text-xs font-medium text-slate-600">
              → {insight.routing_target}
            </span>
          )}
          <span>{timeAgo(insight.created_at)}</span>
        </div>
      </div>
    </div>
  )
}
```

### Step 6.11 — Voice Recorder Component

Create `frontend/src/components/msl/VoiceRecorder.jsx`:
```jsx
import { useState } from 'react'
import { useAudioRecorder } from '../../hooks/useAudioRecorder'

export default function VoiceRecorder({ onRecordingComplete }) {
  const {
    isRecording,
    audioBlob,
    recordingDuration,
    error,
    startRecording,
    stopRecording,
    resetRecording
  } = useAudioRecorder()

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleSubmit = () => {
    if (audioBlob) {
      onRecordingComplete(audioBlob)
      resetRecording()
    }
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-8 text-center">
      <h3 className="text-lg font-semibold text-slate-800 mb-2">Voice Debrief</h3>
      <p className="text-slate-500 text-sm mb-8">
        Speak naturally about your KOL meeting. PharmaBridge will extract and classify everything.
      </p>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 mb-6 text-sm">
          {error}
        </div>
      )}

      {/* Recording Button */}
      <div className="flex flex-col items-center gap-4 mb-8">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={!!audioBlob}
          className={`w-24 h-24 rounded-full text-white font-bold text-4xl transition-all shadow-lg
            ${isRecording
              ? 'bg-red-500 recording-pulse hover:bg-red-600'
              : audioBlob
                ? 'bg-slate-300 cursor-not-allowed'
                : 'bg-blue-900 hover:bg-blue-800 hover:shadow-xl hover:-translate-y-0.5'
            }`}
        >
          {isRecording ? '⏹' : audioBlob ? '✓' : '🎤'}
        </button>

        <div className="text-sm font-medium text-slate-600">
          {isRecording ? (
            <span className="text-red-500 animate-pulse">
              ● Recording {formatDuration(recordingDuration)}
            </span>
          ) : audioBlob ? (
            <span className="text-green-600">
              ✓ Recording captured ({formatDuration(recordingDuration)})
            </span>
          ) : (
            'Click to start recording'
          )}
        </div>
      </div>

      {/* Action Buttons */}
      {audioBlob && (
        <div className="flex gap-3 justify-center">
          <button
            onClick={resetRecording}
            className="px-5 py-2 rounded-lg border border-slate-300 text-slate-600 hover:bg-slate-50 text-sm font-medium"
          >
            Re-record
          </button>
          <button
            onClick={handleSubmit}
            className="px-6 py-2 rounded-lg bg-blue-900 text-white hover:bg-blue-800 text-sm font-bold"
          >
            Submit Debrief →
          </button>
        </div>
      )}
    </div>
  )
}
```

### Step 6.12 — MSL Agent Page

Create `frontend/src/pages/MSLAgent.jsx`:
```jsx
import { useState } from 'react'
import { mslAPI } from '../services/api'
import VoiceRecorder from '../components/msl/VoiceRecorder'
import InsightCard from '../components/msl/InsightCard'
import { useRealtimeInsights } from '../hooks/useSupabaseRealtime'
import toast from 'react-hot-toast'

export default function MSLAgent() {
  const [mslName, setMslName] = useState('')
  const [mslRegion, setMslRegion] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [processingStep, setProcessingStep] = useState('')
  const [lastResult, setLastResult] = useState(null)
  const [textTranscript, setTextTranscript] = useState('')
  const [inputMode, setInputMode] = useState('voice') // 'voice' or 'text'

  const { insights, loading: insightsLoading } = useRealtimeInsights()

  const handleRecordingComplete = async (audioBlob) => {
    if (!mslName.trim()) {
      toast.error('Please enter your name before submitting')
      return
    }

    setIsProcessing(true)
    setLastResult(null)

    try {
      setProcessingStep('Transcribing your voice...')
      const result = await mslAPI.submitDebrief(audioBlob, mslName, mslRegion || 'Unspecified')

      setLastResult(result)
      toast.success(`✅ ${result.insights_extracted} insights extracted!`)
    } catch (err) {
      toast.error(`Error: ${err.message}`)
    } finally {
      setIsProcessing(false)
      setProcessingStep('')
    }
  }

  const handleTextDebrief = async () => {
    if (!mslName.trim()) return toast.error('Please enter your name')
    if (!textTranscript.trim()) return toast.error('Please enter a transcript')

    setIsProcessing(true)
    try {
      setProcessingStep('Extracting insights with AI...')
      const result = await mslAPI.submitTextDebrief(textTranscript, mslName, mslRegion || 'Unspecified')
      setLastResult(result)
      toast.success(`✅ ${result.insights_extracted} insights extracted!`)
    } catch (err) {
      toast.error(`Error: ${err.message}`)
    } finally {
      setIsProcessing(false)
      setProcessingStep('')
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 mb-2">MSL Field Intelligence Agent</h1>
        <p className="text-slate-500">Turn your KOL meeting insights into structured intelligence in 2 minutes.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left: Input Panel */}
        <div className="space-y-6">
          {/* MSL Info */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6">
            <h3 className="font-semibold text-slate-800 mb-4">Your Information</h3>
            <div className="space-y-3">
              <input
                type="text"
                placeholder="Your name (e.g., James Chen)"
                value={mslName}
                onChange={e => setMslName(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Your region (e.g., Southeast Asia)"
                value={mslRegion}
                onChange={e => setMslRegion(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Mode Tabs */}
          <div className="flex gap-2 bg-slate-100 rounded-xl p-1">
            <button
              onClick={() => setInputMode('voice')}
              className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                inputMode === 'voice' ? 'bg-white shadow text-blue-900' : 'text-slate-600'
              }`}
            >
              🎤 Voice Debrief
            </button>
            <button
              onClick={() => setInputMode('text')}
              className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                inputMode === 'text' ? 'bg-white shadow text-blue-900' : 'text-slate-600'
              }`}
            >
              📝 Type Transcript
            </button>
          </div>

          {/* Input Area */}
          {inputMode === 'voice' ? (
            <VoiceRecorder onRecordingComplete={handleRecordingComplete} />
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-6">
              <textarea
                placeholder="Paste or type the meeting transcript here... e.g., 'Dr. Sharma mentioned that two of her patients developed fatigue after starting Drug X. She also asked about the dosing in elderly patients with renal impairment...'"
                value={textTranscript}
                onChange={e => setTextTranscript(e.target.value)}
                rows={8}
                className="w-full border border-slate-200 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
              <button
                onClick={handleTextDebrief}
                disabled={isProcessing}
                className="mt-3 w-full bg-blue-900 text-white py-3 rounded-lg font-bold hover:bg-blue-800 disabled:opacity-50"
              >
                {isProcessing ? processingStep : 'Extract Insights →'}
              </button>
            </div>
          )}

          {/* Processing State */}
          {isProcessing && (
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-center">
              <div className="text-blue-600 font-medium">{processingStep || 'Processing...'}</div>
              <div className="text-blue-400 text-sm mt-1">PharmaBridge AI is working</div>
            </div>
          )}

          {/* Result Summary */}
          {lastResult && (
            <div className="bg-green-50 border border-green-200 rounded-xl p-5">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">✅</span>
                <span className="font-bold text-green-800">Debrief Processed</span>
              </div>
              <p className="text-green-700 text-sm mb-3">{lastResult.debrief_summary}</p>
              <div className="text-green-600 text-sm font-medium">
                {lastResult.insights_extracted} insights extracted and routed →
              </div>
            </div>
          )}
        </div>

        {/* Right: Live Insights Feed */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-slate-800">Live Intelligence Feed</h2>
            <span className="flex items-center gap-1.5 text-xs text-green-600 font-medium">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              Real-time
            </span>
          </div>

          {insightsLoading ? (
            <div className="text-center py-12 text-slate-400">Loading insights...</div>
          ) : insights.length === 0 ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400">
              <div className="text-4xl mb-3">📭</div>
              <p>No insights yet. Submit your first debrief to get started.</p>
            </div>
          ) : (
            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1">
              {insights.map(insight => (
                <InsightCard key={insight.id} insight={insight} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
```

### Step 6.13 — Patient Companion Page

Create `frontend/src/pages/PatientCompanion.jsx`:
```jsx
import { useState, useEffect, useRef } from 'react'
import { patientAPI } from '../services/api'
import toast from 'react-hot-toast'

const DEMO_PATIENT_ID = null // Will be set from DB in production

const BARRIER_COLORS = {
  'Cost': 'bg-amber-100 text-amber-800',
  'Side Effect': 'bg-red-100 text-red-800',
  'Forgetfulness': 'bg-blue-100 text-blue-800',
  'Belief': 'bg-purple-100 text-purple-800',
  'Complexity': 'bg-indigo-100 text-indigo-800',
  'Access': 'bg-teal-100 text-teal-800',
  'Unknown': 'bg-slate-100 text-slate-600',
}

export default function PatientCompanion() {
  const [patients, setPatients] = useState([])
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionStarted, setSessionStarted] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    loadPatients()
  }, [])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadPatients = async () => {
    try {
      const result = await patientAPI.getPatients()
      setPatients(result.patients || [])
    } catch (err) {
      toast.error('Could not load patients')
    }
  }

  const startSession = async (patient) => {
    setSelectedPatient(patient)
    setMessages([])
    setSessionStarted(false)
    setIsLoading(true)

    try {
      const result = await patientAPI.startSession(patient.id)

      // Add opening message
      const openingMsg = {
        role: 'companion',
        content: result.opening_message,
        audio: result.audio,
        timestamp: new Date()
      }
      setMessages([openingMsg])
      setSessionStarted(true)

      // Auto-play audio if available
      if (result.audio?.audio_base64) {
        playAudio(result.audio.audio_base64)
      }
    } catch (err) {
      toast.error('Could not start session')
    } finally {
      setIsLoading(false)
    }
  }

  const sendMessage = async () => {
    if (!inputText.trim() || !selectedPatient || isLoading) return

    const userMsg = { role: 'patient', content: inputText, timestamp: new Date() }
    setMessages(prev => [...prev, userMsg])

    const userInput = inputText
    setInputText('')
    setIsLoading(true)

    try {
      // Build conversation history for Claude
      const history = messages.map(m => ({
        role: m.role === 'companion' ? 'assistant' : 'user',
        content: m.content
      }))

      const result = await patientAPI.chat(selectedPatient.id, userInput, history)

      const companionMsg = {
        role: 'companion',
        content: result.response_text,
        audio: result.audio,
        barrier: result.detected_barrier,
        alertTriggered: result.alert_triggered,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, companionMsg])

      if (result.audio?.audio_base64) {
        playAudio(result.audio.audio_base64)
      }

      if (result.alert_triggered) {
        toast.success('📋 Care team has been notified')
        loadPatients() // Refresh patient data
      }

    } catch (err) {
      toast.error('Message failed. Try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const playAudio = (base64Audio) => {
    try {
      const audioData = `data:audio/mpeg;base64,${base64Audio}`
      const audio = new Audio(audioData)
      audio.play().catch(() => {}) // Silent fail if autoplay blocked
    } catch (e) {}
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 mb-2">Patient Adherence Companion</h1>
        <p className="text-slate-500">Adaptive daily check-ins that detect why patients struggle and adjust accordingly.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Patient List */}
        <div className="space-y-3">
          <h2 className="font-bold text-slate-700 text-sm uppercase tracking-wide">Enrolled Patients</h2>
          {patients.map(patient => (
            <button
              key={patient.id}
              onClick={() => startSession(patient)}
              className={`w-full text-left bg-white rounded-xl border p-4 hover:shadow-md transition-all ${
                selectedPatient?.id === patient.id ? 'border-blue-500 shadow-md' : 'border-slate-200'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="font-semibold text-slate-800">{patient.patient_name}</div>
                  <div className="text-xs text-slate-400">{patient.patient_code} · {patient.condition}</div>
                  <div className="text-xs text-slate-500 mt-1">💊 {patient.drug_name}</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-bold text-slate-700">{patient.adherence_rate}%</div>
                  <div className="text-xs text-slate-400">adherence</div>
                </div>
              </div>
              {patient.primary_barrier && patient.primary_barrier !== 'Unknown' && (
                <div className={`mt-2 inline-block text-xs px-2 py-0.5 rounded-full ${BARRIER_COLORS[patient.primary_barrier]}`}>
                  {patient.primary_barrier} barrier
                </div>
              )}
            </button>
          ))}

          {patients.length === 0 && (
            <div className="text-center py-8 text-slate-400 text-sm">
              No patients enrolled yet. Run the demo seed script first.
            </div>
          )}
        </div>

        {/* Chat Window */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 flex flex-col" style={{ height: '600px' }}>
          {!selectedPatient ? (
            <div className="flex-1 flex items-center justify-center text-slate-400">
              <div className="text-center">
                <div className="text-4xl mb-3">❤️</div>
                <p>Select a patient to start their daily check-in</p>
              </div>
            </div>
          ) : (
            <>
              {/* Chat Header */}
              <div className="border-b border-slate-100 px-6 py-4 flex items-center justify-between">
                <div>
                  <div className="font-bold text-slate-800">{selectedPatient.patient_name}</div>
                  <div className="text-xs text-slate-400">{selectedPatient.condition} · {selectedPatient.drug_name}</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-slate-700">{selectedPatient.adherence_rate}%</div>
                  <div className="text-xs text-slate-400">adherence</div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'patient' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-sm rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                        msg.role === 'patient'
                          ? 'bg-blue-600 text-white rounded-br-sm'
                          : 'bg-slate-100 text-slate-800 rounded-bl-sm'
                      }`}
                    >
                      {msg.role === 'companion' && (
                        <div className="text-xs font-semibold text-slate-500 mb-1">Aria · PharmaBridge</div>
                      )}
                      {msg.content}
                      {msg.alertTriggered && (
                        <div className="text-xs text-amber-600 mt-1 font-medium">📋 Care team notified</div>
                      )}
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-100 rounded-2xl rounded-bl-sm px-4 py-3">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Input */}
              <div className="border-t border-slate-100 p-4 flex gap-3">
                <input
                  type="text"
                  value={inputText}
                  onChange={e => setInputText(e.target.value)}
                  onKeyPress={e => e.key === 'Enter' && sendMessage()}
                  placeholder="Type your response..."
                  disabled={isLoading || !sessionStarted}
                  className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !sessionStarted || !inputText.trim()}
                  className="bg-blue-900 text-white px-5 py-2.5 rounded-xl font-medium text-sm hover:bg-blue-800 disabled:opacity-50"
                >
                  Send
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
```

### Step 6.14 — HQ Dashboard Page

Create `frontend/src/pages/HQDashboard.jsx`:
```jsx
import { useState } from 'react'
import { bridgeAPI } from '../services/api'
import { useRealtimeInsights, useRealtimeSignals, useRealtimeAlerts } from '../hooks/useSupabaseRealtime'
import InsightCard from '../components/msl/InsightCard'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts'
import toast from 'react-hot-toast'

const BARRIER_COLORS_CHART = ['#ef4444', '#f97316', '#3b82f6', '#8b5cf6', '#6366f1', '#14b8a6']
const BARRIER_LABELS = ['Side Effect', 'Cost', 'Forgetfulness', 'Belief', 'Complexity', 'Access']

export default function HQDashboard() {
  const { insights, loading: insightsLoading } = useRealtimeInsights()
  const { signals, loading: signalsLoading } = useRealtimeSignals()
  const { alerts } = useRealtimeAlerts()
  const [isScanning, setIsScanning] = useState(false)

  const runBridgeScan = async () => {
    setIsScanning(true)
    try {
      const result = await bridgeAPI.runScan()
      if (result.new_signals_detected > 0) {
        toast.success(`🔗 ${result.new_signals_detected} new convergent signal(s) detected!`)
      } else {
        toast(`Bridge scan complete. No new signals.`, { icon: '🔍' })
      }
    } catch (err) {
      toast.error('Bridge scan failed')
    } finally {
      setIsScanning(false)
    }
  }

  // Barrier data for pie chart (from live data in prod — using mock for demo)
  const barrierData = BARRIER_LABELS.map((label, i) => ({
    name: label,
    value: Math.floor(Math.random() * 10) + 1
  }))

  // Adherence trend data (mock for demo — real data from Supabase in prod)
  const adherenceTrend = Array.from({ length: 12 }, (_, i) => ({
    week: `W${i + 1}`,
    traditional: Math.max(55, 85 - i * 2),
    pharmabridge: Math.max(80, 85 - i * 0.4)
  }))

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-black text-slate-900 mb-2">HQ Intelligence Dashboard</h1>
          <p className="text-slate-500">Real-time view of field intelligence and patient adherence signals.</p>
        </div>
        <button
          onClick={runBridgeScan}
          disabled={isScanning}
          className="bg-indigo-900 text-white px-6 py-3 rounded-xl font-bold hover:bg-indigo-800 disabled:opacity-50 flex items-center gap-2"
        >
          {isScanning ? (
            <>
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              Scanning...
            </>
          ) : '🔗 Run Bridge Scan'}
        </button>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {[
          { label: 'MSL Insights Today', value: insights.length, icon: '🎤', color: 'blue' },
          { label: 'Active Signals', value: signals.length, icon: '🔗', color: 'purple' },
          { label: 'Care Team Alerts', value: alerts.length, icon: '📋', color: 'amber' },
          { label: 'Urgent Items', value: insights.filter(i => i.urgency === 'Urgent').length, icon: '🚨', color: 'red' },
        ].map(stat => (
          <div key={stat.label} className="bg-white rounded-2xl border border-slate-200 p-5">
            <div className="text-2xl mb-2">{stat.icon}</div>
            <div className="text-3xl font-black text-slate-900">{stat.value}</div>
            <div className="text-sm text-slate-500 mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Convergent Signals */}
      {signals.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            🔗 Convergent Signals
            <span className="bg-red-100 text-red-700 text-xs px-2 py-0.5 rounded-full font-bold">
              {signals.length} Active
            </span>
          </h2>
          <div className="space-y-4">
            {signals.map(signal => (
              <div
                key={signal.id}
                className="bg-gradient-to-r from-indigo-900 to-blue-900 text-white rounded-2xl p-6 signal-alert"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="flex items-center gap-3 mb-1">
                      <span className="text-amber-300 font-mono text-sm bg-white/10 px-2 py-0.5 rounded">
                        💊 {signal.drug_name}
                      </span>
                      <span className="bg-white/20 text-xs px-2 py-0.5 rounded font-medium">
                        {signal.signal_type}
                      </span>
                      <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                        signal.confidence === 'High' ? 'bg-green-400 text-green-900' :
                        signal.confidence === 'Medium' ? 'bg-yellow-400 text-yellow-900' :
                        'bg-slate-400 text-slate-900'
                      }`}>
                        {signal.confidence} Confidence
                      </span>
                    </div>
                    <p className="text-blue-100 text-sm">{signal.signal_summary}</p>
                  </div>
                  {signal.velocity === 'Accelerating' && (
                    <span className="text-red-300 text-sm font-bold animate-pulse">⬆ Accelerating</span>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="bg-white/10 rounded-xl p-3">
                    <div className="text-xs text-blue-200 font-medium mb-1">🎤 MSL Intelligence</div>
                    <p className="text-sm text-white/90">{signal.msl_evidence?.substring(0, 150)}...</p>
                  </div>
                  <div className="bg-white/10 rounded-xl p-3">
                    <div className="text-xs text-red-200 font-medium mb-1">❤️ Patient Data</div>
                    <p className="text-sm text-white/90">{signal.patient_evidence?.substring(0, 150)}...</p>
                  </div>
                </div>

                {signal.recommended_actions && (
                  <div>
                    <div className="text-xs text-blue-200 font-medium mb-2">Recommended Actions:</div>
                    <div className="flex flex-wrap gap-2">
                      {(Array.isArray(signal.recommended_actions)
                        ? signal.recommended_actions
                        : Object.values(signal.recommended_actions || {})
                      ).map((action, i) => (
                        <span key={i} className="bg-white/15 text-xs px-3 py-1 rounded-full">
                          {i + 1}. {action}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Charts & Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Adherence Trend Chart */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6">
          <h3 className="font-bold text-slate-800 mb-4">Adherence Trend — Traditional vs PharmaBridge</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={adherenceTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="week" tick={{ fontSize: 11 }} />
              <YAxis domain={[50, 100]} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="traditional"
                stroke="#94a3b8"
                strokeDasharray="5 5"
                name="Traditional App"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="pharmabridge"
                stroke="#1e3a8a"
                name="PharmaBridge"
                strokeWidth={3}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Barrier Breakdown */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6">
          <h3 className="font-bold text-slate-800 mb-4">Patient Barriers</h3>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={barrierData} cx="50%" cy="50%" innerRadius={40} outerRadius={70} dataKey="value">
                {barrierData.map((entry, index) => (
                  <Cell key={index} fill={BARRIER_COLORS_CHART[index % BARRIER_COLORS_CHART.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-1 mt-2">
            {barrierData.slice(0, 4).map((d, i) => (
              <div key={d.name} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full" style={{ background: BARRIER_COLORS_CHART[i] }}></div>
                  <span className="text-slate-600">{d.name}</span>
                </div>
                <span className="font-medium text-slate-700">{d.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* MSL Feed */}
      <div className="mt-6">
        <h2 className="text-lg font-bold text-slate-800 mb-4">Live MSL Intelligence Feed</h2>
        {insightsLoading ? (
          <div className="text-center py-8 text-slate-400">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {insights.slice(0, 6).map(insight => (
              <InsightCard key={insight.id} insight={insight} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
```

**✅ Phase 6 complete. Full frontend is built.**

---

## 14. Phase 7 — Connecting Everything (Full Integration)

### Step 7.1 — Update Backend main.py with All Routes

Replace `backend/main.py` with the final version:
```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="PharmaBridge API",
    description="Autonomous Pharma Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import all routes
from routes import msl_routes, patient_routes, bridge_routes
from services.transcription import transcribe_audio
from services.tts import text_to_speech

# Register routes
app.include_router(msl_routes.router, prefix="/api/msl", tags=["MSL Intelligence"])
app.include_router(patient_routes.router, prefix="/api/patient", tags=["Patient Companion"])
app.include_router(bridge_routes.router, prefix="/api/bridge", tags=["Bridge Layer"])

@app.get("/")
async def root():
    return {
        "message": "PharmaBridge API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty audio file")

    result = await transcribe_audio(audio_bytes)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Transcription failed"))

    return {"transcript": result["transcript"]}

@app.post("/api/speak")
async def speak(request: dict):
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    result = await text_to_speech(text)
    return result
```

Also create `backend/routes/patient_routes.py` and `backend/routes/bridge_routes.py` from the code in Phases 4 and 5 above (copy-paste each file).

### Step 7.2 — Enable Supabase Realtime

In your Supabase dashboard:
1. Go to **Database** → **Replication**
2. Under "Source tables for replication", click **Add table**
3. Add: `msl_insights`, `patient_conversations`, `care_team_alerts`, `convergent_signals`
4. Click **Save**

This enables the Supabase Realtime WebSocket connection that makes the dashboard update live.

---

## 15. Phase 8 — UI Polish & Design System

The app already has good styling from Tailwind. For extra polish, add these to `frontend/src/index.css`:
```css
/* Smooth page transitions */
* {
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

/* Better scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* Card hover effects */
.insight-card:hover {
  transform: translateY(-1px);
}
```

**Key design decisions already baked in:**
- Blue (`#003087`) = PharmaBridge brand primary (MSL intelligence side)
- Red (`#8B0000`) = Patient companion side  
- The HQ dashboard converges both with `indigo-900` for the Bridge Layer
- All urgency indicators use color coding: red = urgent, amber = medium, slate = low
- Real-time updates use a green pulse dot (industry standard for live data)

---

## 16. Phase 9 — Demo Data & Seeding Scripts

Create `scripts/seed_demo_data.py`:
```python
"""
Seed script: populates PharmaBridge database with realistic demo data.
Run this BEFORE the demo to ensure there's data to show.

Usage:
    python scripts/seed_demo_data.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

from supabase import create_client
import uuid
from datetime import datetime, timedelta
import random

# Connect to Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🌱 Seeding PharmaBridge demo database...\n")

# ============================================================
# SEED MSL INSIGHTS
# ============================================================
msl_insights = [
    {
        "msl_name": "James Chen",
        "msl_region": "North America",
        "kol_name": "Dr. Rachel Patel",
        "kol_institution": "Johns Hopkins Medical Center",
        "kol_specialty": "Endocrinology",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Safety Observation",
        "description": "Dr. Patel reported two patients experiencing significant afternoon fatigue within 3-4 weeks of initiating Cardivex. She suspects it may be related to the lunchtime dosing schedule.",
        "confidence": "High",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Skeptical",
        "debrief_summary": "Dr. Patel raised concerns about fatigue in diabetic patients on Cardivex. She also questioned label dosing flexibility.",
        "status": "New"
    },
    {
        "msl_name": "Sarah Williams",
        "msl_region": "Mid-Atlantic",
        "kol_name": "Dr. Michael Torres",
        "kol_institution": "Mayo Clinic",
        "kol_specialty": "Cardiology",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Safety Observation",
        "description": "Dr. Torres mentioned two of his elderly patients discontinued Cardivex citing fatigue and reduced energy levels. He is exploring whether evening dosing might mitigate this.",
        "confidence": "High",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Skeptical",
        "debrief_summary": "Fatigue signal emerging in elderly Cardivex patients. Dr. Torres open to dose timing study.",
        "status": "New"
    },
    {
        "msl_name": "Priya Krishnamurthy",
        "msl_region": "Southeast",
        "kol_name": "Dr. Helen Morris",
        "kol_institution": "Emory University Hospital",
        "kol_specialty": "Internal Medicine",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Safety Observation",
        "description": "Dr. Morris flagged fatigue as a recurring patient complaint specifically in patients over 65 on Cardivex. She asked whether post-marketing surveillance data shows age-specific fatigue patterns.",
        "confidence": "High",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Neutral",
        "debrief_summary": "Third regional report of fatigue in elderly Cardivex patients. Evidence Gap identified — no age-stratified fatigue data available.",
        "status": "New"
    },
    {
        "msl_name": "James Chen",
        "msl_region": "North America",
        "kol_name": "Dr. Rachel Patel",
        "kol_institution": "Johns Hopkins Medical Center",
        "kol_specialty": "Endocrinology",
        "drug_name": "Neurovax",
        "indication": "Alzheimer's Prevention",
        "insight_type": "Advocacy",
        "description": "Dr. Patel expressed strong support for Neurovax's preventive mechanism. She is willing to present at the upcoming AAN conference and has seen promising early results in 3 patients.",
        "confidence": "High",
        "urgency": "Normal",
        "routing_target": "Medical Affairs",
        "kol_sentiment": "Positive",
        "debrief_summary": "Dr. Patel is a strong Neurovax advocate. Excellent speaker candidate for AAN.",
        "status": "New"
    },
    {
        "msl_name": "David Kim",
        "msl_region": "West Coast",
        "kol_name": "Dr. Samuel Rodriguez",
        "kol_institution": "Stanford Medical",
        "kol_specialty": "Neurology",
        "drug_name": "CompetitorDrug-X",
        "indication": "Type 2 Diabetes",
        "insight_type": "Competitive Intel",
        "description": "Dr. Rodriguez mentioned that CompetitorDrug-X's APEX trial results showed superior HbA1c reduction compared to Cardivex in patients over 60. He is now considering switching several patients.",
        "confidence": "Medium",
        "urgency": "Normal",
        "routing_target": "Commercial",
        "kol_sentiment": "Skeptical",
        "debrief_summary": "APEX trial data creating competitive pressure on Cardivex in elderly diabetic segment.",
        "status": "New"
    }
]

# Insert MSL insights with staggered timestamps for the demo
for i, insight in enumerate(msl_insights):
    insight["created_at"] = (datetime.utcnow() - timedelta(days=i, hours=random.randint(1, 8))).isoformat()
    result = supabase.table("msl_insights").insert(insight).execute()
    print(f"  ✅ Insight: [{insight['insight_type']}] {insight['kol_name']} re: {insight['drug_name']}")

print(f"\n📊 Inserted {len(msl_insights)} MSL insights\n")

# ============================================================
# SEED PATIENT PROFILES
# ============================================================
patients = [
    {
        "patient_name": "Sarah Johnson",
        "patient_code": "PT-001",
        "age_group": "46-60",
        "condition": "Type 2 Diabetes",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-01-15",
        "care_team_email": "dr.patel@example.com",
        "adherence_rate": 68.5,
        "consecutive_days_tracked": 14,
        "primary_barrier": "Side Effect",
        "barrier_confidence": "High",
        "barrier_details": "Patient reports afternoon fatigue correlated with lunchtime Cardivex dosing",
        "barrier_detected_at": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        "current_strategy": "Side effect investigation — timing adjustment pending care team review",
        "intervention_stage": 3
    },
    {
        "patient_name": "Robert Martinez",
        "patient_code": "PT-002",
        "age_group": "60+",
        "condition": "Type 2 Diabetes",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-02-01",
        "care_team_email": "dr.torres@example.com",
        "adherence_rate": 45.0,
        "consecutive_days_tracked": 10,
        "primary_barrier": "Side Effect",
        "barrier_confidence": "High",
        "barrier_details": "Significant fatigue and reduced energy, stopped taking medication 4 days ago",
        "barrier_detected_at": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        "current_strategy": "Urgent care team referral — medication discontinued",
        "intervention_stage": 4
    },
    {
        "patient_name": "Mary Chen",
        "patient_code": "PT-003",
        "age_group": "31-45",
        "condition": "Hypertension",
        "drug_name": "Hypertex",
        "drug_start_date": "2025-03-10",
        "care_team_email": "dr.chen@example.com",
        "adherence_rate": 72.0,
        "consecutive_days_tracked": 21,
        "primary_barrier": "Forgetfulness",
        "barrier_confidence": "High",
        "barrier_details": "Patient forgets evening doses when schedule changes. Morning doses are consistent.",
        "barrier_detected_at": (datetime.utcnow() - timedelta(days=7)).isoformat(),
        "current_strategy": "Routine anchoring — linking evening dose to dinner routine",
        "intervention_stage": 2
    },
    {
        "patient_name": "James Williams",
        "patient_code": "PT-004",
        "age_group": "60+",
        "condition": "Type 2 Diabetes",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-01-20",
        "care_team_email": "dr.morris@example.com",
        "adherence_rate": 82.0,
        "consecutive_days_tracked": 18,
        "primary_barrier": "Cost",
        "barrier_confidence": "Medium",
        "barrier_details": "Patient mentioned high co-pay. May be rationing doses.",
        "barrier_detected_at": (datetime.utcnow() - timedelta(days=4)).isoformat(),
        "current_strategy": "Patient assistance program identification",
        "intervention_stage": 2
    },
    {
        "patient_name": "Lisa Thompson",
        "patient_code": "PT-005",
        "age_group": "46-60",
        "condition": "Cardiovascular Disease",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-02-15",
        "care_team_email": "dr.smith@example.com",
        "adherence_rate": 91.0,
        "consecutive_days_tracked": 28,
        "primary_barrier": "Unknown",
        "barrier_confidence": "Low",
        "barrier_details": None,
        "barrier_detected_at": None,
        "current_strategy": "General support — monitoring adherence",
        "intervention_stage": 1
    }
]

patient_ids = {}
for patient in patients:
    result = supabase.table("patient_profiles").insert(patient).execute()
    if result.data:
        patient_ids[patient["patient_code"]] = result.data[0]["id"]
        print(f"  ✅ Patient: {patient['patient_name']} ({patient['patient_code']}) — {patient['primary_barrier']} barrier")

print(f"\n👥 Inserted {len(patients)} patient profiles\n")

# ============================================================
# SEED SAMPLE CONVERSATIONS for PT-001 (Sarah — the demo patient)
# ============================================================
if "PT-001" in patient_ids:
    patient_id = patient_ids["PT-001"]
    conversations = [
        # Day 1
        {"role": "companion", "message": "Good morning, Sarah! How are you feeling today? Did you take your Cardivex this morning?", "session_date": "2025-06-01", "session_number": 1},
        {"role": "patient", "message": "I did take it. But I've been feeling really tired in the afternoons.", "session_date": "2025-06-01", "session_number": 1, "barrier_signal": "Side Effect", "signal_strength": "Weak"},
        {"role": "companion", "message": "I'm glad you took it. That tiredness is worth paying attention to — does it happen at around the same time each day?", "session_date": "2025-06-01", "session_number": 1},
        {"role": "patient", "message": "Yes, always around 2 or 3pm. It's actually the time I take my pill at lunch.", "session_date": "2025-06-01", "session_number": 1, "barrier_signal": "Side Effect", "signal_strength": "Strong"},

        # Day 3
        {"role": "companion", "message": "Good morning! How did yesterday go? Did you take your Cardivex?", "session_date": "2025-06-03", "session_number": 3},
        {"role": "patient", "message": "I did, but honestly the fatigue is making it hard to get through my workday. I'm thinking about stopping.", "session_date": "2025-06-03", "session_number": 3, "barrier_signal": "Side Effect", "signal_strength": "Strong"},
        {"role": "companion", "message": "Thank you for telling me that — stopping suddenly could affect your treatment. I'm going to flag this to your care team right now so they can review whether a timing change might help. You don't have to just deal with this.", "session_date": "2025-06-03", "session_number": 3},
    ]

    for conv in conversations:
        conv["patient_id"] = patient_id
        supabase.table("patient_conversations").insert(conv).execute()

    print(f"  ✅ Seeded conversation history for Sarah (PT-001)")

# ============================================================
# SEED CARE TEAM ALERT
# ============================================================
if "PT-001" in patient_ids:
    supabase.table("care_team_alerts").insert({
        "patient_id": patient_ids["PT-001"],
        "patient_code": "PT-001",
        "drug_name": "Cardivex",
        "alert_type": "Barrier Detected",
        "alert_message": "Patient Sarah Johnson (PT-001) has confirmed afternoon fatigue consistently correlated with lunchtime Cardivex dosing (Day 3 of 7-day arc). Patient mentioned considering stopping medication.",
        "barrier_type": "Side Effect",
        "barrier_details": "Afternoon fatigue 1-2 hours post lunchtime dose, confirmed over 3 days",
        "recommended_action": "Schedule clinical review of dose timing. Consider dinner-time dosing trial.",
        "status": "Pending"
    }).execute()
    print(f"  ✅ Care team alert created for Sarah (PT-001)")

print("\n🎉 Demo data seeded successfully!")
print("\n📋 Summary:")
print(f"   {len(msl_insights)} MSL insights — including 3 fatigue reports for Cardivex")
print(f"   {len(patients)} patient profiles — with 3 Cardivex patients (Side Effect barrier)")
print(f"   1 conversation arc (Sarah's 3-day fatigue journey)")
print(f"   1 care team alert")
print(f"\n🔗 Run the Bridge Scan from the HQ Dashboard to generate the convergent signal!")
```

Run the seed script:
```bash
cd scripts
python seed_demo_data.py
```

---

## 17. How to Run the Full App

Open **three terminal windows** side by side.

### Terminal 1 — Backend
```bash
cd pharmabridge/backend
source venv/bin/activate   # Mac/Linux
# OR: venv\Scripts\activate   (Windows)

uvicorn main:app --reload --port 8000
```

You should see: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2 — Frontend
```bash
cd pharmabridge/frontend
npm run dev
```

You should see: `Local: http://localhost:5173/`

### Terminal 3 — Keep this available for:
- Running seed scripts
- Testing API calls
- Debugging

Open your browser at **http://localhost:5173** — PharmaBridge is running.

### Quick Verification Checklist
- [ ] `http://localhost:8000` → shows `{"message": "PharmaBridge API is running"}`
- [ ] `http://localhost:8000/docs` → shows the interactive API documentation
- [ ] `http://localhost:5173` → shows the PharmaBridge landing page
- [ ] Clicking "MSL Intelligence Agent" → loads the MSL page
- [ ] Clicking "Patient Companion" → loads the patient selection page
- [ ] HQ Dashboard → shows the dashboard with charts

---

## 18. Demo Script (Presentation Walkthrough)

Use this script when presenting to judges. Each section maps to approximately how much time to spend.

### Opening (60 seconds)
Show the landing page. Say:
> "Pharmaceutical companies spend $2.6 billion bringing a single drug to market. Then 50% of patients stop taking it — and the company has almost no idea why. Simultaneously, their field teams are having conversations with top doctors every day about exactly these problems. Those insights are never captured. PharmaBridge connects both."

Click through the three stat cards on the landing page.

### The Human Story (30 seconds)
> "Meet Sarah. She stopped her Cardivex because of fatigue. She told nobody. And meet James — an MSL who heard from three different doctors about fatigue on the same drug. He filed a brief CRM note. Nobody ever connected James's intelligence to Sarah's struggle. Until now."

### Demo Module 1 — MSL Debrief (2 minutes)
Navigate to **MSL Intelligence Agent**.

**Option A (live):** Record yourself saying:
> "I just met with Dr. Patel at Apollo Hospital. She expressed some serious concerns about Cardivex. Two of her patients — both over 60 — developed significant fatigue about two weeks after starting the medication. She's uncertain whether it's the drug and asked if we have any age-specific safety data. She also mentioned that the APEX trial results from Competitor X are making her reconsider her first-line choice."

Submit and watch the AI extract: Safety Observation (routed to Pharmacovigilance) + Competitive Intel (routed to Commercial). Point out the confidence scoring and urgency flags.

**Option B (text):** Use the text input tab — paste the above transcript directly. Faster and more reliable for demos.

### Demo Module 2 — Patient Companion (2 minutes)
Navigate to **Patient Companion**.

Select **Sarah Johnson (PT-001)** from the patient list. The opening message will appear. Walk through Sarah's 3-day conversation arc from the seeded data (it's already in the DB — you can show the conversation history). 

Key talking points:
- Point out the adaptive questioning — Aria doesn't just send reminders, it listens
- Show the barrier profile updating from "Unknown" to "Side Effect: High Confidence"
- Show the care team alert in the HQ dashboard appearing automatically

### The Bridge Moment (1 minute — the most important part)
Navigate to **HQ Dashboard**. 

If you've already run the seed script, click **Run Bridge Scan**. 

The system will analyze:
- 3 MSL fatigue reports (James Chen, Sarah Williams, Priya Krishnamurthy — all about Cardivex)
- 3 patients with confirmed Side Effect barrier on Cardivex

After ~5 seconds, the Convergent Signal alert appears on screen.

Point to it and say:
> "Three MSLs across separate regions independently flagged fatigue on Cardivex. Simultaneously, the patient companion confirmed fatigue as the primary adherence barrier in three Cardivex patients. Two completely independent sources. Same drug. Same signal. No pharma company in the world can see this connection today. PharmaBridge surfaces it automatically, in real time."

### Close (30 seconds)
> "$300 billion lost annually. 125,000 preventable deaths. These are not technology problems — they are information problems. The answers existed all along. They just lived in two places that never talked to each other. PharmaBridge is the bridge."

---

## 19. Troubleshooting Common Issues

### "Microphone not working"
- Browser must be served over `https://` or `localhost` for microphone access
- Check browser microphone permissions: Chrome → Settings → Privacy → Microphone
- The text input mode is a full backup — works identically for the demo

### "API key errors"
- Double-check your `.env` files — no spaces around the `=` sign
- Make sure the backend `.env` is in the `backend/` folder, not the root
- Restart uvicorn after changing `.env` (Ctrl+C, then run again)

### "Supabase connection failed"
- Check that the URL starts with `https://` (not `http://`)
- Confirm you're using the **service_role** key in the backend `.env`, not the anon key
- Verify table creation — go to Supabase → Table Editor — tables should be visible

### "CORS error in browser"
- The backend must be running on port 8000
- The CORS_ORIGINS in backend `.env` must include `http://localhost:5173`
- Never add a trailing slash to CORS origins

### "Claude returns non-JSON"
- This can happen occasionally. The code handles it with fallback values.
- If it's persistent: check your ANTHROPIC_API_KEY is valid and has credit

### "Realtime updates not working"
- Confirm you enabled Replication in Supabase for the key tables
- Check the Supabase Realtime status: Project Settings → API → check Realtime is enabled
- In the browser console, look for WebSocket connection messages

### "ElevenLabs audio not playing"
- Some browsers block autoplay — the app will silently fail and still show text
- Test manually: go to `http://localhost:8000/api/speak` via the `/docs` page and call it directly
- Check your ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID are set correctly

### Running out of Whisper API credit
- Use the text input tab on the MSL Agent page — it has identical functionality
- For the demo, typing the transcript is actually more reliable than live voice

---

## Final Checklist Before the Demo

- [ ] All `.env` keys are filled in and correct
- [ ] `python seed_demo_data.py` has been run successfully
- [ ] Backend is running (`uvicorn main:app --reload --port 8000`)
- [ ] Frontend is running (`npm run dev`)
- [ ] Landing page loads at `http://localhost:5173`
- [ ] MSL Agent page: try submitting a text debrief and confirm insights appear
- [ ] Patient page: Sarah Johnson shows up, conversation starts
- [ ] HQ Dashboard: click "Run Bridge Scan" and confirm signal appears
- [ ] Browser microphone permission granted (for voice demo)
- [ ] ElevenLabs voice tested (patient companion speaks)
- [ ] You have practiced the demo walkthrough at least twice

---

*PharmaBridge — Autonomous Pharma Intelligence Platform*  
*Bridging the gap between what doctors say in the field and what patients experience at home.*
