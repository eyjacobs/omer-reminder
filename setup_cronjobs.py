"""
setup_cronjobs.py — Creates all Omer Reminder cron jobs on cron-job.org

Usage:
    python3 setup_cronjobs.py

You will be prompted for your cron-job.org API key and GitHub PAT.
Both are kept in memory only — never written to disk or committed.

Requirements:
    - Free account at https://cron-job.org
    - API key from https://cron-job.org/dashboard (Settings → API)
    - GitHub Personal Access Token with 'workflow' scope
      Generate at: https://github.com/settings/tokens
"""

import json
import urllib.request
import urllib.error
import getpass

GITHUB_REPO   = "eyjacobs/omer-reminder"
WORKFLOW_FILE = "omer.yml"
CRONJOB_API   = "https://api.cron-job.org"

# All send times in UTC.
# Regular nights = nightfall EDT + 10 min (EDT = UTC-4, so +10 min crosses midnight into next UTC day)
# Fridays = 90 min before Shabbat (these fire earlier, same UTC calendar day)
JOBS = [
    # (label,              month, mday, hour, minute)
    # ── Regular nights ───────────────────────────────────────────────────────
    ("Day 11 — Apr 12",    4,  13,  0, 22),
    ("Day 12 — Apr 13",    4,  14,  0, 23),
    ("Day 13 — Apr 14",    4,  15,  0, 24),
    ("Day 14 — Apr 15",    4,  16,  0, 25),
    ("Day 15 — Apr 16",    4,  17,  0, 26),
    ("Day 17 — Apr 18",    4,  19,  0, 28),
    ("Day 18 — Apr 19",    4,  20,  0, 29),
    ("Day 19 — Apr 20",    4,  21,  0, 30),
    ("Day 20 — Apr 21",    4,  22,  0, 31),
    ("Day 21 — Apr 22",    4,  23,  0, 32),
    ("Day 22 — Apr 23",    4,  24,  0, 33),
    ("Day 24 — Apr 25",    4,  26,  0, 35),
    ("Day 25 — Apr 26",    4,  27,  0, 36),
    ("Day 26 — Apr 27",    4,  28,  0, 37),
    ("Day 27 — Apr 28",    4,  29,  0, 38),
    ("Day 28 — Apr 29",    4,  30,  0, 39),
    ("Day 29 — Apr 30",    5,   1,  0, 40),
    ("Day 31 — May 2",     5,   3,  0, 42),
    ("Day 32 — May 3",     5,   4,  0, 43),
    ("Day 33 — May 4",     5,   5,  0, 44),
    ("Day 34 — May 5",     5,   6,  0, 45),
    ("Day 35 — May 6",     5,   7,  0, 46),
    ("Day 36 — May 7",     5,   8,  0, 47),
    ("Day 38 — May 9",     5,  10,  0, 49),
    ("Day 39 — May 10",    5,  11,  0, 50),
    ("Day 40 — May 11",    5,  12,  0, 51),
    ("Day 41 — May 12",    5,  13,  0, 52),
    ("Day 42 — May 13",    5,  14,  0, 53),
    ("Day 43 — May 14",    5,  15,  0, 54),
    ("Day 45 — May 16",    5,  17,  0, 56),
    ("Day 46 — May 17",    5,  18,  0, 57),
    ("Day 47 — May 18",    5,  19,  0, 58),
    ("Day 48 — May 19",    5,  20,  0, 59),
    ("Day 49 — May 20",    5,  21,  1,  0),
    # ── Fridays (pre-Shabbat) ────────────────────────────────────────────────
    ("Day 16 — Apr 17 (Fri)", 4, 17, 21, 48),
    ("Day 23 — Apr 24 (Fri)", 4, 24, 21, 56),
    ("Day 30 — May 1  (Fri)", 5,  1, 22,  3),
    ("Day 37 — May 8  (Fri)", 5,  8, 22, 10),
    ("Day 44 — May 15 (Fri)", 5, 15, 22, 17),
]

def create_job(cronjob_api_key, github_pat, label, month, mday, hour, minute):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    payload = {
        "job": {
            "url": url,
            "enabled": True,
            "saveResponses": True,
            "requestMethod": 1,  # POST
            "extendedData": {
                "headers": {
                    "Authorization": f"token {github_pat}",
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json",
                },
                "body": json.dumps({"ref": "main"}),
            },
            "schedule": {
                "timezone": "UTC",
                "minutes":  [minute],
                "hours":    [hour],
                "mdays":    [mday],
                "months":   [month],
                "wdays":    [-1],
            },
        }
    }
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        f"{CRONJOB_API}/jobs",
        data=data,
        headers={
            "Authorization": f"Bearer {cronjob_api_key}",
            "Content-Type":  "application/json",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            job_id = result.get("jobId", "?")
            print(f"  ✓ {label:30s}  UTC {month:02d}/{mday:02d} {hour:02d}:{minute:02d}  (id={job_id})")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ✗ {label:30s}  ERROR {e.code}: {body}")

def main():
    print("Omer Reminder — cron-job.org setup")
    print("=" * 50)
    print("Get your cron-job.org API key from: https://cron-job.org/dashboard (Settings → API)")
    cronjob_api_key = getpass.getpass("cron-job.org API key: ")
    print("Get your GitHub PAT from: https://github.com/settings/tokens (needs 'workflow' scope)")
    github_pat      = getpass.getpass("GitHub Personal Access Token: ")
    print()
    print(f"Creating {len(JOBS)} cron jobs...")
    print()
    for label, month, mday, hour, minute in JOBS:
        create_job(cronjob_api_key, github_pat, label, month, mday, hour, minute)
    print()
    print("Done! View your jobs at https://cron-job.org/dashboard")

if __name__ == "__main__":
    main()
