
import random
import tkinter as tk

board = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]

current_player = "X"
score_x = 0
score_o = 0
ai_mode = None  

buttons = []
window = tk.Tk()
window.title("Tic Tac Toe")
window.configure(bg="white")

def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != "":
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] != "":
            return b[0][i]
    if b[0][0] == b[1][1] == b[2][2] != "":
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != "":
        return b[0][2]
    for row in b:
        if "" in row:
            return None
    return "draw"


def random_ai():
    empty_cells = [(r,c) for r in range(3) for c in range(3) if board[r][c] == ""]
    return random.choice(empty_cells)

def easy_ai():
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                return (r, c)

def minimax(board_state, player):
    result = check_winner(board_state)
    if result == "X":
        return -1
    if result == "O":
        return 1
    if result == "draw":
        return 0
    if player == "O":
        best_score = -100
        for r in range(3):
            for c in range(3):
                if board_state[r][c] == "":
                    board_state[r][c] = "O"
                    score = minimax(board_state, "X")
                    board_state[r][c] = ""
                    if score > best_score:
                        best_score = score
        return best_score
    else:
        best_score = 100
        for r in range(3):
            for c in range(3):
                if board_state[r][c] == "":
                    board_state[r][c] = "X"
                    score = minimax(board_state, "O")
                    board_state[r][c] = ""
                    if score < best_score:
                        best_score = score
        return best_score

def hard_ai():
    best_score = -100
    best_move = (0,0)
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = "O"
                score = minimax(board, "X")
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move

def ai_move():
    if ai_mode == "random":
        r, c = random_ai()
    elif ai_mode == "easy":
        r, c = easy_ai()
    else:
        r, c = hard_ai()
    place_mark(r, c)

def place_mark(r, c):
    global current_player, score_x, score_o

    if board[r][c] != "":
        return

    board[r][c] = current_player
    buttons[r][c].config(text=current_player)

    result = check_winner(board)
    if result:
        if result == "X":
            score_x += 1
            status_label.config(text="You win!")
        elif result == "O":
            score_o += 1
            status_label.config(text="AI wins!")
        else:
            status_label.config(text="Draw!")

        score_label.config(text=f"Score — X: {score_x}   O: {score_o}")
        window.after(1200, reset_board)
        return

    current_player = "O" if current_player == "X" else "X"

    if current_player == "O":
        status_label.config(text="AI thinking...")
        window.after(300, ai_move)
    else:
        status_label.config(text="Your turn (X)")

def cell_clicked(r, c):
    if current_player == "X":
        place_mark(r, c)

def reset_board():
    global board, current_player
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = "X"
    status_label.config(text="Your turn (X)")
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", bg="light gray")

def on_enter(event):
    event.widget.config(bg="gray")

def on_leave(event):
    event.widget.config(bg="light gray")

status_label = tk.Label(window, text="Your turn (X)", font=("Arial", 16), bg="white")
status_label.grid(row=0, column=0, columnspan=3, pady=8)

score_label = tk.Label(window, text="Score — X: 0   O: 0", font=("Arial", 14), bg="white")
score_label.grid(row=1, column=0, columnspan=3, pady=8)

for r in range(3):
    row = []
    for c in range(3):
        btn = tk.Button(window, text="", font=("Arial", 32), width=4, height=2, bg="light gray",
                        command=lambda r=r, c=c: cell_clicked(r, c))
        btn.grid(row=r+2, column=c, padx=5, pady=5)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        row.append(btn)
    buttons.append(row)

def choose_mode(selected_mode):
    global ai_mode
    ai_mode = selected_mode
    mode_window.destroy()

mode_window = tk.Toplevel(window)
mode_window.title("Select AI Difficulty")
mode_window.geometry("260x130")
mode_window.resizable(False, False)

label = tk.Label(mode_window, text="Choose AI difficulty:", font=("Arial", 14))
label.pack(pady=10)

btn_easy = tk.Button(mode_window, text="Easy", width=15, command=lambda: choose_mode("easy"))
btn_easy.pack(pady=3)

btn_hard = tk.Button(mode_window, text="Hard", width=15, command=lambda: choose_mode("hard"))
btn_hard.pack(pady=3)

btn_random = tk.Button(mode_window, text="Random", width=15, command=lambda: choose_mode("random"))
btn_random.pack(pady=3)

mode_window.transient(window)
mode_window.grab_set()
window.wait_window(mode_window)

window.mainloop()