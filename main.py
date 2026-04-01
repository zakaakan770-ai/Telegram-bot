from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8310232049:AAF3BLFwO2XqgDrxLhQD2--G-PDZ9gRCUtQ"

# /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot läuft 🔥")

# /ping Command
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong 🏓")

# App erstellen
app = ApplicationBuilder().token(TOKEN).build()

# Commands hinzufügen
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))

# Bot starten
app.run_polling()
