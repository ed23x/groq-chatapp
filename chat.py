import os
import tkinter as tk
from tkinter import scrolledtext
from groq import Groq

# Fetch the API key from environment variables
api_key = "<GROQ-API>"  # Replace <GROQ-API> with the actual api

# Initialize Groq client
client = Groq(api_key=api_key)

# List of available models
models = [
    "gemma-7b-it",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768"
]

# Function to handle sending and receiving messages
def send_message(event=None):  # Accepting event parameter for key binding
    user_message = user_input_text.get("1.0", tk.END).strip()
    if user_message:
        conversation.append({"role": "user", "content": user_message})
        user_input_text.delete("1.0", tk.END)
        update_chat_window(f"You: {user_message}")

        # Get selected model
        selected_model = model_var.get()

        # Get AI response
        chat_completion = client.chat.completions.create(
            messages=conversation,
            model=selected_model,
        )
        ai_message = chat_completion.choices[0].message.content
        conversation.append({"role": "assistant", "content": ai_message})
        update_chat_window(f"{selected_model}: {ai_message}")

# Function to update chat window
def update_chat_window(message):
    chat_window.configure(state='normal')
    chat_window.insert(tk.END, f"{message}\n")
    chat_window.configure(state='disabled')
    chat_window.yview(tk.END)

# Setting up the UI
root = tk.Tk()
root.title("Groq API Chat Interface")
root.configure(bg='#555555')

# Conversation history
conversation = []

# Chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, bg='#444444', fg='#ffffff', state='disabled')
chat_window.grid(column=0, row=0, columnspan=2, padx=10, pady=10)

# Model selection dropdown
model_var = tk.StringVar(root)
model_var.set(models[0])  # Set default model
model_menu = tk.OptionMenu(root, model_var, *models)
model_menu.config(bg='#444444', fg='#ffffff')
model_menu.grid(column=0, row=1, padx=10, pady=10)

# User input area
user_input_text = tk.Text(root, wrap=tk.WORD, width=50, height=3, bg='#444444', fg='#ffffff')
user_input_text.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
user_input_text.bind("<Return>", send_message)  # Bind ENTER key to send_message

# Send button
send_button = tk.Button(root, text="Send", command=send_message, bg='#444444', fg='#ffffff')
send_button.grid(column=1, row=1, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
