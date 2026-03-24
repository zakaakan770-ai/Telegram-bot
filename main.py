import random
import requests
import phonenumbers
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
def get_flag(country_code):
    return "".join(chr(127397 + ord(c)) for c in country_code.upper())


TOKEN = "8310232049:AAF3BLFwO2XqgDrxLhQD2--G-PDZ9gRCUtQ"

countries = {
    "DE": "de", "US": "us", "FR": "fr", "GB": "gb",
    "ES": "es", "IT": "it", "NL": "nl", "CH": "ch",
    "TR": "tr", "IN": "in", "BR": "br", "CA": "ca",
    "AU": "au", "DK": "dk", "FI": "fi", "NO": "no",
    "IE": "ie", "MX": "mx"
}

def generate_phone(region):
    try:
        number = phonenumbers.example_number(region.upper())
        return phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
    except:
        return "N/A"

def get_user(country):
    try:
        url = f"https://randomuser.me/api/?nat={country}"
        res = requests.get(url, timeout=5).json()
        return res["results"][0]
    except:
        return None

# ✅ async jetzt!
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    amount = 1
    if len(args) >= 2 and args[1].isdigit():
        amount = min(int(args[1]), 10)

    if args:
        country = args[0].upper()
        if country not in countries:
            await update.message.reply_text("❌ Land nicht gefunden")
            return
    else:
        country = random.choice(list(countries.keys()))

    results = []

    for _ in range(amount):
        user = get_user(countries[country])

        if not user:
            continue

        name = f"{user['name']['first']} {user['name']['last']}"
        street = f"{user['location']['street']['name']} {user['location']['street']['number']}"
        city = user['location']['city']
        postcode = user['location']['postcode']
        email = user['email']
        phone = generate_phone(country)
        user_id = random.randint(100000, 999999)
flag = get_flag(country)
text = f"""
📍Address Generator
𝗖𝗼𝘂𝗻𝘁𝗿𝘆:
{flag}
𝗡𝗮𝗺𝗲: 
{name}
𝗔𝗱𝗱𝗿𝗲𝘀𝘀:
{street}
𝗖𝗶𝘁𝘆/𝗧𝗼𝘄𝗻/𝗩𝗶𝗹𝗹𝗮𝗴𝗲:
{city}
𝗣𝗼𝘀𝘁𝗰𝗼𝗱𝗲:
{postcode}
𝗡𝘂𝗺𝗯𝗲𝗿:
{phone}
"""
        results.append(text.strip())

    if results:
        await update.message.reply_text("\n\n---\n\n".join(results))
    else:
        await update.message.reply_text("❌ Fehler beim Laden")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selam Quzeng"
    )

# 🚀 Start
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fake", gen))

print("Bot läuft... 🚀")
app.run_polling()
