import os
import feedparser
import json
import time
import hashlib
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
from dateutil import parser

# Configuration
SENT_NEWS_DIR = "sent_news"
WEBHOOKS_FILE = "webhooks.json"
FEED_URL = "https://www.logic-sunrise.com/forums/rss/forums/1-news-fr/"
MAX_DESCRIPTION_CHARACTERS = 200
CHECK_INTERVAL_SECONDS = 240  # 4 minutes


def ensure_directory_exists(directory):
    """Ensure the specified directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_webhook_id(webhook_url, thread_id):
    """Generate a unique identifier for a webhook using its URL and thread ID."""
    unique_string = f"{webhook_url}-{thread_id}"
    return hashlib.sha256(unique_string.encode("utf-8")).hexdigest()


def hash_title(title):
    """Generate a SHA-256 hash for the title."""
    return hashlib.sha256(title.encode("utf-8")).hexdigest()


def load_webhooks():
    """Load webhook configurations from the JSON file."""
    if not os.path.exists(WEBHOOKS_FILE):
        raise FileNotFoundError(f"Configuration file '{WEBHOOKS_FILE}' not found!")
    with open(WEBHOOKS_FILE, "r") as file:
        return json.load(file).get("webhooks", [])


def load_sent_news_for_webhook(webhook_id):
    """Load the sent news hashes for a specific webhook."""
    ensure_directory_exists(SENT_NEWS_DIR)
    filepath = os.path.join(SENT_NEWS_DIR, f"{webhook_id}.json")
    if not os.path.exists(filepath):
        return set()
    with open(filepath, "r") as file:
        content = file.read().strip()
        return set(json.loads(content)) if content else set()


def save_sent_news_for_webhook(webhook_id, sent_hashes):
    """Save the sent news hashes for a specific webhook."""
    ensure_directory_exists(SENT_NEWS_DIR)
    filepath = os.path.join(SENT_NEWS_DIR, f"{webhook_id}.json")
    with open(filepath, "w") as file:
        json.dump(list(sent_hashes), file)


def parse_rss_feed(feed_url, sent_hashes):
    """Parse the RSS feed and return new entries not yet sent, ordered by oldest first."""
    feed = feedparser.parse(feed_url)
    new_entries = []
    for entry in feed.entries:
        title = entry.title.strip()
        title_hash = hash_title(title)
        if title_hash not in sent_hashes:
            description, image_url = extract_description_and_image(entry.description)
            new_entries.append({
                "title": title,
                "title_hash": title_hash,
                "link": entry.link,
                "description": description,
                "image_url": image_url,
                "pubDate": entry.published,
                "pubDate_parsed": parser.parse(entry.published)  # Parse the date for sorting
            })
    # Sort by publication date (oldest first)
    new_entries.sort(key=lambda x: x["pubDate_parsed"])
    return new_entries


def extract_description_and_image(description):
    """Clean and extract text and the first image from the description."""
    soup = BeautifulSoup(description, "html.parser")
    text_content = soup.get_text().strip()

    # Remove empty lines and limit description length
    lines = [line.strip() for line in text_content.splitlines() if line.strip()]
    cleaned_text = " ".join(lines)
    if len(cleaned_text) > MAX_DESCRIPTION_CHARACTERS:
        cleaned_text = cleaned_text[:MAX_DESCRIPTION_CHARACTERS] + "..."

    # Find the first image
    img_tag = soup.find("img")
    image_url = img_tag["src"] if img_tag else None

    return cleaned_text, image_url


def send_news_to_discord(entry, webhook_url, thread_id):
    """Send a news entry to Discord using the provided webhook."""
    webhook = DiscordWebhook(
        url=webhook_url,
        username="Logic-Sunrise Bot",
        avatar_url="https://www.logic-sunrise.com/forums/public/style_images/LSv4/logo.png"
    )
    if thread_id:
        webhook.thread_id = thread_id

    # Build embed message
    embed = DiscordEmbed(
        title=entry["title"],
        description=entry["description"],
        url=entry["link"],
        color=0xFFA500
    )
    embed.set_author(
        name="Logic-Sunrise",
        url="https://www.logic-sunrise.com",
        icon_url="https://www.logic-sunrise.com/forums/public/style_images/LSv4/logo.png"
    )
    embed.add_embed_field(name="Date", value=entry["pubDate"], inline=False)
    if entry["image_url"]:
        embed.set_image(url=entry["image_url"])
    embed.set_footer(text="@ Logic-Sunrise • Powered by LS Bot")
    embed.set_timestamp()

    webhook.add_embed(embed)
    webhook.content = "🆕 Une nouvelle News Hack est dispo sur Logic-Sunrise:"
    response = webhook.execute()

    if response.status_code != 200:
        print(f"Failed to send {entry['title']}: {response.status_code}")


def main():
    """Main function to monitor and send news."""
    print("Starting script...")

    while True:
        webhooks = load_webhooks()

        for webhook_data in webhooks:
            webhook_url = webhook_data.get("url")
            thread_id = webhook_data.get("thread_id", "default")
            if not webhook_url:
                print("Invalid webhook configuration. Skipping.")
                continue

            webhook_id = generate_webhook_id(webhook_url, thread_id)
            sent_hashes = load_sent_news_for_webhook(webhook_id)

            new_entries = parse_rss_feed(FEED_URL, sent_hashes)
            if new_entries:
                print(f"{len(new_entries)} new entries found for webhook ID {webhook_id}.")
                for entry in new_entries:
                    send_news_to_discord(entry, webhook_url, thread_id)
                    sent_hashes.add(entry["title_hash"])
                save_sent_news_for_webhook(webhook_id, sent_hashes)
            else:
                print(f"No new entries for webhook ID {webhook_id}.")

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
