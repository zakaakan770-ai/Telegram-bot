import random
from faker import Faker
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8310232049:AAF3BLFwO2XqgDrxLhQD2--G-PDZ9gRCUtQ"

# 🌍 Länder Mapping
countries = {
    "DE": "de_DE", "US": "en_US", "FR": "fr_FR", "GB": "en_GB",
    "ES": "es_ES", "IT": "it_IT", "NL": "nl_NL", "CH": "de_CH",
    "TR": "tr_TR", "IN": "en_IN", "BR": "pt_BR", "CA": "en_CA",
    "AU": "en_AU", "DK": "da_DK", "FI": "fi_FI", "NO": "no_NO",
    "IE": "en_IE", "MX": "es_MX", "RS": "sr_RS", "MY": "en_MY",
    "XK": "xk"
}

# 🇩🇪 Flag Generator
def get_flag(country_code):
    if country_code.upper() == "XK":
        return "🇽🇰"
    return "".join(chr(127397 + ord(c)) for c in country_code.upper())

# 📞 Telefonnummern
def generate_phone(region):
    prefixes = {
        "DE": "+49 15",
        "US": "+1 20",
        "FR": "+33 6",
        "GB": "+44 7",
        "TR": "+90 5",
        "RS": "+381 6",
        "MY": "+60 1"
    }

    prefix = prefixes.get(region.upper(), "+00")
    number = random.randint(1000000, 9999999)
    return f"{prefix}{number}"

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

        # 🇽🇰 KOSOVO CUSTOM
        if country == "XK":
            name = random.choice([
                "Arben Krasniqi", "Besnik Berisha", "Luan Gashi",
                "Flamur Hoxha", "Valon Shala", "Driton Kelmendi",
                "Arta Krasniqi", "Blerta Gashi", "Elira Berisha",
                "Muhamet Fejzi"
            ])

            street = random.choice([
                "Rruga Bill Clinton", "Rruga Nënë Tereza",
                "Rruga UÇK", "Rruga Dardania", "Abdullah Presheva 228"
            ]) + f" {random.randint(1, 200)}"

            city = random.choice([
                "Pristina", "Prizren", "Peja", "Gjakova", "Ferizaj"
            ])

            postcode = str(random.randint(10000, 70000))
            email = name.lower().replace(" ", ".") + "@gmail.com"
            phone = "+383 " + random.choice(["44","45","49"]) + str(random.randint(1000000,9999999))

        # 🌍 ANDERE LÄNDER
        else:
            fake = Faker(countries[country])

            name = fake.name()
            street = fake.street_address()
            city = fake.city()
            postcode = fake.postcode()
            email = fake.email()
            phone = generate_phone(country)

        flag = get_flag(country)

        # 🎨 DEIN ORIGINAL FORMAT (UNVERÄNDERT)
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
