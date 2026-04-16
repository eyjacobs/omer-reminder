"""
update_cronjobs.py — Updates the GitHub PAT on all existing Omer Reminder cron-job.org jobs

Usage:
    python3 update_cronjobs.py

You will be prompted for your cron-job.org API key and new GitHub PAT.
"""

import json
import time
import urllib.request
import urllib.error
import getpass

GITHUB_REPO   = "eyjacobs/omer-reminder"
CRONJOB_API   = "https://api.cron-job.org"

def get_jobs(api_key):
    req = urllib.request.Request(
        f"{CRONJOB_API}/jobs",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read()).get("jobs", [])

def update_job(api_key, github_pat, job):
    job_id = job["jobId"]
    # Patch just the Authorization header, preserving everything else
    payload = {
        "job": {
            "extendedData": {
                "headers": {
                    "Authorization": f"token {github_pat}",
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json",
                },
                "body": json.dumps({"ref": "main"}),
            }
        }
    }
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        f"{CRONJOB_API}/jobs/{job_id}",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type":  "application/json",
        },
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            resp.read()
            print(f"  ✓ Updated job {job_id}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ✗ Error updating job {job_id}: {e.code}: {body}")

def main():
    print("Omer Reminder — update GitHub PAT on cron-job.org jobs")
    print("=" * 55)
    cronjob_api_key = getpass.getpass("cron-job.org API key: ")
    github_pat      = getpass.getpass("New GitHub Personal Access Token: ")
    print()

    print("Fetching existing jobs...")
    jobs = get_jobs(cronjob_api_key)
    omer_jobs = [j for j in jobs if GITHUB_REPO in j.get("url", "")]
    print(f"Found {len(omer_jobs)} Omer Reminder jobs to update.")
    print()

    for job in omer_jobs:
        update_job(cronjob_api_key, github_pat, job)
        time.sleep(2)

    print()
    print("Done! Verify at https://cron-job.org/dashboard")

if __name__ == "__main__":
    main()
