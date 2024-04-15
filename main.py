import discord
from discord.ext import commands
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['discord_bot']
questions_collection = db['questions']

# Initialize the Discord bot
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def ask(ctx, *, question: str):
    # Create a new question document in MongoDB
    question_document = {
        "question": question,
        "answers": []
    }
    result = questions_collection.insert_one(question_document)
    # Send back a confirmation message with the unique question ID
    await ctx.send(f'Question added with ID: {result.inserted_id}')

@bot.command()
async def answer(ctx, question_id: str, *, answer: str):
    # Update the question document with the new answer
    result = questions_collection.update_one(
        {"_id": MongoClient().database.ObjectId(question_id)},
        {"$push": {"answers": answer}}
    )
    if result.modified_count:
        await ctx.send('Answer added successfully!')
    else:
        await ctx.send('Failed to add answer. Please check the question ID.')

@bot.command()
async def view(ctx, question_id: str):
    # Retrieve the question document based on the provided ID
    question_document = questions_collection.find_one({"_id": MongoClient().database.ObjectId(question_id)})
    if question_document:
        answers = question_document['answers']
        if answers:
            answer_list = '\n'.join(answers)
            await ctx.send(f'Answers for "{question_document["question"]}":\n{answer_list}')
        else:
            await ctx.send('No answers yet for this question.')
    else:
        await ctx.send('Question not found. Please check the question ID.')

# Start the bot
bot.run(DISCORD_TOKEN)
