import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading

# ----------------- Bot Configurations -----------------
bots = [
    {
        "name": "ViratBot",
        "token": "8413345646:AAHQkiZkWQf_2qM_k33JSf7NkXYwPHFUYKw",
        "file": r"C:\Users\FINRISE\Desktop\Telegram\My_data\Monish Sakpal Final.docx",
        "authorized_chat_id": None  # Anyone can access
    },
    {
        "name": "Birjubhaibot",
        "token": "8494020954:AAHEZ0AdNVeb1qQr9K8agEX-D-H81tKhBQ4",
        "file": r"C:\Users\FINRISE\Desktop\Telegram\My_data\Brijeshbhai.txt",
        "authorized_chat_id": [2032666794, 7388112318]  # Only authorized users
    }
]

# ----------------- Bot Handlers -----------------
def create_bot_app(bot_config):
    async def sendfile(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        print(f"[{bot_config['name']}] /sendfile accessed by Chat ID: {chat_id}")

        # Authorization check
        auth_ids = bot_config["authorized_chat_id"]
        if auth_ids is not None and chat_id not in auth_ids:
            await update.message.reply_text("❌ You are not authorized to access this file.")
            return

        # Check if file exists
        if not os.path.exists(bot_config["file"]):
            await update.message.reply_text(f"❌ File not found: {bot_config['file']}")
            print(f"[{bot_config['name']}] File not found: {bot_config['file']}")
            return

        # Send the designated file
        try:
            with open(bot_config["file"], "rb") as f:
                await update.message.reply_document(document=InputFile(f))
            await update.message.reply_text("✅ File sent successfully!")
            print(f"[{bot_config['name']}] Sent file: {bot_config['file']}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error sending file: {e}")
            print(f"[{bot_config['name']}] Error sending file: {e}")

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        print(f"[{bot_config['name']}] /start accessed by Chat ID: {chat_id}")
        await update.message.reply_text(
            f"Hello! Welcome to {bot_config['name']}. Use /sendfile to get the file."
        )

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        print(f"[{bot_config['name']}] /help accessed by Chat ID: {chat_id}")
        await update.message.reply_text(
            """Available Commands:
            /sendfile - Send the predefined file
            /help - Show this help message"""
        )

    async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        print(f"[{bot_config['name']}] Unknown command from Chat ID: {chat_id}")
        await update.message.reply_text(f"❌ Sorry '{update.message.text}' is not a valid command.")

    async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        print(f"[{bot_config['name']}] Unknown text from Chat ID: {chat_id}")
        await update.message.reply_text(f"❌ Sorry I can't recognize you, you said '{update.message.text}'.")

    # Build the bot app
    app = ApplicationBuilder().token(bot_config["token"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("sendfile", sendfile))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))
    return app

# ----------------- Run Bot in Thread -----------------
def run_bot(bot_config):
    app = create_bot_app(bot_config)
    print(f"✅ {bot_config['name']} is running...")
    app.run_polling()

# ----------------- Main -----------------
if __name__ == "__main__":
    threads = []
    for bot in bots:
        t = threading.Thread(target=run_bot, args=(bot,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
