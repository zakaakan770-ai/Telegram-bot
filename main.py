import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = "8310232049:AAF3BLFwO2XqgDrxLhQD2--G-PDZ9gRCUtQ"



# 🌍 Länder Mapping
countries = {
    "DE": "de", "US": "us", "FR": "fr", "GB": "gb",
    "ES": "es", "IT": "it", "NL": "nl", "CH": "ch",
    "TR": "tr", "IN": "in", "BR": "br", "CA": "ca",
    "AU": "au", "DK": "dk", "FI": "fi", "NO": "no",
    "IE": "ie", "MX": "mx", "RS": "rs", "MY": "my",
    "XK": "xk"
}

# 🇩🇪 Flag Generator
def get_flag(country_code):
    if country_code.upper() == "XK":
        return "🇽🇰"
    return "".join(chr(127397 + ord(c)) for c in country_code.upper())

# 📞 Realistischere Nummern
def generate_phone(region):
    prefixes = {
        "DE": "+49 15",
        "US": "+1 20",
        "FR": "+33 6",
        "GB": "+44 7",
        "TR": "+90 5"
    }

    prefix = prefixes.get(region.upper(), "+00")
    number = random.randint(1000000, 9999999)
    return f"{prefix}{number}"

# 👤 User Daten holen
def get_user(country):
    try:
        url = f"https://randomuser.me/api/?nat={country}&inc=name,location,email&noinfo"
        res = requests.get(url, timeout=5).json()
        return res["results"][0]
    except:
        return None

# 🤖 Fake Generator
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    amount = 1
    if len(args) >= 2 and args[1].isdigit():
        amount = min(int(args[1]), 5)

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

        # ✨ Schöne Daten
        name = f"{user['name']['first'].title()} {user['name']['last'].title()}"
        street_name = user['location']['street']['name'].title()
        street = f"{street_name} {random.randint(1, 200)}"
        city = user['location']['city'].title()
        postcode = str(user['location']['postcode'])
        email = user['email']
        phone = generate_phone(country)

        flag = get_flag(country)

        # 🎨 SCHÖNER OUTPUT
        text = f"""
📍 *Address Generator*

   *Country:* {country} {flag}

*Name:*
{name}

*Address:*
{street}

*City:*
{city}

*Postcode:*
{postcode}

*Phone:*
{phone}

*Email:*
{email}
"""

        results.append(text.strip())

    if results:
        await update.message.reply_text("\n\n━━━━━━━━━━━━━━\n\n".join(results), parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Fehler beim Generieren")

# ▶️ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selam Quzeng")

# 🚀 Bot starten
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fake", gen))

print("Bot läuft... 🚀")
app.run_polling()
