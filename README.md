# 🕯️ Omer Reminder — Nightly SMS Counter

A lightweight macOS cron system that sends you a nightly text message reminding you which day of the Omer it is.

## What It Does

Each evening, your Mac automatically texts you a reminder like:

> "Don't forget to count! Day 14"

Send times increment by 1 minute each night (starting at 8:12 PM) to roughly track later nightfall times as spring progresses.

## How It Works

- `omer_send.sh` — sends a single SMS via [TextBelt](https://textbelt.com) for a given day number
- `setup_omer_cron.sh` — installs 39 cron jobs (Days 11–49) into your crontab

## Setup

### 1. Configure your phone number

Open `omer_send.sh` and replace the phone number with your own:

```bash
PHONE="+1XXXXXXXXXX"
```

### 2. Make the scripts executable

```bash
chmod +x ~/omer_send.sh ~/setup_omer_cron.sh
```

### 3. Install the cron jobs

```bash
~/setup_omer_cron.sh
```

### 4. Grant cron Full Disk Access (macOS Catalina+)

Without this, cron jobs run silently and fail.

1. Open **System Settings → Privacy & Security → Full Disk Access**
2. Click **+**, press **Cmd+Shift+G**, type `/usr/sbin/cron`, and add it

### 5. Test it

Send yourself a text right now to confirm it's working:

```bash
~/omer_send.sh 11
```

Then check the log:

```bash
cat ~/omer_log.txt
```

## SMS via TextBelt

This project uses [TextBelt](https://textbelt.com)'s free tier, which allows **1 free text per day**. The free API key is `textbelt`.

For reliable daily delivery, consider purchasing a TextBelt API key and updating `omer_send.sh`:

```bash
--data-urlencode "key=YOUR_API_KEY"
```

## ⚠️ Important: Mac Must Be Awake

Cron only runs when your Mac is awake. If it's asleep at send time, the text won't go out.

**Fix:** Go to **System Settings → Battery → Schedule** and set your Mac to wake a few minutes before 8:12 PM — or simply keep it plugged in and awake in the evenings.

## Coverage

| Days | Dates (2026) | Send Time |
|------|-------------|-----------|
| Day 11 | April 12 | 8:12 PM |
| Day 29 | April 30 | 8:30 PM |
| Day 49 | May 20 | 8:50 PM |

Days 1–10 are not included (assumed to have already passed or set up separately).

## Log

Every send attempt (success or failure) is logged to `~/omer_log.txt`.
