# CSS/FIA Daily Dawn Agent

Automates daily CSS/FIA prep from Dawn newspaper and delivers it to your Telegram.

## What it does

**Daily package (once a day, ~8:00 AM PKT):**
- Fetches today's Dawn editorial
- 50-word gist in English
- 50-word gist in Urdu
- Full ~180-word summary
- 8-10 important vocabulary words (CSS English relevance) with Urdu meanings
- Suggests CSS-relevant PDF resources found via web search
- Generates 50 current affairs MCQs (mixed Pakistan + International), packaged
  into a PDF with an answer key, and sends it as a Telegram document

**Hourly ping (24x a day):**
- A short 5-6 line current affairs bulletin from the latest Pakistan + World headlines

## One-time setup (10 minutes)

### 1. Create a GitHub repo
- Go to github.com -> New repository (e.g. `css-dawn-agent`). Can be public or private.
- Upload all files in this folder, preserving the `.github/workflows/` folder structure.

### 2. Add your secrets
Repo -> **Settings -> Secrets and variables -> Actions -> New repository secret**. Add:

| Secret name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key from console.anthropic.com |
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | `6345421988` (already set as a default in config.py, but the secret takes priority) |

### 3. Enable Actions
Repo -> **Actions** tab -> click "I understand my workflows, go ahead and enable them" if prompted.

### 4. Test it manually first
Repo -> **Actions** -> select "Daily CSS Current Affairs Package" -> **Run workflow**.
Check your Telegram — you should get the text package + PDF within ~1-2 minutes.
Do the same for "Hourly Current Affairs Ping".

Once both manual runs work, the schedules take over automatically — no further action needed.

## Important things to know

- **GitHub scheduled workflows pause after 60 days with zero repo activity.** Just push
  any small commit (or manually run a workflow) every couple of months to keep it alive.
- **Cron timing on GitHub is "best effort"** — during high load it can run a few minutes
  late. This is a GitHub platform behavior, not something in the code.
- **Cost**: Anthropic API usage is pay-as-you-go on your key. 24 hourly calls + 1 daily
  call (which generates 50 MCQs, a heavier call) per day is a modest, predictable load —
  check console.anthropic.com for your usage/billing.
- **Public vs private repo**: if you make the repo public, GitHub Actions minutes are
  unlimited/free. If private, GitHub gives a free minutes quota per month, which this
  workload comfortably fits within, but do check the Actions usage tab occasionally.
- If Dawn changes its site's HTML structure, `fetch_article._fetch_full_text()` might
  return less content than usual — it falls back gracefully to the RSS summary,
  so the pipeline won't break, just occasionally rely on a shorter source text.

## File overview

- `config.py` — reads secrets/settings from environment
- `fetch_article.py` — pulls today's editorial + headline pool via Dawn RSS feeds
- `ai_processor.py` — all Claude API calls (summary, gists, vocab, 50 MCQs, PDF search)
- `pdf_builder.py` — builds the daily MCQ PDF
- `telegram_bot.py` — sends text/documents to your Telegram chat
- `main_daily.py` — orchestrates the once-a-day full package
- `main_hourly.py` — orchestrates the lightweight hourly bulletin
- `.github/workflows/daily.yml`, `.github/workflows/hourly.yml` — the schedules
