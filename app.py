# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
from supabase import create_client
from datetime import datetime
from dataset import save_to_supabase
from dotenv import load_dotenv

load_dotenv()  # Load from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



st.title("🛍️ Amazon Price Tracker")

# Step 1: Input product URL
product_url = st.text_input("Enter Amazon Product URL")

if product_url:
    # Step 2: Scrape Title, Price, Image
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15"
    }
    page = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id='productTitle')
    title = title.get_text(strip=True) if title else "Title not found"

    price_span = soup.select_one('span.a-price span.a-offscreen')
    price = price_span.get_text(strip=True).replace("₹", "").replace(",", "") if price_span else None

    image_tag = soup.select_one('#imgTagWrapperId img')
    image_url = image_tag['src'] if image_tag else None

    st.subheader("Product Preview:")
    st.write(f"**Title:** {title}")
    st.write(f"**Current Price:** ₹{price if price else 'Not Found'}")
    if image_url:
        st.image(image_url, width=250)

    # Step 3: Ask Target Price and Email
    target_price = st.number_input("Enter your target price (₹)", min_value=0)
    email = st.text_input("Enter your email address")

    if st.button("✅ Start Tracking"):
        if price is None:
            st.error("Couldn't find the current price.")
        elif not email:
            st.error("Please enter a valid email.")
        else:
            tracker_data = {
                "title": title,
                "url": product_url,
                "image_url": image_url,
                "current_price": float(price),
                "target_price": float(target_price),
                "email": email,
                "last_checked": str(datetime.now())
            }

            # Save to Supabase Dataset 
            save_to_supabase(tracker_data)

            st.success("🎯 Tracking started! You'll get an email when the price drops.")
