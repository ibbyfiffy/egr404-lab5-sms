# EGR404 Mood Playlist Bot — public compliance pages

This folder contains **only** the public-facing website for the educational SMS bot:

- `index.html` — SMS opt-in instructions and **illustrative** example messages.
- `privacy.html` — draft Privacy Policy.
- `terms.html` — draft Terms & Conditions.
- `styles.css` — shared design.

## BEFORE publishing or submitting the Twilio campaign

1. Open `privacy.html` and `terms.html`. Replace ALL `[BRACKETED PLACEHOLDERS]` with accurate, verifiable details. The registered brand name must match the Twilio filing. Use a monitored contact email (not an API key or phone credential).
2. Confirm whether your application stores phone numbers, opt-in state, SMS content, or logs, how long each is stored, and where. Describe that truthfully in `privacy.html`.
3. Implement and actually test any keyword workflow you advertise: START enrollment with confirmation, STOP opt-out, HELP responses, and consent storage. Consider Twilio's built-in Advanced Opt-Out feature; avoid conflicting automatic and custom responses.
4. Check your actual opt-in disclosures and make an authentic screenshot of your public signup page. Capture **real** START and confirmation messages after the flow is operational, where Twilio requests them. Do not treat the examples on the page as actual message logs.
5. Use an appropriately authorized number and complete the applicable messaging registration. Publishing these pages does not, by itself, resolve Twilio error 30034.
6. Ask the course instructor whether GitHub-hosted pages and your chosen two-participant testing model meet their expectations. Review all policy wording for accuracy before submission.

## Publishing through GitHub's website (no Git installation needed)

1. Create a **public** GitHub repository named `egr404-lab5-sms`.
2. Upload `index.html`, `privacy.html`, `terms.html`, and `styles.css` at the repository root. Do **not** upload your `.env` or application credentials.
3. Open **Settings → Pages**, choose **Deploy from a branch**, select **main** and **/(root)**, then **Save**.
4. After deployment, visit:
   - `https://YOUR-USERNAME.github.io/egr404-lab5-sms/`
   - `https://YOUR-USERNAME.github.io/egr404-lab5-sms/privacy.html`
   - `https://YOUR-USERNAME.github.io/egr404-lab5-sms/terms.html`
5. Open each page in a private/incognito browser window to confirm it is public.
6. Only after pages and workflows are accurate, paste the privacy and terms URLs into Twilio's required fields. The opt-in proof can reference the main signup page and genuine conversation evidence.

## Do not upload

- `.env`, API tokens, Twilio Auth Token, or Spotify Client Secret.
- Phone numbers of private testers except the intentionally published Twilio service number.
- Fabricated sample conversations represented as real test evidence.

These are **draft templates** for a student project, not a claim of carrier compliance or legal advice.
