import google.generativeai as ai
from deep_translator import GoogleTranslator
import re
import tkinter as tk
from tkinter import scrolledtext

API_KEY = "AIzaSyBTzZn-w8iFm72BrK9vGm7pH1Ix_DjGwIM"
ai.configure(api_key=API_KEY)

model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

translator = GoogleTranslator(source="en", target="ar")

def contains_arabic(text):
    return bool(re.search("[\u0600-\u06FF]", text))

def send_message(event=None):
    user_message = entry.get()
    if not user_message.strip():
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_message}\n", "user")
    chat_display.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

    if user_message.lower() == "bye" or user_message == "وداعًا":
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Chatbot: Goodbye! / وداعًا!\n", "bot")
        chat_display.config(state=tk.DISABLED)
        return

    response = chat.send_message(user_message)
    chatbot_response = response.text

    chat_display.config(state=tk.NORMAL)
    if contains_arabic(chatbot_response):
        chat_display.insert(tk.END, f"Chatbot (Arabic): {chatbot_response}\n", "arabic")
    else:
        arabic_translation = translator.translate(chatbot_response)
        chat_display.insert(tk.END, f"Chatbot (English): {chatbot_response}\n", "bot")
        chat_display.insert(tk.END, f"Chatbot (Arabic): {arabic_translation}\n", "arabic")
    
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

root = tk.Tk()
root.title("Bilingual Chatbot")
root.geometry("600x700")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=65, height=25, font=("Arial", 16))
chat_display.pack(pady=10, padx=10)
chat_display.config(state=tk.DISABLED)

chat_display.tag_config("user", foreground="blue", font=("Arial", 18, "bold"))
chat_display.tag_config("bot", foreground="green", font=("Arial", 18))
chat_display.tag_config("arabic", foreground="red", font=("Arial", 22))

entry = tk.Entry(root, width=55, font=("Arial", 18))
entry.pack(pady=5)
entry.bind("<Return>", send_message)

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 16))
send_button.pack(pady=5)

root.mainloop()
