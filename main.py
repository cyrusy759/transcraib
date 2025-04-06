from groq_app.groq_chatbot import GroqChatBot

if __name__ == "__main__":
    bot = GroqChatBot()
    print("Hello welcome to Transcraib!")
    bot.question_user()