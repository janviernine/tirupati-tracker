Tirupati Tracker - replicate setup
==============================

Files in this folder:
1. tirupati_track.py  - monitor script (fetches tracking page, prints deterministic status)
2. cron-prompt.txt    - cron job prompt (formatting + change-gating rules)
3. cron-settings.txt  - cron job settings (name, schedule, monitor, flags)

Setup steps:
1. Copy tirupati_track.py to your Hermes scripts folder:
   C:/Users/<you>/AppData/Local/hermes/scripts/tirupati_track.py
   (Or keep it here and point the cron monitor at the full path.)

   To track a different parcel, edit URL = ... inside tirupati_track.py
   with that parcel's Frm_DocTrackWeb.aspx?docno=... link.
   Requires: python + requests (pip install requests).

2. Create the cron job (via cronjob_manage action=create):
   - name: tirupati-<YOUR_AWB>
   - schedule: */10 * * * *   (started as 30m, tightened to 10m)
   - monitor: tirupati_track.py  (or full path if not in scripts folder)
   - continuity: true
   - deliver: your DM or channel ID
   - prompt: contents of cron-prompt.txt

3. How it works:
   - Every tick the monitor script runs. Its stdout is diffed vs last tick.
   - First tick = baseline (sends current status).
   - Later ticks: agent runs only when output changed; prompt rules
     make it send a 📦 update only on STATUS / route change, else silent.

Original parcel details removed for sharing - paste your own AWB / route when you set it up.
