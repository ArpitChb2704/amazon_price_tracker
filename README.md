# 🛍️ Amazon Price Tracker

Track Amazon product prices, get notified via email when prices drop, and manage your tracked items through a simple Streamlit web interface. 
Uses Supabase and Gmail API integration.

## 🔧 Features

✅ Add any Amazon product to track by URL
🤑 Set your target price
📧 Get email alerts when prices drop below your target
☁️ Powered by:
Streamlit (Frontend)
Supabase (Backend)
Gmail API (Emailing)
🔐 Secrets managed via Render environment variables

## Project Structure

<pre lang="markdown"> ``` 📁 Project Structure amazon-price-tracker/ 
      ├── app.py # Streamlit frontend 
      ├── check_prices.py # Background price checker (optional cron) 
      ├── emailing.py # Gmail API integration 
      ├── dataset.py # Supabase DB operations 
      ├── requirements.txt 
      ├── .env (local only) # Contains sensitive keys (not pushed) 
      ├── README.md ``` </pre>

## UI 
<img width="717" alt="Screenshot 2025-07-10 at 12 11 17 PM" src="https://github.com/user-attachments/assets/deac4a32-fde7-4140-97d8-d24805bd5d26" />

<img width="1462" alt="Screenshot 2025-07-10 at 12 12 48 PM" src="https://github.com/user-attachments/assets/8c575ab3-7b51-41aa-b84b-94ce6754360d" />

<img width="1038" alt="Screenshot 2025-07-10 at 12 23 05 PM" src="https://github.com/user-attachments/assets/7b04fa4d-883a-45f2-bb9a-e2d87cea121c" />






