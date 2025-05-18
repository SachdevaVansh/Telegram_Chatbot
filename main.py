from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize reference memory
class Reference:
    def __init__(self) -> None:
        self.reference = ""

reference = Reference()
model_name = "gpt-3.5-turbo"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    reference.reference = ""

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    clear_past()
    await message.reply("I have cleared the past conversations and context.")

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Hi\nI am a bot powered by aiogram and ChatGPT.\nHow may I assist you?")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    help_command = """
    Hi there, I am a Bot 🤖
    /start - to start the conversation
    /clear - to clear past conversations and context 
    /help - to get this help menu 
    I hope this helps you! :)
    """
    await message.reply(help_command)

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    print(f">>> USER:\n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {'role': "assistant", "content": reference.reference},
            {'role': "user", "content": message.text}
        ]
    )
    reference.reference = response['choices'][0]['message']['content']
    print(f">>> ChatGPT:\n\t{reference.reference}")
    await bot.send_message(chat_id=message.chat.id, text=reference.reference)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)
