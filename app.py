import tkinter as tk
from tkinter import Tk, messagebox
from PIL import Image, ImageTk
import threading
import time

# Main Menu
def main_menu():
    """Create the main menu for the game."""
    def start_game():
        """Start the quiz game."""
        menu_window.destroy()  # Close the menu window
        quiz_game()  # Start the quiz game

    def show_instructions():
        """Show instructions for the game."""
        messagebox.showinfo(
            "Instructions",
            "Welcome to the Cybersecurity Quiz!\n\n"
            "1. Each question has 4 options.\n"
            "2. You earn points based on how quickly you answer.\n"
            "3. Max score per question is 1000 points.\n"
            "4. Be quick but careful!\n\nGood luck!",
        )

    def exit_game():
        """Exit the game."""
        menu_window.destroy()

    # Create the main menu window
    menu_window = tk.Tk()
    menu_window.iconbitmap("technion-logo.png")  # Set the application icon
    menu_window.configure(bg="white")
    menu_window.title("Cybersecurity Quiz - Menu")
    menu_window.attributes("-fullscreen", True)  # Make fullscreen

    # Get screen dimensions
    screen_width = menu_window.winfo_screenwidth()
    screen_height = menu_window.winfo_screenheight()

    # Load background image using Pillow
    bg_image = Image.open("encrypt.jpg")
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Add background image to the window using Canvas
    canvas = tk.Canvas(menu_window, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Load and place technion logo as .png in the top-right corner (transparent background)
    technion_logo = Image.open("technion-logo.png").convert("RGBA")  # Use PNG with transparent background
    technion_logo = technion_logo.resize((64, 64), Image.Resampling.LANCZOS)  # Resize for proper display
    technion_logo_photo = ImageTk.PhotoImage(technion_logo)

    canvas.create_image(screen_width - 80, 20, image=technion_logo_photo, anchor="nw")

    # Title
    title_label = tk.Label(
        menu_window, text="Cybersecurity Quiz", font=("Arial", 32, "bold"), bg="black", fg="black"
    )
    title_label.pack(pady=50)

    # Start Game Button
    start_button = tk.Button(
        menu_window,
        text="Start Game",
        font=("Arial", 20),
        bg="#28a745",
        fg="white",
        width=20,
        command=start_game,
    )
    start_button.place(x=160, y=screen_height - 400)  # Position near the bottom-left corner

    # Instructions Button
    instructions_button = tk.Button(
        menu_window,
        text="Instructions",
        font=("Arial", 20),
        bg="#007bff",
        fg="white",
        width=20,
        command=show_instructions,
    )
    instructions_button.place(x=160, y=screen_height - 310)  # Position below Start Game button

    # Exit Button
    exit_button = tk.Button(
        menu_window,
        text="Exit",
        font=("Arial", 20),
        bg="#dc3545",
        fg="white",
        width=20,
        command=exit_game,
    )
    exit_button.place(x=160, y=screen_height - 230)  # Position below Instructions button

    # Keep references to avoid garbage collection
    canvas.image = bg_photo
    technion_logo_photo = technion_logo_photo  # Keep a reference to the image

    menu_window.mainloop()

# Quiz Game
def quiz_game():
    """Start the quiz game."""
    global current_question, score, max_score_per_question, questions
    current_question = 0
    score = 0
    max_score_per_question = 1000

    questions = [
        {
            "question": "What is the most common form of cyber attack?",
            "options": ["Phishing", "DDoS Attack", "Ransomware", "SQL Injection"],
            "correct": 0,
        },
        {
            "question": "Which protocol is used to encrypt web traffic?",
            "options": ["HTTP", "SSL/TLS", "FTP", "SMTP"],
            "correct": 1,
        },
        {
            "question": "What is the primary goal of a firewall?",
            "options": ["Prevent virus attacks", "Control network traffic", "Encrypt data", "Monitor CPU usage"],
            "correct": 1,
        },
    ]

    def start_timer(seconds):
        global timer_running, time_left
        timer_running = True
        time_left = seconds
        for i in range(seconds, -1, -1):
            if not timer_running:
                break
            time_left = i
            timer_canvas.delete("timer")
            timer_canvas.create_oval(20, 20, 180, 180, outline="white", width=5)
            timer_canvas.create_text(100, 100, text=str(i), font=("Arial", 32), fill="white", tags="timer")
            time.sleep(1)

        if timer_running:
            timer_running = False
            check_answer(-1)

    def start_timer_thread(seconds=20):
        threading.Thread(target=start_timer, args=(seconds,), daemon=True).start()

    def display_question():
        global selected_option, timer_running, points_earned

        selected_option = -1
        question_label.config(text=questions[current_question]["question"])

        for i, option in enumerate(questions[current_question]["options"]):
            option_buttons[i].config(text=option, state="normal", bg=option_colors[i])

        feedback_label.config(text="")
        next_button.config(state="disabled")
        points_earned = max_score_per_question

        timer_running = False
        start_timer_thread(20)

    def select_option(idx):
        global selected_option

        selected_option = idx

        for i, button in enumerate(option_buttons):
            if i == idx:
                button.config(bg="#28a745")
            else:
                button.config(bg=option_colors[i])

        next_button.config(state="normal")

    def check_answer(selected_idx):
        global current_question, score, points_earned, timer_running

        timer_running = False
        correct_option = questions[current_question]["correct"]

        if selected_idx == correct_option:
            points_earned = int(max_score_per_question * (time_left / 20))
            score += points_earned
            feedback_label.config(text=f"✅ Correct! You earned {points_earned} points.", fg="green")
        elif selected_idx == -1:
            points_earned = 0
            feedback_label.config(text="⏰ Time's up! No answer selected.", fg="red")
        else:
            points_earned = 0
            feedback_label.config(
                text=f"❌ Incorrect! Correct: {questions[current_question]['options'][correct_option]}.",
                fg="red",
            )

        for btn in option_buttons:
            btn.config(state="disabled")

        current_question += 1
        if current_question < len(questions):
            window.after(1500, display_question)
        else:
            window.after(1500, show_score)

    def show_score():
        messagebox.showinfo("Quiz Completed", f"Your final score is: {score}/{len(questions) * max_score_per_question}")
        window.destroy()

    window = tk.Tk()
    window.title("Cybersecurity Quiz")
    window.geometry("800x600")
    window.configure(bg="black")

    question_label = tk.Label(window, text="", font=("Arial", 18), bg="black", fg="white", wraplength=700, justify="center")
    question_label.pack(pady=20)

    timer_canvas = tk.Canvas(window, width=200, height=200, bg="black", highlightthickness=0)
    timer_canvas.pack()

    options_frame = tk.Frame(window, bg="black")
    options_frame.pack(pady=50)

    option_colors = ["#003366", "#8B0000", "#006400", "#FFD700"]
    option_buttons = []
    for i in range(4):
        btn = tk.Button(
            options_frame,
            text="",
            font=("Arial", 16),
            bg=option_colors[i],
            fg="white",
            width=40,
            height=2,
            relief="solid",
            command=lambda idx=i: select_option(idx),
        )
        row = i // 2
        col = i % 2
        btn.grid(row=row, column=col, padx=20, pady=10)
        option_buttons.append(btn)

    feedback_label = tk.Label(window, text="", font=("Arial", 14), bg="black", fg="lime")
    feedback_label.pack(pady=10)

    next_button = tk.Button(
        window,
        text="Next",
        font=("Arial", 14),
        bg="gray",
        fg="white",
        width=20,
        state="disabled",
        command=lambda: check_answer(selected_option),
    )
    next_button.pack(pady=20)

    display_question()
    window.mainloop()

if __name__ == "__main__":
    main_menu()
