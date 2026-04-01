import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8310232049:AAF3BLFwO2XqgDrxLhQD2--G-PDZ9gRCUtQ"

data = {

"DE": {
    "cities": [
        "Berlin","Hamburg","München","Köln","Frankfurt","Stuttgart","Düsseldorf",
        "Dortmund","Essen","Leipzig","Bremen","Dresden","Hannover","Nürnberg",
        "Bochum","Wuppertal","Bielefeld","Bonn","Mannheim","Karlsruhe",
        "Augsburg","Wiesbaden","Münster","Gelsenkirchen","Aachen",
        "Braunschweig","Chemnitz","Kiel","Magdeburg","Freiburg",
        "Krefeld","Lübeck","Oberhausen","Erfurt","Mainz",
        "Rostock","Kassel","Hagen","Potsdam","Saarbrücken",
        "Hamm","Mülheim","Ludwigshafen","Leverkusen","Oldenburg",
        "Osnabrück","Solingen","Heidelberg","Herne"
    ],
    "names": [
        "Lukas Müller","Leon Schmidt","Finn Schneider","Paul Fischer",
        "Jonas Weber","Max Wagner","Luis Becker","Noah Hoffmann",
        "Elias Schäfer","Tim Koch","David Bauer","Jan Richter",
        "Felix Wolf","Moritz Schröder"
    ],
    "prefix": "+49 15"
},

"US": {
    "cities": [
        "New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia",
        "San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville",
        "Fort Worth","Columbus","Charlotte","San Francisco","Indianapolis",
        "Seattle","Denver","Washington","Boston","El Paso","Detroit",
        "Nashville","Memphis","Portland","Oklahoma City","Las Vegas",
        "Louisville","Baltimore","Milwaukee","Albuquerque","Tucson",
        "Fresno","Sacramento","Mesa","Atlanta","Kansas City",
        "Colorado Springs","Miami","Raleigh","Omaha","Long Beach",
        "Virginia Beach","Oakland","Minneapolis","Tulsa"
    ],
    "names": [
        "James Smith","Michael Johnson","Robert Williams",
        "David Brown","William Jones","Richard Garcia",
        "Joseph Miller","Thomas Davis","Charles Wilson"
    ],
    "prefix": "+1 20"
},

"UK": {
    "cities": [
        "London","Manchester","Birmingham","Leeds","Glasgow","Liverpool",
        "Bristol","Sheffield","Edinburgh","Leicester","Coventry",
        "Bradford","Cardiff","Belfast","Nottingham","Hull",
        "Newcastle","Stoke","Southampton","Derby","Portsmouth",
        "Brighton","Plymouth","Luton","Reading","Wolverhampton",
        "Bolton","Aberdeen","Norwich","Swansea","Milton Keynes",
        "Oxford","Cambridge","York","Exeter","Dundee"
    ],
    "names": [
        "Oliver Smith","George Jones","Harry Taylor",
        "Jack Brown","Charlie Williams","Thomas Wilson"
    ],
    "prefix": "+44 7"
},

"TR": {
    "cities": [
        "Istanbul","Ankara","Izmir","Bursa","Antalya","Adana",
        "Konya","Gaziantep","Mersin","Diyarbakir","Kayseri",
        "Eskisehir","Trabzon","Samsun","Denizli","Sanliurfa",
        "Malatya","Erzurum","Van","Balikesir","Kahramanmaras",
        "Aydin","Tekirdag","Manisa","Kocaeli","Sakarya",
        "Elazig","Hatay","Corum","Afyon"
    ],
    "names": [
        "Ahmet Yılmaz","Mehmet Kaya","Mustafa Demir",
        "Ali Çelik","Hüseyin Şahin","Hasan Yıldız"
    ],
    "prefix": "+90 5"
},

"XK": {
    "cities": [
        "Pristina","Prizren","Peja","Gjakova","Gjilan","Ferizaj",
        "Mitrovica","Podujeva","Vushtrri","Suhareka","Rahovec",
        "Drenas","Skenderaj","Istog","Kacanik","Lipjan",
        "Kamenica","Dragash","Obiliq","Decan"
    ],
    "names": [
        "Muhamet Fejzi","Arben Krasniqi","Besnik Berisha",
        "Luan Gashi","Flamur Shala","Valon Hoxha"
    ],
    "prefix": "+383 4"
}

}

# 🌍 Flag
def get_flag(code):
    if code == "XK":
        return "🇽🇰"
    return "".join(chr(127397 + ord(c)) for c in code)

# 🤖 Command
async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower().split()

    if len(text) < 2:
        await update.message.reply_text("❌ Beispiel: /fake de")
        return

    country = text[1].upper()

    if country not in data:
        await update.message.reply_text("❌ Land nicht vorhanden")
        return

    d = data[country]

    name = random.choice(d["names"])
    city = random.choice(d["cities"])
    street = f"{random.choice(['Main Street','Bahnhofstraße','High Street','Rue'])} {random.randint(1,200)}"
    postcode = random.randint(10000,99999)
    phone = f"{d['prefix']}{random.randint(1000000,9999999)}"
    email = name.lower().replace(" ", ".") + "@example.com"

    msg = f"""
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

    await update.message.reply_text(msg)

# ▶️ Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot läuft 🚀")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fake", fake))

print("Bot läuft...")
app.run_polling()
