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

def create_skb_row(name, price, chg, vol, pow, rsi, flow, bubble, cmd, strat, sup="---"):
    return [name, price, chg, get_iran_time(), vol, pow, "---", "---", rsi, "---", "---", "---", flow, sup, cmd, strat]

def update_system():
    print(f"در حال پاکسازی و چیدمان مجدد... {get_iran_time()}")
    
    # الف) لیست شکار (ردیف ۴ تا ۱۳) - ۱۰ ردیف اختصاصی
    hunts = [
        create_skb_row("خساپا", "2,450", "+3%", "بالا", "2.8", "52", "ورود پول", "---", "Buy", "کوتاه مدت", "2,380"),
        create_skb_row("خودرو", "3,100", "+2%", "بالا", "2.1", "48", "پول هوشمند", "---", "Buy", "کوتاه مدت", "2,950")
    ]
    # پر کردن بقیه ردیف‌های شکار با خط تیره برای جلوگیری از تداخل
    while len(hunts) < 10:
        hunts.append(["---"] * 16)
    worksheet.update(range_name="A4:P13", values=hunts)

    # ب) خودرو و مسکن (ردیف ۱۵ و ۱۶) - انتقال به بعد از لیست شکار
    assets = [
        create_skb_row("پژو ۲۰۷ | خودرو", "950M", "0%", "کم", "0.8", "---", "رکود", "---", "Wait", "بلند مدت"),
        create_skb_row("آپارتمان ۵ | مسکن", "120M/m", "+1%", "کم", "1.2", "---", "ارزش ذاتی", "---", "Buy", "بلند مدت")
    ]
    worksheet.update(range_name="A15:P16", values=assets)

    # ج) انتقال اصول استراتژی به ردیف ۶۰ (جایی که تداخل ایجاد نکند)
    edu_box = [
        ["--- شناسنامه استراتژی S.K.B (مشاور هوشمند) ---"],
        ["تحلیل جریان پول (M) | لایه‌های تحلیلی فرمان (O) | بازه زمانی ۸۵-۱۵ (P)"]
    ]
    worksheet.update(range_name="A60:A61", values=edu_box)
    print("تثبیت نهایی انجام شد.")

while True:
    try:
        update_system()
        time.sleep(60)
    except Exception as e:
        print(f"خطا: {e}")
        time.sleep(20)