import tkinter as tk
from tkinter import scrolledtext
from tkinter import font as tkfont

from TextRank import TextRank
from RAKE import RAKE


def process_text_textrank():
    input_text = text_area.get("1.0", tk.END).strip()
    keyphrases = TextRank(input_text)
    result_text_1.set(", ".join(keyphrases))


def process_text_rake():
    input_text = text_area.get("1.0", tk.END).strip()
    keyphrases = RAKE(input_text)
    result_text_2.set(", ".join(keyphrases))


def on_enter(e):
    e.widget['background'] = '#b3e6ff'
    e.widget['foreground'] = '#000000'


def on_leave(e):
    e.widget['background'] = '#ffffff'
    e.widget['foreground'] = '#143d59'


app = tk.Tk()
app.title("Keyphrase Extractor")
app.geometry("700x600")
app.configure(bg="#d9e7f5")

casual_font = tkfont.Font(family="Comic Sans MS", size=12)

label = tk.Label(app, text="Keyphrase Extraction", fg="#143d59", bg="#d9e7f5", font=("Comic Sans MS", 20))
label.pack(pady=10)


label = tk.Label(app, text="Enter your text below:", fg="#143d59", bg="#d9e7f5", font=("Comic Sans MS", 14))
label.pack(pady=10)


main_frame = tk.Frame(app, bg="#d9e7f5")
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=40, height=10, font=("Comic Sans MS", 12))
text_area.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)


button_frame = tk.Frame(app, bg="#d9e7f5")
button_frame.pack(pady=10)

extract_button_1 = tk.Button(button_frame, text="TextRank", command=process_text_textrank, bg="white", fg="#143d59", font=("Comic Sans MS", 12), relief="flat", padx=10, pady=5)
extract_button_1.pack(side=tk.LEFT, padx=5)
extract_button_1.bind("<Enter>", on_enter)
extract_button_1.bind("<Leave>", on_leave)

extract_button_2 = tk.Button(button_frame, text="RAKE", command=process_text_rake, bg="white", fg="#143d59", font=("Comic Sans MS", 12), relief="flat", padx=10, pady=5)
extract_button_2.pack(side=tk.LEFT, padx=5)
extract_button_2.bind("<Enter>", on_enter)
extract_button_2.bind("<Leave>", on_leave)


result_frame_1 = tk.Frame(app, bg="#d9e7f5")
result_frame_1.pack(pady=10, fill=tk.BOTH, expand=True)

result_text_1 = tk.StringVar()
result_label_1 = tk.Label(result_frame_1, textvariable=result_text_1, wraplength=600, justify="left", bg="#d9e7f5", fg="#143d59", font=("Comic Sans MS", 12))
result_label_1.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

result_frame_2 = tk.Frame(app, bg="#d9e7f5")
result_frame_2.pack(pady=10, fill=tk.BOTH, expand=True)

result_text_2 = tk.StringVar()
result_label_2 = tk.Label(result_frame_2, textvariable=result_text_2, wraplength=600, justify="left", bg="#d9e7f5", fg="#143d59", font=("Comic Sans MS", 12))
result_label_2.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)


app.resizable(True, True)


app.mainloop()
