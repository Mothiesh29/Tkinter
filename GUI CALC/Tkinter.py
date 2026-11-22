import tkinter as tk

root = tk.Tk()
root.title("Modern Calculator")
root.geometry("360x540")
root.resizable(False, False)
root.configure(bg="#151922")

# Colors
BG = "#151922"
DISPLAY_BG = "#202735"
NUMBER = "#30394A"
OPERATOR = "#394B68"
SPECIAL = "#E09F3E"
TEXT = "#FFFFFF"
ACCENT = "#4CC9F0"

expression = ""

# Display
display = tk.Entry(
    root,
    font=("Arial", 28, "bold"),
    bg=DISPLAY_BG,
    fg=TEXT,
    insertbackground=TEXT,
    justify="right",
    bd=0,
    state="readonly",
    readonlybackground=DISPLAY_BG
)
display.pack(fill="x", padx=20, pady=(35, 20), ipady=22)


def update_display():
    display.config(state="normal")
    display.delete(0, tk.END)
    display.insert(0, expression if expression else "0")
    display.config(state="readonly")


def press(value):
    global expression

    if value == "C":
        expression = ""

    elif value == "⌫":
        expression = expression[:-1]

    elif value == "=":
        try:
            if not expression:
                return

            allowed = set("0123456789+-*/.() ")
            if any(ch not in allowed for ch in expression):
                raise ValueError

            result = eval(expression, {"__builtins__": {}}, {})

            if isinstance(result, float):
                result = round(result, 10)

            expression = str(result)

        except ZeroDivisionError:
            expression = "Cannot divide by zero"
        except Exception:
            expression = "Invalid Input"

    elif value == "%":
        try:
            if expression:
                result = eval(
                    expression,
                    {"__builtins__": {}},
                    {}
                )
                expression = str(result / 100)
        except Exception:
            expression = "Invalid Input"

    else:
        if expression in ("Cannot divide by zero", "Invalid Input"):
            expression = ""

        expression += value

    update_display()


buttons = [
    ["C", "⌫", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["00", "0", ".", "="]
]


frame = tk.Frame(root, bg=BG)
frame.pack(expand=True, fill="both", padx=15, pady=10)

for r, row in enumerate(buttons):
    for c, value in enumerate(row):

        if value == "=":
            color = ACCENT
            fg = "#151922"
        elif value in ("C", "⌫", "%"):
            color = SPECIAL
            fg = "#151922"
        elif value in ("/", "*", "-", "+"):
            color = OPERATOR
            fg = TEXT
        else:
            color = NUMBER
            fg = TEXT

        button = tk.Button(
            frame,
            text=value,
            font=("Arial", 17, "bold"),
            bg=color,
            fg=fg,
            activebackground="#56647A",
            activeforeground=TEXT,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda v=value: press(v)
        )

        button.grid(
            row=r,
            column=c,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=13
        )

# Equal button and all other buttons get equal space
for i in range(5):
    frame.rowconfigure(i, weight=1)

for i in range(4):
    frame.columnconfigure(i, weight=1)


def keyboard_input(event):
    key = event.char

    if key in "0123456789.+-*/()":
        press(key)
    elif event.keysym == "Return":
        press("=")
    elif event.keysym == "BackSpace":
        press("⌫")
    elif event.keysym == "Escape":
        press("C")


root.bind("<Key>", keyboard_input)

update_display()
root.mainloop()