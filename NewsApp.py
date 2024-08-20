from tkinter import *
from tkinter import messagebox
import requests
import webbrowser
import os
import json
from PIL import Image, ImageTk

class NewsApp:
    NEWS_URL = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=8f8a17c749914206ac1a7aa1b26ec115'
    NEWS_FILE = 'news_data.json'

    def __init__(self):
        self.load_gui()
        self.load_news()

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('1000x600')
        self.root.state('zoomed')
        self.root.resizable(True, True)
        self.root.title('SwIfT NeWzz')

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def welcome_page(self):
        self.clear()

        welcome_frame = Frame(self.root, bg='black')
        welcome_frame.pack(fill=BOTH, expand=True)

        image_path = 'news_image.jpeg'
        try:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            image_label = Label(welcome_frame, image=photo, bg='black')
            image_label.image = photo
            image_label.pack(pady=10, padx=10)
        except Exception as e:
            print(f"Error loading image: {e}")

        welcome_label = Label(
            welcome_frame,
            text="SwIfT NeWzzz : Crisp and Fast News",
            fg='#FFD700',
            font=('Arial', 24, 'bold'),
            bg='black'
        )
        welcome_label.pack(pady=10, padx=10, anchor=CENTER)

        subheading_label = Label(
            welcome_frame,
            text="Get the latest headlines from various sources with a clean and user-friendly interface. Stay informed with up-to-date news and easy navigation.",
            fg='#FFFFFF',
            font=('Arial', 14),
            bg='black',
            wraplength=800,
            justify=LEFT
        )
        subheading_label.pack(pady=20, padx=10, anchor=CENTER)

        start_button = Button(
            welcome_frame,
            text="Start Reading",
            font=('Arial', 16),
            bg='#4CAF50',
            fg='white',
            relief=RAISED,
            bd=4,
            padx=20,
            pady=10,
            command=self.load_news_item
        )
        start_button.pack(pady=10, padx=10, anchor=CENTER)

        categories_frame = Frame(welcome_frame, bg='black')
        categories_frame.pack(side=LEFT, fill=Y, padx=(10, 0), pady=20)

        categories_label = Label(
            categories_frame,
            text="News Categories",
            fg='#FFD700',
            font=('Arial', 18, 'bold'),
            bg='black'
        )
        categories_label.pack(pady=10)

        categories = ["Top Headlines", "Sports", "Technology", "Entertainment", "Health", "Business"]
        for category in categories:
            category_button = Button(
                categories_frame,
                text=category,
                font=('Arial', 14),
                bg='#2196F3',
                fg='white',
                relief=RAISED,
                bd=2,
                padx=10,
                pady=5,
                command=lambda c=category: self.load_category_news(c)
            )
            category_button.pack(pady=5, padx=10)

        right_space_frame = Frame(welcome_frame, bg='black')
        right_space_frame.pack(side=RIGHT, fill=Y, padx=(0, 10), pady=20)

        testimonial_label = Label(
            right_space_frame,
            text="What Our Users Say",
            fg='#FFD700',
            font=('Arial', 18, 'bold'),
            bg='black'
        )
        testimonial_label.pack(pady=10)

        testimonials = [
            "Great app for quick news updates!",
            "Love the clean interface and ease of use.",
            "A must-have for staying informed!"
        ]

        for testimonial in testimonials:
            testimonial_text = Label(
                right_space_frame,
                text=f"- {testimonial}",
                fg='#FFFFFF',
                font=('Arial', 14),
                bg='black',
                wraplength=200,
                justify=LEFT
            )
            testimonial_text.pack(pady=5, padx=10)

        nav_menu_frame = Frame(right_space_frame, bg='black')
        nav_menu_frame.pack(pady=20)

        nav_menu_label = Label(
            nav_menu_frame,
            text="Explore More",
            fg='#FFD700',
            font=('Arial', 18, 'bold'),
            bg='black'
        )
        nav_menu_label.pack(pady=10)

        nav_menu_buttons = [
            ("About Us", self.open_about_us),
            ("Contact Us", self.open_contact_us),
            ("Privacy Policy", self.open_privacy_policy)
        ]

        for text, command in nav_menu_buttons:
            nav_button = Button(
                nav_menu_frame,
                text=text,
                font=('Arial', 14),
                bg='#2196F3',
                fg='white',
                relief=RAISED,
                bd=2,
                padx=10,
                pady=5,
                command=command
            )
            nav_button.pack(pady=5, padx=10)

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

        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True)

        canvas = Canvas(main_frame, bg='#212121')
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        news_frame = Frame(canvas, bg='#212121')
        canvas.create_window((0, 0), window=news_frame, anchor='nw')

        news_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        title_label = Label(
            news_frame,
            text="Latest News",
            fg='#FFD700',
            font=('Arial', 24, 'bold'),
            bg='#212121'
        )
        title_label.pack(pady=20)

        for index, article in enumerate(articles):
            frame = Frame(news_frame, bg='#424242', bd=2, relief=RAISED)
            frame.pack(pady=(10, 10), padx=10, fill=X)

            heading = Label(frame, text=article['title'], bg='#424242', fg='#FFFFFF', font=('Arial', 16, 'bold'), wraplength=730)
            heading.pack(pady=(10, 5), padx=10)

            details = Label(frame, text=article['description'], bg='#424242', fg='#FFFFFF', font=('Arial', 14), wraplength=730)
            details.pack(pady=(0, 10), padx=10)

            read_more = Button(frame, text="Read More", font=('Arial', 12), bg='#2196F3', fg='white', command=lambda url=article['url']: self.open_link(url))
            read_more.pack(pady=(0, 10), padx=10)

        canvas.configure(yscrollcommand=scrollbar.set)

        message_frame = Frame(main_frame, width=250, bg='#1F1F1F')
        message_frame.pack(side=RIGHT, fill=Y, padx=(10, 0))

        message_label = Label(
            message_frame,
            text="Curious about the trending news?",
            fg='#FFD700',
            font=('Arial', 18, 'italic'),
            bg='#1F1F1F',
            wraplength=230
        )
        message_label.pack(pady=20, padx=10)

        rate_button = Button(
            main_frame,
            text="Rate this app",
            font=('Arial', 14),
            bg='#FFC107',
            fg='black',
            relief=RAISED,
            bd=4,
            command=self.open_rating_page
        )
        rate_button.pack(side=BOTTOM, pady=10)

        back_button = Button(
            main_frame,
            text="Back",
            font=('Arial', 14),
            bg='#FF5722',
            fg='white',
            relief=RAISED,
            bd=4,
            command=self.welcome_page
        )
        back_button.pack(side=TOP, pady=10, anchor=E)

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

        submit_button = Button(rating_window, text="Submit", command=lambda: self.submit_rating(rating_scale.get(), rating_window))
        submit_button.pack(pady=10)

    def submit_rating(self, rating, window):
        messagebox.showinfo("Thank You", f"Thank you for the rating of {rating}!")
        window.destroy()

    def load_news_item(self):
        self.clear()
        self.display_news_page()

    def display_news_page(self):
        self.load_news()

    def load_category_news(self, category):
        print(f"Loading news for category: {category}")
        self.load_news()

    def open_about_us(self):
        messagebox.showinfo("About Us", "This app is owned by Sanya Uppal.\nEmail: sanyauppal712@gmail.com")

    def open_contact_us(self):
        messagebox.showinfo("Contact Us", "Contact information for support and feedback.")

    def open_privacy_policy(self):
        messagebox.showinfo("Privacy Policy", "Details about the app's privacy policy.")

if __name__ == "__main__":
    obj = NewsApp()
    obj.welcome_page()
    obj.root.mainloop()
