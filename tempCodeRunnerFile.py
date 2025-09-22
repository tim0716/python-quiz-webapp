import tkinter as tk
from tkinter import messagebox
import random

# --------------------------- User Data & Score ---------------------------
users = {}
leaderboard = []

# --------------------------- Quiz Questions -----------------------------
questions = {
    "Easy": [
        {"question": "What is the output of print(2 + 3)?", "options": ["23", "5", "2+3", "None"], "answer": "5"},
        {"question": "What symbol is used to comment a line in Python?", "options": ["#", "//", "--", "/*"], "answer": "#"},
        {"question": "Which function is used to get input from the user?", "options": ["get()", "input()", "read()", "scan()"], "answer": "input()"},
        {"question": "Which data type is used for True or False?", "options": ["int", "str", "bool", "float"], "answer": "bool"},
        {"question": "What is the correct file extension for Python files?", "options": [".pyth", ".pt", ".py", ".p"], "answer": ".py"},
    ],
    "Medium": [
        {"question": "What does len('Python') return?", "options": ["5", "6", "7", "Error"], "answer": "6"},
        {"question": "What is a correct way to define a function?", "options": ["def myFunc():", "function myFunc()", "func myFunc()", "define myFunc()"], "answer": "def myFunc():"},
        {"question": "Which of these is a tuple?", "options": ["[1,2,3]", "{1,2,3}", "(1,2,3)", "<1,2,3>"], "answer": "(1,2,3)"},
        {"question": "What is the output of 3 * 'Hi '?", "options": ["Hi Hi Hi ", "HiHiHi", "Error", "3Hi"], "answer": "Hi Hi Hi "},
        {"question": "Which keyword is used for loops in Python?", "options": ["loop", "iterate", "for", "repeat"], "answer": "for"},
    ],
    "Hard": [
        {"question": "What does the 'map' function do?", "options": ["Maps values to keys", "Transforms items in an iterable", "Creates a graph", "None"], "answer": "Transforms items in an iterable"},
        {"question": "Which module is used for regular expressions?", "options": ["re", "regex", "expression", "match"], "answer": "re"},
        {"question": "What is a lambda function?", "options": ["Anonymous function", "Loop function", "Named function", "Error"], "answer": "Anonymous function"},
        {"question": "How do you handle exceptions in Python?", "options": ["try/except", "catch/throw", "handle/catch", "error/try"], "answer": "try/except"},
        {"question": "What is the result of bool([])?", "options": ["True", "False", "None", "Error"], "answer": "False"},
    ]
}

# --------------------------- GUI Application -----------------------------
class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Quiz App")
        self.username = ""
        self.score = 0
        self.time_left = 20
        self.q_index = 0
        self.current_level = "Easy"
        self.selected_answers = []

        self.login_page()

    def login_page(self):
        self.clear_window()
        tk.Label(self.master, text="Login", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.master, text="Username").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)
        tk.Button(self.master, text="Start Quiz", command=self.start_quiz).pack(pady=10)

    def start_quiz(self):
        self.username = self.username_entry.get()
        if not self.username:
            messagebox.showwarning("Input Error", "Please enter a username.")
            return
        self.level_selection()

    def level_selection(self):
        self.clear_window()
        tk.Label(self.master, text="Select Difficulty", font=("Arial", 16)).pack(pady=10)
        for level in ["Easy", "Medium", "Hard"]:
            tk.Button(self.master, text=level, width=15, command=lambda l=level: self.begin_quiz(l)).pack(pady=5)

    def begin_quiz(self, level):
        self.current_level = level
        self.questions = questions[level]
        self.q_index = 0
        self.score = 0
        self.selected_answers = []
        self.display_question()

    def display_question(self):
        self.clear_window()
        self.time_left = 20

        if self.q_index >= len(self.questions):
            self.show_result()
            return

        question_data = self.questions[self.q_index]

        self.timer_label = tk.Label(self.master, text=f"Time Left: {self.time_left}s", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=5)
        self.update_timer()

        tk.Label(self.master, text=question_data["question"], wraplength=400, font=("Arial", 14)).pack(pady=10)

        self.var = tk.StringVar()
        for option in question_data["options"]:
            rb = tk.Radiobutton(self.master, text=option, variable=self.var, value=option, font=("Arial", 12))
            rb.pack(anchor='w')

        tk.Button(self.master, text="Next", command=self.next_question).pack(pady=10)

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"{self.time_left} seconds remaining")
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.next_question()

    def next_question(self):
        selected = self.var.get()
        if selected:
            self.selected_answers.append(selected)
            if selected == self.questions[self.q_index]['answer']:
                self.score += 1
        else:
            self.selected_answers.append("Not Answered")

        self.q_index += 1
        self.display_question()

    def show_result(self):
        leaderboard.append((self.username, self.score))
        leaderboard.sort(key=lambda x: x[1], reverse=True)

        self.clear_window()
        tk.Label(self.master, text=f"Quiz Completed!", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.master, text=f"Your Score: {self.score}/{len(self.questions)}", font=("Arial", 14)).pack(pady=5)

        for i, q in enumerate(self.questions):
            correct = q['answer']
            user_ans = self.selected_answers[i]
            result = "✅ Correct" if user_ans == correct else f"❌ Wrong (Correct: {correct})"
            tk.Label(self.master, text=f"Q{i+1}: {result}", font=("Arial", 12)).pack(anchor='w', padx=10)

        tk.Button(self.master, text="Leaderboard", command=self.show_leaderboard).pack(pady=10)

    def show_leaderboard(self):
        self.clear_window()
        tk.Label(self.master, text="Leaderboard", font=("Arial", 16)).pack(pady=10)
        for idx, entry in enumerate(leaderboard[:5]):
            tk.Label(self.master, text=f"{idx+1}. {entry[0]} - {entry[1]}").pack()
        tk.Button(self.master, text="Restart", command=self.login_page).pack(pady=20)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# --------------------------- Main Program -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = QuizApp(root)
    root.mainloop()
