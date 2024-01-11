import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def save_file(main_window, text_editor):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if not file_path:
        return
    
    with open(file_path, "w") as file:
        content = text_editor.get(1.0, tk.END)
        file.write(content)
    main_window.title(f"Notes - {file_path}")

def open_file(main_window, text_editor):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    if not file_path:
        return
    
    text_editor.delete(1.0, tk.END)
    with open(file_path, "r") as file:
        content = file.read()
        text_editor.insert(tk.END, content)
    main_window.title(f"Notes - {file_path}")

def find_text(main_window, text_editor):
    if not text_editor.tag_ranges(tk.SEL):
        target = simpledialog.askstring("Find", "Enter text to find:")
        if target:
            start_pos = text_editor.search(target, 1.0, tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(target)}c"
                text_editor.tag_remove(tk.SEL, 1.0, tk.END)
                text_editor.tag_add(tk.SEL, start_pos, end_pos)
                text_editor.mark_set(tk.INSERT, end_pos)
                text_editor.see(tk.INSERT)
            else:
                messagebox.showinfo("Not Found", f"The word '{target}' was not found.")

def undo_text(text_editor):
    try:
        text_editor.edit_undo()
    except tk.TclError:
        pass  # Ignore undo errors

def update_status_bar(event, status_bar, text_editor):
    line, column = text_editor.index(tk.INSERT).split('.')
    selected_text = text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
    char_count = len(selected_text)

    status_text = f"Line: {line}, Column: {column} | Selected Characters: {char_count}"

    status_bar.config(text=status_text)

def main():
    global text_editor, main_window

    main_window = tk.Tk()
    main_window.title("Notes")
    main_window.geometry("800x600")

    menubar = tk.Menu(main_window)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open", command=lambda: open_file(main_window, text_editor), accelerator="Ctrl+O")
    file_menu.add_command(label="Save", command=lambda: save_file(main_window, text_editor), accelerator="Ctrl+S")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=main_window.destroy)
    menubar.add_cascade(label="File", menu=file_menu)

    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Find", command=lambda: find_text(main_window, text_editor))
    edit_menu.add_separator()
    edit_menu.add_command(label="Undo", command=lambda: undo_text(text_editor))
    menubar.add_cascade(label="Edit", menu=edit_menu)

    main_window.config(menu=menubar)

    text_editor = tk.Text(main_window, font=("Helvetica", 12), wrap="word", padx=10, pady=10, selectbackground="lightblue", undo=True)
    text_editor.pack(expand=True, fill="both")

    status_bar = tk.Label(main_window, text="Line: 1, Column: 0 | Selected Characters: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    main_window.bind("<Control-o>", lambda x: open_file(main_window, text_editor))
    main_window.bind("<Control-s>", lambda x: save_file(main_window, text_editor))
    text_editor.bind("<ButtonRelease>", lambda x: update_status_bar(x, status_bar, text_editor))
    text_editor.bind("<KeyRelease>", lambda x: update_status_bar(x, status_bar, text_editor))

    main_window.mainloop()

main()