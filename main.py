import tkinter as tk
from tkinter import messagebox
import requests
import json

FAVORITES_FILE = "favorites.json"


# Загрузка избранного
def load_favorites():
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


# Сохранение избранного
def save_favorites(data):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Поиск пользователя
def search_user():
    username = entry.get().strip()

    if not username:
        messagebox.showwarning("Ошибка ввода", "Поле поиска не должно быть пустым")
        return

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    listbox.delete(0, tk.END)

    if response.status_code == 200:
        user = response.json()
        listbox.insert(tk.END, f"{user['login']} ({user['html_url']})")
    else:
        listbox.insert(tk.END, "Пользователь не найден")


# Добавление в избранное
def add_to_favorites():
    selection = listbox.get(tk.ACTIVE)

    if not selection:
        messagebox.showwarning("Ошибка", "Выберите пользователя")
        return

    favorites = load_favorites()

    if selection not in favorites:
        favorites.append(selection)
        save_favorites(favorites)
        messagebox.showinfo("OK", "Добавлено в избранное")
    else:
        messagebox.showinfo("OK", "Уже в избранном")

# Удалить из избранного
def remove_favorite():
    selection = listbox.curselection()

    if not selection:
        messagebox.showwarning("Ошибка", "Выберите пользователя")
        return

    item = listbox.get(selection[0])
    favorites = load_favorites()

    if item in favorites:
        favorites.remove(selection)
        save_favorites(favorites)
        show_favorites()
        messagebox.showinfo("OK", "Удалено из избранного")
    else:
        messagebox.showinfo("OK", "Нет в избранном")

# Показ избранного
def show_favorites():
    favorites = load_favorites()

    listbox.delete(0, tk.END)

    for user in favorites:
        listbox.insert(tk.END, user)


# Очистить избранное
def clear_favorites():
    confirm = messagebox.askyesno(
        "Подтверждение",
        "Вы уверены, что хотите очистить избранное?"
    )

    if confirm:
        save_favorites([])
        listbox.delete(0, tk.END)
        messagebox.showinfo("OK", "Избранное очищено")


# GUI
root = tk.Tk()
root.title("Приложение GitHub User Finder")
root.geometry("400x400")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

search_btn = tk.Button(root, text="Поиск", command=search_user)
search_btn.pack()

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

fav_btn = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
fav_btn.pack()

remove_btn = tk.Button(root, text="Удалить из избранного", command=remove_favorite)
remove_btn.pack()

show_btn = tk.Button(root, text="Показать избранное", command=show_favorites)
show_btn.pack()

clear_btn = tk.Button(root, text="Очистить избранное", command=clear_favorites)
clear_btn.pack()

root.mainloop()