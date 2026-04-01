import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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

# 🇽🇰 Kosovo
kosovo_first = ["Arben", "Besnik", "Luan", "Flamur", "Valon", "Jeton", "Driton"]
kosovo_last = ["Krasniqi", "Berisha", "Gashi", "Shala", "Hoxha", "Morina"]

# 🇩🇪 Deutschland
german_first = ["Max", "Leon", "Paul", "Lukas", "Finn", "Marie", "Sophie", "Anna"]
german_last = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber"]
german_streets = ["Hauptstraße", "Bahnhofstraße", "Schulstraße", "Gartenstraße"]
german_data = {
    "Berlin": ("10115", "030"),
    "Hamburg": ("20095", "040"),
    "München": ("80331", "089"),
    "Köln": ("50667", "0221")
}

# 🇺🇸 USA
us_first = ["James", "John", "Robert", "Michael", "William"]
us_last = ["Smith", "Johnson", "Brown", "Jones", "Garcia"]
us_streets = ["Main St", "Oak St", "Pine St", "Maple Ave"]
us_data = {
    "New York": ("10001", "212"),
    "Los Angeles": ("90001", "213"),
    "Chicago": ("60601", "312")
}

# 🇬🇧 UK
uk_first = ["Oliver", "George", "Harry", "Jack"]
uk_last = ["Smith", "Jones", "Taylor", "Brown"]
uk_streets = ["High Street", "Station Road", "Park Road"]
uk_data = {
    "London": ("SW1A 1AA", "020"),
    "Manchester": ("M1 1AE", "0161"),
    "Birmingham": ("B1 1AA", "0121")
}

# 🇩🇪 Flag
def get_flag(code):
    if code == "XK":
        return "🇽🇰"
    return "".join(chr(127397 + ord(c)) for c in code)

# 📞 Default Nummern
def generate_phone(region):
    return f"+00 {random.randint(100000000, 999999999)}"

# 👤 API
def get_user(country):
    try:
        url = f"https://randomuser.me/api/?nat={country}&inc=name,location,email&noinfo"
        return requests.get(url, timeout=5).json()["results"][0]
    except:
        return None

# 🤖 Generator
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

        # 🇽🇰 Kosovo
        if country == "XK":
            name = f"{random.choice(kosovo_first)} {random.choice(kosovo_last)}"
            street = f"Rruga {random.choice(['Skenderbeu','Nënë Tereza','Adem Jashari'])} {random.randint(1,100)}"
            city = random.choice(["Pristina", "Prizren", "Peja", "Gjilan"])
            postcode = str(random.randint(10000, 99999))
            phone = f"+383 4 {random.randint(1000000, 9999999)}"
            email = name.lower().replace(" ", ".") + "@example.com"

        # 🇩🇪 Deutschland
        elif country == "DE":
            name = f"{random.choice(german_first)} {random.choice(german_last)}"
            city = random.choice(list(german_data.keys()))
            postcode, area = german_data[city]
            street = f"{random.choice(german_streets)} {random.randint(1,200)}"
            phone = f"+49 {area} {random.randint(1000000, 9999999)}"
            email = name.lower().replace(" ", ".") + "@example.com"

        # 🇺🇸 USA
        elif country == "US":
            name = f"{random.choice(us_first)} {random.choice(us_last)}"
            city = random.choice(list(us_data.keys()))
            postcode, area = us_data[city]
            street = f"{random.randint(1,9999)} {random.choice(us_streets)}"
            phone = f"+1 {area} {random.randint(1000000, 9999999)}"
            email = name.lower().replace(" ", ".") + "@example.com"

        # 🇬🇧 UK
        elif country == "GB":
            name = f"{random.choice(uk_first)} {random.choice(uk_last)}"
            city = random.choice(list(uk_data.keys()))
            postcode, area = uk_data[city]
            street = f"{random.randint(1,200)} {random.choice(uk_streets)}"
            phone = f"+44 {area} {random.randint(1000000, 9999999)}"
            email = name.lower().replace(" ", ".") + "@example.com"

        # 🌍 andere Länder
        else:
            user = get_user(countries[country])
            if not user:
                continue

            name = f"{user['name']['first']} {user['name']['last']}"
            street = f"{user['location']['street']['name']} {random.randint(1,200)}"
            city = user['location']['city']
            postcode = str(user['location']['postcode'])
            phone = generate_phone(country)
            email = user['email']

        flag = get_flag(country)

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

    await update.message.reply_text("\n\n━━━━━━━━━━━━━━\n\n".join(results), parse_mode="Markdown")

# ▶️ Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selam Quzeng")

# 🚀 Start Bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fake", gen))

print("Bot läuft... 🚀")
app.run_polling()
