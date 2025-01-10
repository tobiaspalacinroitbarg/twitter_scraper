import customtkinter as ctk
import json
import sys
from datetime import datetime
import threading
from funcs import get_users, filter_and_message
from urllib.parse import quote
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

class SearchEntry(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.query_label = ctk.CTkLabel(self, text="Search Query:")
        self.query_label.grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.query = ctk.CTkEntry(self, width=400, placeholder_text="Enter search query...")
        self.query.grid(row=0, column=1, columnspan=3, padx=5, pady=2, sticky='ew')
        
        self.posts_label = ctk.CTkLabel(self, text="Scroll Posts:")
        self.posts_label.grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.scroll_posts = ctk.CTkEntry(self, width=100, placeholder_text="1")
        self.scroll_posts.grid(row=1, column=1, padx=5, pady=2, sticky='w')
        
        self.comments_label = ctk.CTkLabel(self, text="Scroll Comments:")
        self.comments_label.grid(row=1, column=2, padx=5, pady=2, sticky='w')
        self.scroll_comments = ctk.CTkEntry(self, width=100, placeholder_text="1")
        self.scroll_comments.grid(row=1, column=3, padx=5, pady=2, sticky='w')

        self.delete_btn = ctk.CTkButton(self, text="×", width=40, command=self.remove_search)
        self.delete_btn.grid(row=0, column=4, rowspan=2, padx=5, pady=2)

    def remove_search(self):
        self.destroy()

    def get_data(self):
        return {
            "query": self.query.get(),
            "scroll_posts": int(self.scroll_posts.get() or 1),
            "scroll_comments": int(self.scroll_comments.get() or 1)
        }

class CustomLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.original_stdout = sys.stdout

    def write(self, text):
        self.text_widget.configure(state='normal')
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.text_widget.insert('end', f'[{timestamp}] {text}')
        self.text_widget.see('end')
        self.text_widget.configure(state='disabled')
        self.original_stdout.write(text)

    def flush(self):
        self.original_stdout.flush()
class ScraperGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Twitter Scraper")
        self.geometry("900x800")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)  

        self.cred_frame = ctk.CTkFrame(self)
        self.cred_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        cred_title = ctk.CTkLabel(self.cred_frame, text="Credentials", font=ctk.CTkFont(size=16, weight="bold"))
        cred_title.pack(pady=5)

        self.email = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Email")
        self.email.pack(padx=20, pady=5)

        self.username = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Username")
        self.username.pack(padx=20, pady=5)

        self.password = ctk.CTkEntry(self.cred_frame, width=400, placeholder_text="Password", show="*")
        self.password.pack(padx=20, pady=5)

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        search_title = ctk.CTkLabel(self.search_frame, text="Searches", font=ctk.CTkFont(size=16, weight="bold"))
        search_title.pack(pady=5)

        self.searches_container = ScrollableFrame(self.search_frame, height=150)  
        self.searches_container.pack(fill="x", padx=10, expand=True)

        self.add_search_btn = ctk.CTkButton(
            self.search_frame, 
            text="Add Search", 
            command=self.add_search
        )
        self.add_search_btn.pack(pady=10)

        self.message_frame = ctk.CTkFrame(self)
        self.message_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        message_title = ctk.CTkLabel(self.message_frame, text="Custom Message", font=ctk.CTkFont(size=16, weight="bold"))
        message_title.pack(pady=5)

        self.custom_message = ctk.CTkTextbox(self.message_frame, height=60)
        self.custom_message.pack(fill="x", padx=20, pady=5)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.get_users_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Get Users",
            command=self.start_get_users
        )
        self.get_users_btn.pack(side="left", padx=10)
        
        self.filter_send_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Filter and Send Messages",
            command=self.start_filter_and_message
        )
        self.filter_send_btn.pack(side="left", padx=10)

        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=4, column=0, padx=20, pady=(10,20), sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)  
        
        log_title = ctk.CTkLabel(self.log_frame, text="Logs", font=ctk.CTkFont(size=16, weight="bold"))
        log_title.grid(row=0, column=0, pady=5)

        self.log_text = ctk.CTkTextbox(self.log_frame) 
        self.log_text.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        sys.stdout = CustomLogger(self.log_text)

        self.load_default_config()

    def add_search(self):
        search_entry = SearchEntry(self.searches_container)
        search_entry.pack(fill="x", pady=2)

    def load_default_config(self):
        default_config = {
            "mail": "scprbot@gmail.com",
            "username": "NftScpr",
            "password": "scrapperbot25",
            "busquedas": [
                {
                    "scroll_posts": 6,
                    "scroll_comments": 2,
                    "query": "share nft min_replies:20 -giveaway -address -adress -wallet -giveaways -scam -winner"
                },
                {
                    "scroll_posts": 6,
                    "scroll_comments": 2,
                    "query": "sell your nft min_replies:30 -giveaway -address -adress -wallet -giveaways -scam -winner"
                },
                {
                    "scroll_posts": 8,
                    "scroll_comments": 2,
                    "query": "drop nft min_replies:30 -giveaway -address -adress -wallet -giveaways -scam -winner"
                },
                {
                    "scroll_posts": 6,
                    "scroll_comments": 2,
                    "query": "shill nft min_replies:30 -giveaway -address -adress -wallet -giveaways -scam -winner"
                },
                {
                    "scroll_posts": 5,
                    "scroll_comments": 1,
                    "query": "buy nft min_replies:30 -giveaway -address -adress -wallet -giveaways -scam -winner"
                },
                {
                    "scroll_posts": 7,
                    "scroll_comments": 2,
                    "query": "show nft min_replies:30 -giveaway -address -adress -wallet -giveaways -scam -winner"
                },
                {
                    "scroll_posts": 16,
                    "scroll_comments": 1,
                    "query": "\"I've just created \" @rarible"
                },
                {
                    "scroll_posts": 16,
                    "scroll_comments": 0,
                    "query": "\"foundation.app/@\" (a OR e OR i OR o OR u OR l OR z OR x OR q OR w OR @)"
                },
                {
                    "scroll_posts": 16,
                    "scroll_comments": 0,
                    "query": "via @opensea"
                }
            ]
        }

        self.email.insert(0, default_config["mail"])
        self.username.insert(0, default_config["username"])
        self.password.insert(0, default_config["password"])
        
        self.custom_message.insert("1.0", "Hola {user}, cómo estás? Te escribimos porque encontramos una propuesta muy interesante para ti...")
        
        for search in default_config["busquedas"]:
            entry = SearchEntry(self.searches_container)
            entry.pack(fill="x", pady=2)
            entry.query.insert(0, search["query"])
            entry.scroll_posts.insert(0, str(search["scroll_posts"]))
            entry.scroll_comments.insert(0, str(search["scroll_comments"]))

    def save_config(self):
        config = {
            "mail": self.email.get(),
            "username": self.username.get(),
            "password": self.password.get(),
            "busquedas": [search.get_data() for search in self.searches_container.winfo_children()]
        }
        
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

    def prepare_config(self):
        self.save_config()
        with open("config.json", "r") as f:
            config = json.load(f)
        
        mail = config["mail"]
        username = config["username"]
        password = config["password"]
        busquedas = [
            [
                b["scroll_posts"],
                b["scroll_comments"],
                f"https://x.com/search?q={quote(b['query'])}&src=typed_query&f=live"
            ]
            for b in config["busquedas"]
        ]
        
        return mail, username, password, busquedas

    def start_get_users(self):
        def run():
            self.get_users_btn.configure(state="disabled")
            try:
                mail, username, password, busquedas = self.prepare_config()
                self.driver = get_users(busquedas, mail, username, password)
            finally:
                self.get_users_btn.configure(state="normal")
        
        thread = threading.Thread(target=run)
        thread.start()

    def start_filter_and_message(self):
        def run():
            self.filter_send_btn.configure(state="disabled")
            try:
                if not hasattr(self, 'driver'):
                    print("Please run 'Get Users' first!")
                    return
                    
                mail, username, password, _ = self.prepare_config()
                
                with open("funcs.py", "r") as f:
                    content = f.read()
                
                new_message = self.custom_message.get("1.0", "end-1c")
                updated_content = content.replace(
                    'Hola {user}, cómo estás? Este mensaje esta hecho con un scraper por Tato. Te escribimos porque encontramos una propuesta muy interesante para ti...',
                    new_message
                )
                
                with open("funcs.py", "w") as f:
                    f.write(updated_content)
                
                self.driver = filter_and_message(self.driver, mail, username, password)
            finally:
                self.filter_send_btn.configure(state="normal")
        
        thread = threading.Thread(target=run)
        thread.start()

if __name__ == "__main__":
    app = ScraperGUI()
    app.mainloop()
