import os
from turtle import update

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from parser import extract_text, extract_text_from_pdf
# from ticket_parser import parse_ticket, format_ticket_summary
# from entity_extractor import extract_entities, format_entities

from ml_extractor import extract_ml_entities, format_ml_entities





load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Smart Travel Assistant Bot\n\n"
        "Send me:\n"
        "- Ticket photo\n"
        "- PDF ticket\n\n"
        "I will try to extract travel information."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    photo = update.message.photo[-1]

    file = await context.bot.get_file(photo.file_id)

    os.makedirs("downloads", exist_ok=True)

    file_path = "downloads/ticket.jpg"

    await file.download_to_drive(file_path)

    await update.message.reply_text(
        "📸 Photo received.\n"
        "Reading text with OCR..."
    )

    extracted_text = extract_text(file_path)

    await update.message.reply_text(
        f"📄 Extracted text:\n\n{extracted_text}"
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document.file_name.lower().endswith(".pdf"):

        await update.message.reply_text(
            "❌ Please send PDF file only."
        )

        return

    file = await context.bot.get_file(document.file_id)

    os.makedirs("downloads", exist_ok=True)

    file_path = f"downloads/{document.file_name}"

    await file.download_to_drive(file_path)

    await update.message.reply_text(
        "📄 PDF received. Reading text..."
    )

    extracted_text = extract_text_from_pdf(file_path)
    
    ml_entities = extract_ml_entities(extracted_text)

    summary = format_ml_entities(ml_entities)

    await update.message.reply_text(summary)

def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN not found. Check your .env file."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(filters.PHOTO, handle_photo)
    )

    app.add_handler(
        MessageHandler(filters.Document.PDF, handle_document)
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()