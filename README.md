# Omer Reminder

A lightweight SMS reminder system for counting the Omer — the 49-day period between Passover and Shavuot. Each evening it sends a text message reminding you which day to count.

Reminders run entirely in the cloud via GitHub Actions — **no computer needs to be on or awake.** All you need is a GitHub account and a Gmail address.

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

### Adjusting for your timezone

The schedule is currently set for **Eastern time (EDT, UTC-4)**. If you're in a different timezone, adjust the cron times in `omer.yml` accordingly. GitHub Actions cron always uses UTC, so add or subtract the offset for your timezone to keep reminders arriving around 8 PM local time:

| Timezone | UTC offset | Adjustment |
|---|---|---|
| Eastern (EDT) | UTC-4 | no change needed |
| Central (CDT) | UTC-5 | add 1 hour to each cron time |
| Mountain (MDT) | UTC-6 | add 2 hours to each cron time |
| Pacific (PDT) | UTC-7 | add 3 hours to each cron time |

For example, if the cron entry is `12 0 13 4 *` (12:12 AM UTC = 8:12 PM EDT), a Pacific time user would change it to `12 3 13 4 *` (3:12 AM UTC = 8:12 PM PDT).

### 6. Enable GitHub Actions

If Actions are disabled on your fork, go to the **Actions** tab and enable them. The workflow will trigger automatically on the scheduled dates — no server or local machine required.

## Files

| File | Description |
|---|---|
| `.github/workflows/omer.yml` | GitHub Actions workflow — sends nightly reminders |
| `config.sh.example` | Template showing the config variables used locally |
