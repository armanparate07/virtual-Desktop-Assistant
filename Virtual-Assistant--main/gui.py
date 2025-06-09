from tkinter import *
from PIL import Image, ImageTk
import action
import spech_to_text  # Assuming this is the intended module name
import threading
import queue

# Initialize message queue for thread-safe GUI updates
message_queue = queue.Queue()

def append_to_text(message):
    """Put message in the queue for GUI update."""
    message_queue.put(message)

def update_text_area():
    """Update text area with messages from the queue."""
    while not message_queue.empty():
        message = message_queue.get()
        convo_text.config(state=NORMAL)
        convo_text.insert(END, message + "\n")
        convo_text.config(state=DISABLED)
        convo_text.see(END)
    root.after(100, update_text_area)

def user_send():
    """Handle text input from entry widget."""
    send = entry.get().strip()
    if not send:
        return
    append_to_text("Me --> " + send)
    entry.delete(0, END)
    threading.Thread(target=process_query, args=(send,)).start()

def process_query(query):
    """Process query in a separate thread."""
    try:
        bot = action.Action(query)
        if bot:
            append_to_text("Bot <-- " + str(bot))
            if bot.lower() == "ok sir":
                root.after(0, root.destroy)
    except Exception as e:
        append_to_text(f"Bot <-- Error: {str(e)}")

def ask():
    """Handle voice input in a separate thread."""
    append_to_text("Listening for voice input...")
    threading.Thread(target=process_speech).start()

def process_speech():
    """Process speech input in a separate thread."""
    try:
        ask_val = spech_to_text.spech_to_text()  # Assuming this function exists
        if ask_val:
            append_to_text("Me --> " + ask_val)
            bot_val = action.Action(ask_val)
            if bot_val:
                append_to_text("Bot <-- " + str(bot_val))
                if bot_val.lower() == "ok sir":
                    root.after(0, root.destroy)
        else:
            append_to_text("Bot <-- No voice input detected.")
    except Exception as e:
        append_to_text(f"Bot <-- Error in speech recognition: {str(e)}")

def delete_text():
    """Clear the conversation text widget."""
    convo_text.config(state=NORMAL)
    convo_text.delete("1.0", END)
    convo_text.config(state=DISABLED)

# Create main window
root = Tk()
root.geometry("550x700")  # Slightly increased height to accommodate all elements
root.title("AI Assistant")
root.resizable(False, False)
root.config(bg="#1A3C34")  # Dark teal background to mimic gradient

# Load robot image for avatar and display
robot_img = Image.open(r"C:\Users\nitin\Downloads\Virtual-Assistant--main\image\robot.png")
robot_img_small = robot_img.resize((40, 40), Image.LANCZOS)
robot_img_tiny = robot_img.resize((30, 30), Image.LANCZOS)
robot_photo_small = ImageTk.PhotoImage(robot_img_small)
robot_photo_tiny = ImageTk.PhotoImage(robot_img_tiny)



# Header Frame (for title and avatar)
header_frame = Frame(root, bg="#2E5A50", height=60)  # Slightly lighter teal for header
header_frame.pack(fill=X, side=TOP, padx=10, pady=(0, 10))
header_frame.pack_propagate(False)

# Header Content (Avatar and Title)
avatar_label = Label(header_frame, image=robot_photo_small, bg="#2E5A50")
avatar_label.pack(side=LEFT, padx=10)
title_label = Label(header_frame, text="ChatGPT", font=("Helvetica", 16, "bold"), bg="#2E5A50", fg="#A3E4D7")
title_label.pack(side=LEFT, pady=15)

# Main Frame to hold conversation and input areas
main_frame = Frame(root, bg="#1A3C34")
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))

# Conversation Frame (for text display)
convo_frame = Frame(main_frame, bg="#2E5A50", bd=2, relief="flat")
convo_frame.pack(fill=BOTH, expand=True)  # Expand to fill available space

# Conversation Text Widget with Scrollbar
convo_text = Text(convo_frame, font=("Arial", 12), bg="#344A44", fg="white", state=DISABLED, wrap=WORD, bd=0, padx=10, pady=10)
convo_text.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar = Scrollbar(convo_frame, command=convo_text.yview, bg="#2E5A50", troughcolor="#1A3C34")
scrollbar.pack(side=RIGHT, fill=Y)
convo_text.config(yscrollcommand=scrollbar.set)

# Input Frame (for entry and buttons)
input_frame = Frame(root, bg="#1A3C34")
input_frame.pack(fill=X, padx=20, pady=(0, 10), side=BOTTOM)

# Entry Widget with Avatar
entry_subframe = Frame(input_frame, bg="#344A44", bd=2, relief="groove")
entry_subframe.pack(fill=X, pady=(0, 5))
avatar_entry_label = Label(entry_subframe, image=robot_photo_tiny, bg="#344A44")
avatar_entry_label.pack(side=LEFT, padx=5, pady=5)
entry = Entry(entry_subframe, font=("Arial", 14), bg="#4A5A54", fg="white", bd=1, insertbackground="white", relief="flat")
entry.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
entry.bind("<Return>", lambda event: user_send())  # Bind Enter key to send

# Buttons Frame
buttons_frame = Frame(input_frame, bg="#1A3C34")
buttons_frame.pack(fill=X, pady=5)

# Buttons with Text Labels
ask_button = Button(buttons_frame, text="Ask", font=("Arial", 12), bg="#2E5A50", fg="white", activebackground="#A3E4D7", bd=0, command=ask)
ask_button.pack(side=RIGHT, padx=5)
send_button = Button(buttons_frame, text="Send", font=("Arial", 12), bg="#2E5A50", fg="white", activebackground="#A3E4D7", bd=0, command=user_send)
send_button.pack(side=RIGHT, padx=5)
clear_button = Button(buttons_frame, text="Clear", font=("Arial", 12), bg="#2E5A50", fg="white", activebackground="#A3E4D7", bd=0, command=delete_text)
clear_button.pack(side=RIGHT, padx=5)

# Start updating the text area
root.after(100, update_text_area)

root.mainloop()