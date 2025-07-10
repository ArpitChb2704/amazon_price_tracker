# price_checker.py

import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from emailing import send_email  # ✅ Imported from your uploaded file
from supabase import create_client
import os 
from dotenv import load_dotenv

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15"
    }

load_dotenv()  # Load from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



print("🔍 Checking for price alerts...")


def check_prices():
    # Step 1: Fetch all tracking records
    response = supabase.table("track_data").select("*").execute()
    if not response.data:
        print("❌ Failed to fetch data from Supabase.")
        return
    
    track_items = response.data

    for item in track_items:
        try:
            # Step 2: Scrape Amazon price
            r = requests.get(item["url"], headers=headers)
            soup = BeautifulSoup(r.content, "html.parser")
            price_tag = soup.select_one('span.a-price span.a-offscreen')

            current_price = float(price_tag.get_text(strip=True).replace("₹", "").replace(",", "")) if price_tag else None

            print(f"👉 {item['title']}")
            print(f"💰 Current: {current_price}, Target: {item['target_price']}")

            if current_price and current_price <= item["target_price"]:
                # Step 3: Compose email body
                body = f"""🔔 Price Alert: Your tracked product is now cheaper!\n
🛍️ Product: {item['title']}
💸 Current Price: ₹{current_price}
🎯 Your Target Price: ₹{item['target_price']}
🔗 Link: {item['url']}

-- Amazon Price Tracker"""

                # Step 4: Send email
                send_email(to=item["email"], message_text=body, subject="Amazon Price Tracker")

                print(f"[{datetime.now()}] ✅ Email sent to {item['email']}")

            # Step 5: Update last_checked timestamp
            supabase.table("track_data").update({
                "last_checked": datetime.now().isoformat()
            }).eq("id", item["id"]).execute()

        except Exception as e:
            print(f"❌ Error checking {item['title']}: {e}")


if __name__ == "__main__":
    check_prices()
