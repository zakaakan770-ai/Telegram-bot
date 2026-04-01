import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8310232049:AAF3BLFwO2XqgDrxLhQD2--G-PDZ9gRCUtQ"

# 🌍 80+ Länder Codes
all_countries = [
    "de","us","gb","fr","it","es","nl","ch","tr","ca","au","in","br","my",
    "dk","fi","no","se","ie","mx","ar","cl","co","za","ng","eg","sa","ae",
    "jp","kr","cn","th","vn","ph","id","pk","bd","pl","cz","at","be","pt",
    "gr","hu","ro","sk","si","hr","bg","lt","lv","ee"
]

# 🇽🇰 Kosovo FIX
kosovo_data = {
    "first": ["Arben","Luan","Senat","Driton","Valon"],
    "last": ["Krasniqi","Gashi","Fejzi","Berisha","Shala"],
    "cities": ["Pristina","Prizren","Peja","Gjilan","Gjakova"],
    "streets": ["Skenderbeu","Nënë Tereza","Adem Jashari"]
}

def get_flag(code):
    if code.upper() == "XK":
        return "🇽🇰"
    return "".join(chr(127397 + ord(c)) for c in code.upper())

def get_user(country):
    try:
        url = f"https://randomuser.me/api/?nat={country}&results=1"
        res = requests.get(url, timeout=5).json()
        return res["results"][0]
    except:
        return None

async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # zufälliges Land aus 80+
    country = random.choice(all_countries).upper()

    # 🇽🇰 Kosovo separat
    if country == "XK":
        name = f"{random.choice(kosovo_data['first'])} {random.choice(kosovo_data['last'])}"
        city = random.choice(kosovo_data["cities"])
        street = f"{random.choice(kosovo_data['streets'])} {random.randint(1,200)}"
        postcode = str(random.randint(10000,99999))
        phone = f"+383 {random.randint(40,49)} {random.randint(100000,999999)}"
        email = name.lower().replace(" ", ".") + "@example.com"

    else:
        user = get_user(country.lower())

        if not user:
            await update.message.reply_text("❌ Fehler")
            return

        name = f"{user['name']['first']} {user['name']['last']}"
        street = f"{user['location']['street']['name']} {random.randint(1,200)}"
        city = user['location']['city']
        postcode = str(user['location']['postcode'])
        email = user['email']

        phone = f"+{random.randint(1,99)} {random.randint(100000000,999999999)}"

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

    await update.message.reply_text(text.strip(), parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selam Quzeng")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fake", gen))

print("Bot läuft 🚀")
app.run_polling()
