"""Real Estate Marketing & SEO agent CLI.

Sends a user query to an LLM through OpenRouter and prints the answer,
guided by a hardcoded real-estate SEO expert persona.

Usage:
    export OPENROUTER_API_KEY="sk-or-v1-..."
    python seo_agent.py "How do I rank a luxury condo listing in Austin?"
"""

import argparse
import os
import sys
from pathlib import Path

from openai import OpenAI, OpenAIError

try:  # optional: auto-load .env from the project root (real env vars still win)
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-v4.1-flash-1017"

SYSTEM_PROMPT = """\
You are an elite Digital Marketing and advanced SEO expert who specializes \
exclusively in the real estate sector.

Follow these rules strictly:
- Deliver actionable strategies, never generic marketing filler. Every \
recommendation must be something the user can execute today.
- Prioritize long-tail keyword optimization: surface specific buyer-intent \
and seller-intent search phrases, and explain where to place them (titles, \
headings, meta descriptions, listing copy, blog structure).
- Write persuasive property listing copywriting when asked: benefit-led \
headlines, sensory neighborhood detail, and clear calls to action that \
convert viewers into inquiries.
- Apply proven lead conversion tactics: landing page structure, lead magnet \
ideas, follow-up timing, and trust signals tailored to real estate audiences.
- Structure every answer with clear headings and bullet points, and adapt \
tactics to the user's market, property type, and budget when they provide them.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ask the Real Estate Marketing & SEO agent a question.",
        epilog='Run with no query to enter interactive chat mode (type "exit" or Ctrl+D to quit).',
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="The marketing or SEO question to ask (quote multi-word queries)",
    )
    return parser


def ask(client: OpenAI, messages: list[dict[str, str]]) -> str | None:
    """Send the conversation to OpenRouter and return the reply text."""
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
    except OpenAIError as exc:
        print(f"Error: OpenRouter request failed: {exc}", file=sys.stderr)
        return None
    content = response.choices[0].message.content
    return content if content else None


def chat_loop(client: OpenAI) -> int:
    """Interactive mode: keeps conversation history until exit/Ctrl+D."""
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Real Estate SEO agent - interactive mode. Type 'exit' or Ctrl+D to quit.")
    while True:
        try:
            query = input("\nYou: ").strip()
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            return 0
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            return 0

        messages.append({"role": "user", "content": query})
        reply = ask(client, messages)
        if reply is None:
            messages.pop()  # drop the failed turn; let the user retry
            continue
        messages.append({"role": "assistant", "content": reply})
        print(f"\nAgent:\n{reply}")


def main() -> int:
    args = build_parser().parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        print(
            "Error: OPENROUTER_API_KEY is not set. "
            'Export it first: export OPENROUTER_API_KEY="sk-or-v1-..."',
            file=sys.stderr,
        )
        return 1

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)

    if args.query is None:
        return chat_loop(client)

    reply = ask(client, [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": args.query},
    ])
    if reply is None:
        return 1
    print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
