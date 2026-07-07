"""
All calls to the Anthropic API. Requires ANTHROPIC_API_KEY in the environment.
"""
import json
import re
import anthropic
import config

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def _text_from_response(response) -> str:
    return "".join(block.text for block in response.content if block.type == "text")


def make_daily_package(article: dict, headline_pool: list) -> dict:
    """
    One call that returns everything needed for the daily package:
    - 50-word English gist
    - 50-word Urdu gist
    - ~180 word full summary (English)
    - 8-10 important vocabulary words with Urdu meaning (CSS English prep habit)
    - 50 current-affairs MCQs (mix of Pakistan + International) as structured JSON
    """
    headlines_text = "\n".join(f"- {h['title']}: {h['summary']}" for h in headline_pool if h["title"])

    prompt = f"""You are helping a CSS/FIA exam candidate in Pakistan with daily preparation.

TODAY'S DAWN EDITORIAL:
Title: {article['title']}
Text: {article['full_text'][:6000]}

RECENT HEADLINE POOL (Pakistan + International, for MCQ variety):
{headlines_text[:6000]}

Produce a JSON object with EXACTLY these keys, and nothing else (no markdown fences, no preamble):

{{
  "english_gist_50_words": "exactly ~50 words summarizing the editorial's core argument, in English",
  "urdu_gist_50_words": "exactly ~50 words summarizing the same, written in Urdu script",
  "full_summary": "a 150-200 word English summary of the editorial covering its argument, context, and significance for CSS Current Affairs / Pakistan Affairs paper",
  "vocabulary": [
    {{"word": "difficult word from the article", "meaning_english": "concise English meaning", "meaning_urdu": "Urdu meaning"}}
  ],
  "mcqs": [
    {{
      "question": "MCQ text",
      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "answer": "A",
      "category": "Pakistan" or "International"
    }}
  ]
}}

Rules:
- "vocabulary" should have 8-10 entries of genuinely non-trivial words (CSS-exam level).
- "mcqs" must have EXACTLY 50 items, roughly half tagged "Pakistan" and half "International",
  based on the editorial plus the headline pool above, covering current affairs relevant to
  the CSS/FIA current affairs paper (institutions, policy, treaties, key figures, dates, geography).
- Do not fabricate facts not supported by the text; when unsure, write general-knowledge
  current-affairs MCQs consistent with the headlines given.
- Output must be valid JSON only.
"""

    response = client.messages.create(
        model=config.MODEL_NAME,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = _text_from_response(response)
    raw = re.sub(r"^```json|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    return json.loads(raw)


def find_css_relevant_pdfs(article_title: str) -> str:
    """
    Uses Claude's web_search tool to locate CSS-relevant PDF resources
    (past papers, FPSC syllabus notes, official reports) tied to today's topic.
    Returns plain text: a short list of titles + links.
    """
    prompt = f"""Search the web for high-quality, freely available PDF resources
(FPSC syllabus documents, official reports, past CSS/FIA papers, reputable
current-affairs digests) that are directly relevant to today's Dawn editorial
topic: "{article_title}".

Return a short plain-text list (max 5 items), each as:
Title - one line on why it's relevant - URL
No markdown formatting, no extra commentary."""

    response = client.messages.create(
        model=config.MODEL_NAME,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )
    return _text_from_response(response).strip()


def make_hourly_bulletin(headline_pool: list) -> str:
    """Short current-affairs bulletin for the hourly Telegram ping."""
    headlines_text = "\n".join(f"- {h['title']}" for h in headline_pool if h["title"])[:3000]

    prompt = f"""From these recent Dawn headlines, write a compact current-affairs
bulletin for a CSS exam candidate: 5-6 bullet points, each one line, mixing
Pakistan and International news, plain text only (no markdown symbols like * or #).

Headlines:
{headlines_text}
"""
    response = client.messages.create(
        model=config.MODEL_NAME,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return _text_from_response(response).strip()
