import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8310232049:AAF3BLFwO2XqgDrxLhQD2--G-PDZ9gRCUtQ"

# 🌍 Länder Daten (viele Städte + Namen)
data = {
    "DE": {
        "cities": [
            "Berlin","Hamburg","München","Köln","Frankfurt","Stuttgart","Düsseldorf",
            "Dortmund","Essen","Leipzig","Bremen","Dresden","Hannover","Nürnberg",
            "Bochum","Wuppertal","Bielefeld","Bonn","Mannheim","Karlsruhe",
            "Augsburg","Wiesbaden","Münster","Gelsenkirchen","Aachen",
            "Braunschweig","Chemnitz","Kiel","Magdeburg","Freiburg"
        ],
        "names": [
            "Lukas Müller","Leon Schmidt","Finn Schneider","Paul Fischer",
            "Jonas Weber","Max Wagner","Luis Becker","Noah Hoffmann",
            "Elias Schäfer","Tim Koch","David Bauer","Jan Richter",
            "Nico Klein","Felix Wolf","Moritz Schröder","Kevin Neumann"
        ],
        "prefix": "+49 15"
    },

    "US": {
        "cities": [
            "New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia",
            "San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville",
            "San Francisco","Columbus","Charlotte","Indianapolis","Seattle",
            "Denver","Boston","Detroit","Nashville","Memphis","Portland"
        ],
        "names": [
            "James Smith","Michael Johnson","Robert Williams","David Brown",
            "William Jones","Richard Garcia","Joseph Miller","Thomas Davis",
            "Charles Wilson","Daniel Anderson","Matthew Taylor"
        ],
        "prefix": "+1 20"
    },

    "UK": {
        "cities": [
            "London","Manchester","Birmingham","Leeds","Glasgow","Liverpool",
            "Bristol","Sheffield","Edinburgh","Leicester","Coventry",
            "Nottingham","Newcastle","Oxford","Cambridge"
        ],
        "names": [
            "Oliver Smith","George Jones","Harry Taylor","Jack Brown",
            "Charlie Williams","Thomas Wilson","Oscar Davies"
        ],
        "prefix": "+44 7"
    },

    "XK": {
        "cities": [
            "Pristina","Prizren","Peja","Gjakova","Gjilan","Ferizaj",
            "Mitrovica","Podujeva","Vushtrri","Suhareka","Rahovec"
        ],
        "names": [
            "Muhamet Fejzi","Arben Krasniqi","Besnik Berisha",
            "Luan Gashi","Flamur Shala","Valon Hoxha",
            "Jeton Mustafa","Blerim Selimi","Agon Zeka"
        ],
        "prefix": "+383 4"
    }
}

# 🌍 Flag
def get_flag(code):
    if code == "XK":
        return "🇽🇰"
    return "".join(chr(127397 + ord(c)) for c in code)

# 📞 Nummer
def generate_phone(prefix):
    return f"{prefix}{random.randint(1000000,9999999)}"

# 🤖 Generator
async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args:
        country = args[0].upper()
        if country not in data:
            await update.message.reply_text("❌ Land nicht vorhanden")
            return
    else:
        country = random.choice(list(data.keys()))

    d = data[country]

    name = random.choice(d["names"])
    city = random.choice(d["cities"])
    street = f"{random.choice(['Main Street','Bahnhofstraße','High Street','Rue'])} {random.randint(1,200)}"
    postcode = random.randint(10000,99999)
    phone = generate_phone(d["prefix"])
    email = name.lower().replace(" ", ".") + "@example.com"

    text = f"""
📍 Address Generator

Country: {country} {get_flag(country)}

Name:
{name}

Address:
{street}

City:
{city}

Postcode:
{postcode}

Phone:
{phone}

Email:
{email}
"""

    await update.message.reply_text(text)

# ▶️ Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot läuft 🚀")

# 🚀 Run
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fake", fake))

print("Bot läuft...")
app.run_polling()
