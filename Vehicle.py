import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Vehicle OSINT Bot! Please enter the vehicle registration number to start the search.")

def search_vehicle(update, context):
    reg_number = update.message.text.upper()
    
    # Call the vehicle OSINT API
    response = requests.get(f"https://api.vehicle-osint.com/nl/?q={reg_number}")
    
    if response.status_code == 200:
        data = response.json()
        
        if data['found']:
            result = f"Registration Number: {data['registration_number']}\nMake: {data['make']}\nModel: {data['model']}\nYear: {data['year']}"
        else:
            result = "Vehicle information not found."
    else:
        result = "An error occurred while searching for vehicle information."
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search_vehicle))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
