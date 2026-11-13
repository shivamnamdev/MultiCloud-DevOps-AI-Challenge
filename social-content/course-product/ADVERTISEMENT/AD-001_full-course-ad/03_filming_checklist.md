# 🎥 03: FILMING CHECKLIST + SHOT LIST: AD-001 (Face Video)
Gate: `Content-Creation/checklists/04_FILMING_CHEATSHEET_PRINTABLE_CHECKLIST.md` · Read from `02a_teleprompter.md` · **16:9, 1080p @ 30 fps**.
Rule: shoot the approved script as written. No new claims, numbers or offers on camera. **Do not record until every `{{...}}` in `02_script.md` is filled.**

## A. Pre-flight
- [ ] Lens wiped · Airplane mode ON · 20 GB free · phone on tripod, lens at eye level, eyes on top third
- [ ] AE/AF lock on face · fans/AC off · clap test · 15 s room tone → `assets_raw/audio/`
- [ ] Lav mic 6" below mouth, peaks -12 to -6 dB · key light 45°, fill 3:1, rim, 4500-5000K
- [ ] Props in frame: laptop with a terminal, one sticky note "BUILD · SHIP · FIX"; no clutter · plain solid-colour top
- [ ] Teleprompter under/over lens (use `teleprompter/` video for pace) · water, 30 s vocal warm-up

## B. Performance rules
- 130% energy. High/inquisitive on Beat 1 questions; **low chest voice** on `[LOW, CHEST VOICE]` lines (Beat 2 "ये DevOps सीखना नहीं है…", Beat 6 thesis, Beat 12 "दो रास्ते हैं").
- **Beat 1 off-book**, straight into the lens, say it to ONE person (a fresher stuck in tool-collector mode), never "guys".
- Real 1-2 s pauses at `[PAUSE]`; desk tap or palm slam at `[SLAM]` (Beat 3).
- Smile only on Beat 8 reframe and the Beat 12 sign-off. Beat 11 refund line: slow, flat, clear.
- Record each beat as its own block, 2-3 takes. Clap at the start of every take.

## C. Screen-capture shot list (record separately, 1920x1080)
| ID | Beat | Capture |
|---|---|---|
| S1 | 1 | **Real demo with a visible timer:** one prompt → Dockerfile + K8s YAML + Jenkins pipeline; stop timer (must be < 10 s) |
| S2 | 1/12 | Full-screen red alert `PRODUCTION DOWN · 02:00 AM` (graphic) |
| S3 | 2 | 30 browser tabs with the tool logos; YAML with red error; paste into chatbot ×2 |
| S4 | 4 | Hand-on-wall B-roll or graphic; path diagram Code→Build→Image→Registry→Cluster→Traffic→Monitoring |
| S5 | 5 | Split: failed build vs clean green pipeline |
| S6 | 9 | One 3-5 s clip per block: terminal; EC2/IAM/VPC; Jenkins stages; Dockerfile layers; K8s pods scaling; Grafana; Terraform plan; capstone pipeline; AI-served API |
| S7 | 11 | Price card + inclusions (graphic) |
## D. Hand-off
Footage → `assets_raw/a_roll/`, screens → `assets_raw/screen_recordings/`, audio → `assets_raw/audio/` (naming per `NAMING_CONVENTIONS.md` if present).
