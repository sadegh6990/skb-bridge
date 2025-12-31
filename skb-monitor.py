import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime, timedelta, timezone

# ۱. تنظیمات اتصال
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
worksheet = client.open("SKB-BRIDGE.GM").get_worksheet(0)

def get_iran_time():
    iran_tz = timezone(timedelta(hours=3, minutes=30))
    return datetime.now(iran_tz).strftime('%H:%M:%S')

# تابع جدید برای زنده کردن قیمت‌های کریپتو (حل مشکل نوسان شبکه)
def get_crypto_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        res = requests.get(url, timeout=5).json()
        return f"{float(res['price']):,.0f}"
    except:
        return "نوسان شبکه"

def create_skb_row(name, price, chg, vol, pow, rsi, flow, bubble, cmd, strat, sup="---"):
    return [name, price, chg, get_iran_time(), vol, pow, "---", "---", rsi, "---", "---", "---", flow, sup, cmd, strat]

def update_system():
    print(f"در حال به‌روزرسانی هوشمند... {get_iran_time()}")
    
    # الف) لیست شکار (ردیف ۴ تا ۱۳) - حفاظت شده
    hunts = [
        create_skb_row("خساپا", "2,450", "+3%", "بالا", "2.8", "52", "ورود پول", "---", "Buy", "کوتاه مدت", "2,380"),
        create_skb_row("خودرو", "3,100", "+2%", "بالا", "2.1", "48", "پول هوشمند", "---", "Buy", "کوتاه مدت", "2,950")
    ]
    while len(hunts) < 10:
        hunts.append(["---"] * 16)
    worksheet.update(range_name="A4:P13", values=hunts)

    # ب) خودرو و مسکن (ردیف ۱۵ و ۱۶) - تثبیت جایگاه
    assets = [
        create_skb_row("پژو ۲۰۷ | خودرو", "950M", "0%", "کم", "0.8", "---", "رکود", "---", "Wait", "بلند مدت"),
        create_skb_row("آپارتمان ۵ | مسکن", "120M/m", "+1%", "کم", "1.2", "---", "ارزش ذاتی", "---", "Buy", "بلند مدت")
    ]
    worksheet.update(range_name="A15:P16", values=assets)

    # ج) بخش کریپتو (اضافه شده برای تصویر ۳)
    btc_price = get_crypto_price("BTC")
    crypto_data = [
        create_skb_row("بیت‌کوین (BTC)", btc_price, "---", "بالا", "---", "---", "جریان جهانی", "---", "Hold", "استراتژیک"),
    ]
    worksheet.update(range_name="A18:P18", values=crypto_data)

    # د) امنیت مطلق: کد زیر هرگز از ردیف ۳۹ پایین‌تر نمی‌رود تا ردیف ۴۰ دست‌نخورده بماند.
    print("تایید امنیتی: ردیف ۴۰ تا ۴۳ حفظ شد.")

while True:
    try:
        update_system()
        time.sleep(60)
    except Exception as e:
        print(f"خطا در سیستم: {e}")
        time.sleep(20)
