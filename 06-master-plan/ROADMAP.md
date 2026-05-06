# ROADMAP
## The Den — Build Plan

**Principle throughout: Boring infrastructure beats exciting complexity. Ship working pieces.**

---

## Phase 1 — Foundation
**Target: Stable daily use within one week**

### Objectives
- One governing prompt layer that does not need to be rebuilt
- One RTDL in one place
- One context file (Stu.md) that eliminates re-introduction
- The Den cockpit opens without error

### Deliverables

**1. Core Framework (done)**
The May 2026 version is the definitive document. Store at `05-prompts-and-notes/Master_Prompt_Core_Framework_0526.md`. Update in place when priorities shift. Do not create new versions — edit the file directly.

**2. Stu.md**
Create a single persistent context file. Contents: identity, current projects (ranked), financial reality snapshot, active real estate files, key contacts, decisions made and when. Paste this at the start of any new AI session. Update monthly or when something material changes.

**3. RTDL — Single Authoritative File**
Pick one format (Excel or Markdown). Archive all prior versions to `01-chatgpt-versions/rtdl-archive/`. The live RTDL lives at one path. Only one file. Updated after each session where tasks change.

**4. The Den V6 — Stabilized**
Audit The Den V6 HTML for any features requiring a running server or live API call. Comment those out or remove them. The base cockpit (daily view, RTDL display, morning ritual) should work offline. Test: open the file in a browser with no internet. It should load.

**5. Session Start Ritual**
Document a three-step session start:
1. Open The Den
2. Paste Stu.md into the AI
3. Paste or attach current RTDL

This replaces every version of "let me explain who I am again."

### Dependencies
- Core Framework: exists
- Stu.md: needs to be written (30 minutes of work)
- RTDL consolidation: pick the Feb 16 version as the base, update it
- The Den V6 audit: 1-2 hours

### Risks
- RTDL version proliferation will resume unless there is a clear rule: one file, one location, no copies
- Stu.md will go stale if not updated regularly — schedule a monthly 10-minute update

### Recommended Tools
- Markdown for Stu.md and RTDL (plain text, no app dependency)
- Chrome for The Den HTML cockpit
- Claude (Cowork) as the primary AI layer

---

## Phase 2 — Retrieval and Search
**Target: 4-6 weeks after Phase 1 is stable**

### Objectives
- Past decisions and promises are findable without manual searching
- Waiting On items surface automatically before they go stale
- Weekly review is a formal ritual with consistent output

### Deliverables

**1. Waiting On Log**
A simple text file or RTDL section where every "I will follow up on X" gets logged with a date. Reviewed at every session start. Stale items (older than 7 days with no update) flagged automatically by the AI when Stu.md is pasted.

**2. Weekly Review Prompt**
A single prompt that produces a weekly review in 15 minutes. Inputs: current RTDL, prior week's log. Outputs: what moved, what is stale, what is the one thing for next week, any promises that need action. Output appended to a running `weekly-log.md` file.

**3. Decision Log**
A simple append-only file. Every significant decision logged: what was decided, why, when. Not a journal. Just the decisions. Referenced when context is needed for a follow-up.

**4. Fieldy — Simplified**
Replace the local Python webhook with a simpler capture method. Options: voice memo app to text file via iOS Shortcuts, or direct paste of a transcript into Claude with a standard intake prompt. No local server required.

### Dependencies
- Phase 1 must be stable before Phase 2 begins
- Waiting On Log requires Phase 1 RTDL to be consolidated first

### Risks
- Weekly review will be skipped unless it is in the calendar as a non-negotiable
- Decision log only works if the habit forms — start with one entry per week minimum

---

## Phase 3 — Integrations and Connectors
**Target: 2-3 months after Phase 2 is stable**

### Objectives
- Google Calendar is the single source of truth and the AI can read it
- Real estate files (Skyslope, Lofty CRM) have a structured summary format that feeds the RTDL
- Burn The Sky and Pumpkin Patch have their own project sub-prompts under the Core Framework

### Deliverables

**1. Calendar Integration**
Connect Google Calendar to the AI layer. Morning session automatically surfaces the day's appointments without manual paste. Start with the Cowork calendar MCP if available.

**2. CRM Summary Format**
A standard weekly pull from Lofty: active buyer files, listing activity, pending follow-ups. Formatted as a paste-in block for the RTDL update. Manual at first, automated in Phase 4.

**3. Project Sub-Prompts**
Following the Core Framework model, create sub-prompts for:
- Burn The Sky (opens May 2026, inventory tracking, staffing, permits)
- Pumpkin Patch (planting June 2026, seed/supplier, ground prep, labour)
- LPT Recruiting / The Foundation (6-12 month build, theFoundation.ca)

Each sub-prompt defers to the Core Framework for identity and tone. It adds project-specific facts the AI should know without being re-told.

**4. S2 / The Foundation**
S2 (real estate AI assistant on theFoundation.ca) is a separate Lovable project with its own Supabase backend. Keep it separate. The integration point in Phase 3 is a summary: what S2 conversations happened this week, what follow-ups were generated.

### Dependencies
- Stable Phase 2 system
- Google Calendar access via Cowork
- Lofty CRM access or manual export

### Risks
- Calendar integration only valuable if the calendar is actually maintained as a single source of truth
- Project sub-prompts will go stale — review monthly alongside Core Framework update

---

## Phase 4 — Automation and AI Assistance
**Target: 4-6 months out**

### Objectives
- Voice capture is fully automated (speak, it lands in the system, no manual steps)
- RTDL updates from completed tasks without manual editing
- Morning briefing is generated automatically before Stu opens his laptop

### Deliverables

**1. Automated Voice Capture**
Fieldy rebuilt properly. Voice memo triggers a transcription pipeline. Output lands in a designated inbox file. AI processes the inbox at session start and surfaces tasks, promises, and decisions.

**2. RTDL Auto-Update**
When tasks are marked done in a session, the RTDL file is updated automatically. No manual copy-paste between the AI conversation and the file.

**3. Morning Briefing Email or Notification**
5am trigger. Single summary: today's calendar, top 3 tasks from RTDL, any stale Waiting On items, one question to answer before anything else. Plain text. No dashboard required to read it.

### Dependencies
- Phase 3 integrations in place
- Stable RTDL format (changing the format in Phase 4 breaks automation)

### Risks
- Automation creates maintenance overhead. Only automate what has been done manually and reliably for at least 4 weeks
- Morning briefing is only useful if it is acted on. Do not build it until the daily ritual is established

---

## Phase 5 — Advanced Agent Systems
**Target: 6-12 months out, only if Phase 4 is stable**

### Objectives
- Multi-context memory without manual paste-in
- AI agents that take actions (draft emails, update CRM, flag stale files) without being asked
- The Foundation / S2 integrated into the broader OS

### Deliverables

**1. Persistent Memory Layer**
True memory across sessions without manual Stu.md paste. Options depend on tool availability at that time: Claude memory features, local vector store, or structured database.

**2. Proactive Agents**
Agents that run on a schedule and surface findings: listing activity digest, recruiting pipeline update, Waiting On items overdue by more than 7 days.

**3. Full Foundation Integration**
S2 conversation insights feed the RTDL automatically. Agent interactions on theFoundation.ca create follow-up tasks in Stu's system.

### Dependencies
- All prior phases stable and in daily use
- Tool ecosystem mature enough to support reliable agents

### Risks
- Phase 5 is the most likely place to over-engineer. The test: does each agent make Stu more effective today, or does it feel impressive but create overhead?
- Do not begin Phase 5 until Phase 4 has been running for at least 60 days without requiring a rebuild

---

## What to Build First

If you do nothing else this week:

1. Write Stu.md (30 minutes)
2. Consolidate the RTDL to one file (15 minutes)
3. Confirm The Den V6 opens without error (10 minutes)

That is Phase 1. Everything else follows from there.
