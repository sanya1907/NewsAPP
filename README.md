from tkinter import *
from PIL import Image, ImageFilter, ImageTk
import requests
import webbrowser
import os
import json

class NewsApp:
    NEWS_URL = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=8f8a17c749914206ac1a7aa1b26ec115'
    NEWS_FILE = 'news_data.json'

    def __init__(self):
        # Install GUI load
        self.load_gui()
        # Load news either online or offline
        self.load_news()

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('800x600')
        self.root.resizable(0, 0)
        self.root.title('My Shorts')  # Set window title

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def welcome_page(self):
        self.clear()

        # Load background image
        img = Image.open("C:/Users/Sanya Uppal/Desktop/wallpaper.jpg")
        img = img.resize((800, 600), Image.ANTIALIAS)
        background_image = ImageTk.PhotoImage(img)

        # Create a Canvas
        canvas = Canvas(self.root, width=800, height=600)
        canvas.pack(fill="both", expand=True)

        # Display background image
        canvas.create_image(0, 0, image=background_image, anchor="nw")

        # Add welcome label
        welcome_label = Label(canvas, text="Welcome to My Shorts", fg='white', font=('Nunito Sans', 20), bg='black')
        canvas.create_window(400, 150, window=welcome_label)

        # Add start button
        start_button = Button(canvas, text="Start Reading", command=self.load_news_item)
        canvas.create_window(400, 250, window=start_button)

    def load_news(self):
        if self.is_online():
            self.fetch_news_online()
        else:
            self.fetch_news_offline()

    def fetch_news_online(self):
        try:
            response = requests.get(self.NEWS_URL)
            data = response.json()
            articles = data.get('articles', [])
            with open(self.NEWS_FILE, 'w') as file:
                json.dump(articles, file)
            self.display_news(articles)
        except Exception as e:
            print("Error fetching news online:", e)
            self.fetch_news_offline()

    def fetch_news_offline(self):
        if os.path.exists(self.NEWS_FILE):
            with open(self.NEWS_FILE, 'r') as file:
                articles = json.load(file)
                self.display_news(articles)
        else:
            print("No news data available.")

    def display_news(self, articles):
        self.clear()
        for article in articles:
            heading = Label(self.root, text=article['title'], bg='black', fg='white', wraplength=780, justify='center')
            heading.pack(pady=(10, 5), anchor='center')
            details = Label(self.root, text=article['description'], bg='black', fg='white', wraplength=780, justify='center')
            details.pack(pady=(2, 10), anchor='center')
            read_more = Button(self.root, text="Read More", command=lambda url=article['url']: self.open_link(url))
            read_more.pack(pady=(0, 10), anchor='center')

        # Add rating button
        rate_button = Button(self.root, text="Rate this app", command=self.open_rating_page)
        rate_button.pack()

    def open_link(self, url):
        webbrowser.open_new(url)

    def is_online(self):
        try:
            response = requests.get('http://www.google.com', timeout=5)
            return True
        except requests.ConnectionError:
            print("No internet connection available.")
            return False

    def open_rating_page(self):
        rating_window = Toplevel(self.root)
        rating_window.geometry('300x200')
        rating_window.title('Rate this app')

        label = Label(rating_window, text="How would you rate this app?")
        label.pack(pady=10)

        rating_scale = Scale(rating_window, from_=1, to=5, orient=HORIZONTAL)
        rating_scale.pack(pady=10)

        submit_button = Button(rating_window, text="Submit", command=lambda: print("User Rating:", rating_scale.get()))
        submit_button.pack(pady=10)

    def load_news_item(self):
        self.clear()
        self.display_news_page()

    def display_news_page(self):
        self.load_news()

if __name__ == "__main__":
    obj = NewsApp()
    obj.welcome_page()
    obj.root.mainloop()

