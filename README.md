# Omer Reminder

A free SMS reminder system for counting the Omer — the 49-day period between Passover and Shavuot. Sign up on the web, receive a nightly text.

Reminders run entirely in the cloud via GitHub Actions — **no computer needs to be on or awake.**

**Live signup form:** [eyjacobs.github.io/omer-reminder](https://eyjacobs.github.io/omer-reminder)

---

## How it works

1. People sign up at the form with their phone number, carrier, and timezone.
2. Signups are stored in a Google Sheet.
3. GitHub Actions runs each night, reads the sheet, and texts everyone at ~8 PM their local time.
4. Subscribers receive: `Don't forget to count! Day N`

---

## Setup (for your own fork)

### 1. Fork this repository

Fork [eyjacobs/omer-reminder](https://github.com/eyjacobs/omer-reminder) to your own GitHub account.

---

### 2. Create the Google Sheet

1. Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet.
2. In the first row, add these exact column headers:

   | A | B | C | D |
   |---|---|---|---|
   | Timestamp | Phone | Carrier | Timezone |

3. Note the spreadsheet ID from the URL — you'll need it in the next step. It's the long string between `/d/` and `/edit` in the URL.

---

### 3. Set up the Google Apps Script

This script receives signups from the form and writes them to your sheet.

1. In your Google Sheet, go to **Extensions → Apps Script**
2. Delete any existing code and paste the following:

```javascript
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.appendRow([
    new Date(),
    e.parameter.phone,
    e.parameter.carrier,
    e.parameter.timezone
  ]);
  return ContentService.createTextOutput('OK');
}
```

3. Click **Deploy → New deployment**
4. Set type to **Web app**
5. Set "Execute as" to **Me**
6. Set "Who has access" to **Anyone**
7. Click **Deploy** and copy the web app URL — you'll need it in step 5

---

### 4. Publish the sheet as a public CSV

This lets GitHub Actions read your subscriber list without needing API credentials.

1. In your Google Sheet, go to **File → Share → Publish to web**
2. Set the first dropdown to **Sheet1** and the second to **Comma-separated values (.csv)**
3. Click **Publish** and copy the URL
4. Add this URL as a GitHub secret named `SHEET_CSV_URL` (see step 6)

---

### 5. Add your Apps Script URL to the form

In your forked repo, open `index.html` and replace `YOUR_APPS_SCRIPT_URL_HERE` with the URL from step 3:

```js
const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_ID/exec';
```

Commit and push the change.

---

### 6. Add GitHub Secrets

In your forked repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret name | Value |
|---|---|
| `GMAIL_USER` | Your Gmail address |
| `GMAIL_PASSWORD` | A [Gmail App Password](https://support.google.com/accounts/answer/185833) |
| `SHEET_CSV_URL` | The CSV publish URL from step 4 |

---

### 7. Enable GitHub Pages

Go to **Settings → Pages**, set the source to **Deploy from a branch**, and select **main** / **root**. Your signup form will be live at `https://YOUR_USERNAME.github.io/omer-reminder`.

---

### 8. Enable GitHub Actions

If Actions are disabled on your fork, go to the **Actions** tab and enable them. The workflow will trigger automatically each night — no server or local machine required.

---

## Carrier gateway reference

| Carrier | Gateway |
|---|---|
| T-Mobile | `tmomail.net` |
| AT&T | `txt.att.net` |
| Verizon | `vtext.com` |
| Sprint | `messaging.sprintpcs.com` |

---

## Timezone reference

Reminders are sent at ~8 PM local time. The workflow runs at UTC 00:00, 01:00, 02:00, and 03:00 — one for each US timezone:

| Timezone | UTC offset | Send time |
|---|---|---|
| Eastern | UTC-4 | 8:00 PM EDT |
| Central | UTC-5 | 8:00 PM CDT |
| Mountain | UTC-6 | 8:00 PM MDT |
| Pacific | UTC-7 | 8:00 PM PDT |

---

## Updating the schedule for future years

The workflow is pre-configured for **2026** (days 11–49). For a future year, update the `SCHEDULE` dict in `.github/workflows/omer.yml` with the new UTC dates. The first night of Passover can be found at [hebcal.com](https://www.hebcal.com/holidays/). Counting begins the second night of Passover.

---

## Monitoring

View run history, logs, and any errors at: `https://github.com/YOUR_USERNAME/omer-reminder/actions`
