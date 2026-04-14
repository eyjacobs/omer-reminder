# Omer Reminder

A lightweight SMS reminder system for counting the Omer — the 49-day period between Passover and Shavuot. Each evening it sends a text message reminding you which day to count.

Reminders are sent via Gmail's SMTP to your carrier's email-to-SMS gateway, triggered by a GitHub Actions workflow on a nightly schedule. No third-party SMS services or paid APIs required.

## How it works

1. A GitHub Actions cron job fires each evening at the correct time (8:12–8:50 PM EDT, depending on the day).
2. The workflow runs a Python script that looks up the current Omer day and sends an SMS via Gmail SMTP → T-Mobile email-to-SMS gateway.
3. You receive a text that says: `Don't forget to count! Day N`

## Setup

### 1. Fork this repository

Fork [eyjacobs/omer-reminder](https://github.com/eyjacobs/omer-reminder) to your own GitHub account.

### 2. Create a Gmail App Password

The workflow authenticates with Gmail using an [App Password](https://support.google.com/accounts/answer/185833) (not your regular Gmail password). To generate one:

1. Go to your Google Account → Security → 2-Step Verification (must be enabled)
2. At the bottom of that page, click **App passwords**
3. Create a new app password (name it anything, e.g. "Omer Reminder")
4. Copy the 16-character password — you'll need it in the next step

### 3. Add GitHub Secrets

In your forked repo, go to **Settings → Secrets and variables → Actions** and add three secrets:

| Secret name | Value |
|---|---|
| `GMAIL_USER` | Your Gmail address (e.g. `you@gmail.com`) |
| `GMAIL_PASSWORD` | The App Password from step 2 |
| `PHONE` | Your phone number (e.g. `+15551234567`) |

### 4. Update the carrier gateway (if not on T-Mobile)

The workflow sends SMS by emailing `<your-number>@tmomail.net`. If you're on a different carrier, update the `to_sms` line in `.github/workflows/omer.yml`:

| Carrier | Gateway |
|---|---|
| T-Mobile | `@tmomail.net` |
| AT&T | `@txt.att.net` |
| Verizon | `@vtext.com` |
| Sprint | `@messaging.sprintpcs.com` |

### 5. Update the schedule for your year (if needed)

The workflow in `.github/workflows/omer.yml` is pre-configured for **2026** (days 11–49, starting April 12). If you're setting this up for a different year, you'll need to update:

- The cron schedule entries (UTC times corresponding to ~8 PM local time on each evening)
- The `schedule` dict in the Python script mapping UTC dates to Omer day numbers

The first night of Passover (day 1) can be found at [hebcal.com](https://www.hebcal.com/holidays/). Count begins the second night of Passover.

### 6. Enable GitHub Actions

If Actions are disabled on your fork, go to the **Actions** tab and enable them. The workflow will trigger automatically on the scheduled dates — no server or local machine required.

## Local alternative

If you prefer to run reminders from your own machine instead of GitHub Actions:

1. Copy `config.sh.example` to `config.sh` and fill in your values:
   ```bash
   cp config.sh.example config.sh
   ```
2. Save your Gmail App Password to `~/.omer_app_password`:
   ```bash
   echo "your-app-password" > ~/.omer_app_password
   chmod 600 ~/.omer_app_password
   ```
3. Run the cron setup script to install all reminders:
   ```bash
   bash setup_omer_cron.sh
   ```

This installs cron jobs that call `omer_send.sh` each evening with the correct day number.

## Files

| File | Description |
|---|---|
| `.github/workflows/omer.yml` | GitHub Actions workflow — main way to run reminders |
| `omer_send.sh` | Shell script for local cron-based sending |
| `setup_omer_cron.sh` | Installs local cron jobs for the full Omer period |
| `config.sh.example` | Template for local config (copy to `config.sh`) |
