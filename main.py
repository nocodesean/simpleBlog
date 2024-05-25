import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import sqlite3

# Database setup
conn = sqlite3.connect('blog.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
conn.commit()

# GUI setup
root = tk.Tk()
root.title("Personal Blog Platform")

def refresh_posts():
    for widget in posts_frame.winfo_children():
        widget.destroy()
    c.execute("SELECT id, title FROM posts")
    for post in c.fetchall():
        post_id, post_title = post
        btn = tk.Button(posts_frame, text=post_title, command=lambda pid=post_id: view_post(pid))
        btn.pack(fill='x')

def view_post(post_id):
    c.execute("SELECT title, content FROM posts WHERE id=?", (post_id,))
    post = c.fetchone()
    title_var.set(post[0])
    content_text.delete('1.0', tk.END)
    content_text.insert('1.0', post[1])
    delete_btn.config(state=tk.NORMAL)
    save_btn.config(state=tk.NORMAL, command=lambda: save_post(post_id))

def create_post():
    title = simpledialog.askstring("Title", "Enter the title of the post:")
    if title:
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, ""))
        conn.commit()
        refresh_posts()

def save_post(post_id):
    title = title_var.get()
    content = content_text.get('1.0', tk.END)
    c.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
    conn.commit()
    refresh_posts()
    messagebox.showinfo("Success", "Post saved successfully")

def delete_post():
    post_id = int(c.execute("SELECT id FROM posts WHERE title=?", (title_var.get(),)).fetchone()[0])
    c.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    title_var.set("")
    content_text.delete('1.0', tk.END)
    delete_btn.config(state=tk.DISABLED)
    save_btn.config(state=tk.DISABLED)
    refresh_posts()
    messagebox.showinfo("Success", "Post deleted successfully")

# GUI Widgets
posts_frame = tk.Frame(root)
posts_frame.pack(side='left', fill='y')

content_frame = tk.Frame(root)
content_frame.pack(side='right', expand=True, fill='both')

title_var = tk.StringVar()
title_entry = tk.Entry(content_frame, textvariable=title_var)
title_entry.pack(fill='x')

content_text = scrolledtext.ScrolledText(content_frame)
content_text.pack(expand=True, fill='both')

create_btn = tk.Button(root, text="Create Post", command=create_post)
create_btn.pack(side='top', fill='x')

delete_btn = tk.Button(root, text="Delete Post", state=tk.DISABLED, command=delete_post)
delete_btn.pack(side='top', fill='x')

save_btn = tk.Button(root, text="Save Post", state=tk.DISABLED)
save_btn.pack(side='top', fill='x')

refresh_posts()
root.mainloop()

conn.close()
