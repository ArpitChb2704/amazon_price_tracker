import supabase
from supabase.client import create_client, Client
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()  # Load from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_to_supabase(data):
    response = supabase.from_("track_data").insert([{
        "title": data["title"],
        "url": data["url"],
        "image_url": data["image_url"],
        "current_price": data["current_price"],
        "target_price": data["target_price"],
        "email": data["email"],
        "last_checked": datetime.now().isoformat()
    }]).execute()

    if response.data:
        print("✅ Data saved successfully!")
    else:
        print("❌ Error saving data:", response)