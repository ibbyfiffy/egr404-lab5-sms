# lab5 SMS campaign website

This folder contains GitHub Pages for the **registered brand: lab5** (EGR404 educational mood playlist project).

## Publish updates
1. In your existing GitHub repository, upload the updated `index.html`, `privacy.html`, `terms.html`, and `styles.css` files to the repository root. Confirm replacement of existing files, then commit.
2. Wait for GitHub Pages to redeploy. Open each URL in a private window.

## Required before A2P submission
- Verify `ibrahim.tahoun@uri.edu` is the intended, monitored public support email in `privacy.html` and `terms.html`.
- Verify actual data retention and edit `privacy.html` if your deployed implementation differs.
- Ensure the exact registered brand in Twilio is `lab5`.
- Confirm your production messaging service uses expected Twilio opt-out keyword handling, and your bot enforces consent. Do not claim that the illustrated exchange is an actual screenshot.
- Confirm the number and your published `START` invitation are correct and that the website URLs open publicly.
- Do not upload `.env`, tokens, phone logs, or client secrets.

## Program disclosure
Test participants (student and instructor) are invited to opt in by texting START to the registered SMS number. The program replies only to requests; frequency varies; message and data rates may apply. STOP opts out and HELP supplies help. No marketing. Outbound messaging remains unavailable until Twilio approves required registration.

## Optional reference implementation
A separately provided `sms_bot_reference.py` shows how to implement opt-in and mood routing. Review and merge it with your existing `sms_bot.py`; it does not automatically alter your local code.
