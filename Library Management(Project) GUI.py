import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector as v
from datetime import date
import os
import platform
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # Global variables for MySQL credentials
        self.mysql_user = None
        self.mysql_password = None
        
        # Create a style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#4CAF50", foreground="black", font=('Arial', 10, 'bold'), padding=6)
        self.style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        self.style.configure("Header.TLabel", font=('Arial', 16, 'bold'), background="#f0f0f0")
        self.style.configure("SubHeader.TLabel", font=('Arial', 12, 'bold'), background="#f0f0f0")
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Database connection frame
        self.db_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.db_frame, text="Database Connection")
        
        # Setup the database connection frame
        self.setup_db_connection_frame()
        
        # Initially hide other tabs
        # They will be added after successful connection
        
    def setup_db_connection_frame(self):
        # Create a frame for connection info
        connection_frame = ttk.Frame(self.db_frame, padding="20")
        connection_frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(connection_frame, text="Connect to MySQL Database", style="Header.TLabel")
        header_label.pack(pady=(0, 20))
        
        # Username
        username_frame = ttk.Frame(connection_frame)
        username_frame.pack(fill=tk.X, pady=5)
        
        username_label = ttk.Label(username_frame, text="MySQL Username:", width=20)
        username_label.pack(side=tk.LEFT, padx=5)
        
        self.username_entry = ttk.Entry(username_frame, width=30)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        self.username_entry.focus()
        
        # Password
        password_frame = ttk.Frame(connection_frame)
        password_frame.pack(fill=tk.X, pady=5)
        
        password_label = ttk.Label(password_frame, text="MySQL Password:", width=20)
        password_label.pack(side=tk.LEFT, padx=5)
        
        self.password_entry = ttk.Entry(password_frame, width=30, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        # Connect Button
        connect_button = ttk.Button(connection_frame, text="Connect", command=self.connect_database)
        connect_button.pack(pady=20)
        
        # Status Label
        self.status_label = ttk.Label(connection_frame, text="", foreground="blue")
        self.status_label.pack(pady=10)
        
    def connect_database(self):
        self.mysql_user = self.username_entry.get()
        self.mysql_password = self.password_entry.get()
        
        if not self.mysql_user or not self.mysql_password:
            messagebox.showerror("Error", "Username and Password are required")
            return
            
        try:
            self.status_label.config(text="Connecting to database...")
            self.root.update()
            
            # Attempt to connect to MySQL
            conn = v.connect(host="localhost", user=self.mysql_user, passwd=self.mysql_password, charset="utf8")
            
            if conn.is_connected():
                self.status_label.config(text="Connected successfully!")
                
                # Create cursor and setup database
                mycur = conn.cursor()
                mycur.execute("CREATE DATABASE IF NOT EXISTS library_management")
                
                # Connect to the library_management database
                self.cnx = v.connect(
                    user=self.mysql_user,
                    passwd=self.mysql_password,
                    host='localhost',
                    database="library_management"
                )
                
                # Create required tables
                cursor = self.cnx.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS bookrecord(Bno INTEGER PRIMARY KEY, Bname VARCHAR(30) NOT NULL, Author VARCHAR(40), Price DECIMAL, publ VARCHAR(40), qty INTEGER, d_o_purchase DATE)")
                cursor.execute("CREATE TABLE IF NOT EXISTS Member(Mno INTEGER PRIMARY KEY, Mname VARCHAR(30) NOT NULL, MOB BIGINT(10) NOT NULL, DOM DATE, ADR VARCHAR(50))")
                cursor.execute("CREATE TABLE IF NOT EXISTS issue(Bno INTEGER REFERENCES bookrecord(bno), Mno INTEGER REFERENCES member(mno), doi DATE, dor DATE)")
                
                # Setup other tabs after successful connection
                self.setup_main_tabs()
                
                # Switch to the main menu tab
                self.notebook.select(1)  # Index 1 is the Main Menu tab
                
            else:
                self.status_label.config(text="Failed to connect to the database.")
                
        except v.Error as err:
            error_msg = f"Error: {err}"
            self.status_label.config(text=error_msg)
            messagebox.showerror("Database Error", error_msg)
    
    def setup_main_tabs(self):
        # Main Menu Tab
        self.main_menu_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_menu_frame, text="Main Menu")
        
        # Book Management Tab
        self.book_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.book_frame, text="Book Management")
        
        # Member Management Tab
        self.member_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.member_frame, text="Member Management")
        
        # Issue/Return Tab
        self.issue_return_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.issue_return_frame, text="Issue & Return")
        
        # Setup the content for each tab
        self.setup_main_menu()
        self.setup_book_management()
        self.setup_member_management()
        self.setup_issue_return()
    
    def setup_main_menu(self):
        main_frame = ttk.Frame(self.main_menu_frame, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(main_frame, text="Library Management System", style="Header.TLabel")
        header_label.pack(pady=(0, 30))
        
        # Description
        description = """
        Welcome to the Library Management System!
        
        This application allows you to manage books, members, and book issue/return.
        
        Use the tabs above to navigate between different functions:
        - Book Management: Add, view, search, update, or delete books
        - Member Management: Add, view, search, update, or delete members
        - Issue & Return: Issue books to members, return books, and view status
        
        Connected to MySQL as: {}
        """.format(self.mysql_user)
        
        desc_label = ttk.Label(main_frame, text=description, justify=tk.LEFT)
        desc_label.pack(pady=10)
        
        # Buttons frame for direct access
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)
        
        # Book Management Button
        book_button = ttk.Button(buttons_frame, text="Book Management", 
                                 command=lambda: self.notebook.select(2))
        book_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Member Management Button
        member_button = ttk.Button(buttons_frame, text="Member Management", 
                                  command=lambda: self.notebook.select(3))
        member_button.grid(row=0, column=1, padx=10, pady=10)
        
        # Issue/Return Button
        issue_button = ttk.Button(buttons_frame, text="Issue & Return", 
                                 command=lambda: self.notebook.select(4))
        issue_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Exit Button
        exit_button = ttk.Button(buttons_frame, text="Exit Application", 
                               command=self.root.destroy)
        exit_button.grid(row=1, column=1, padx=10, pady=10)
    
    def setup_book_management(self):
        # Create a notebook for book management options
        book_notebook = ttk.Notebook(self.book_frame)
        book_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add Book Tab
        add_book_frame = ttk.Frame(book_notebook)
        book_notebook.add(add_book_frame, text="Add Book")
        self.setup_add_book_frame(add_book_frame)
        
        # Display Books Tab
        display_books_frame = ttk.Frame(book_notebook)
        book_notebook.add(display_books_frame, text="Display Books")
        self.setup_display_books_frame(display_books_frame)
        
        # Search Book Tab
        search_book_frame = ttk.Frame(book_notebook)
        book_notebook.add(search_book_frame, text="Search Book")
        self.setup_search_book_frame(search_book_frame)
        
        # Delete Book Tab
        delete_book_frame = ttk.Frame(book_notebook)
        book_notebook.add(delete_book_frame, text="Delete Book")
        self.setup_delete_book_frame(delete_book_frame)
        
        # Update Book Tab
        update_book_frame = ttk.Frame(book_notebook)
        book_notebook.add(update_book_frame, text="Update Book")
        self.setup_update_book_frame(update_book_frame)
    
    def setup_add_book_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Add New Book", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Book Code
        ttk.Label(frame, text="Book Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.book_code_entry = ttk.Entry(frame, width=30)
        self.book_code_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Book Name
        ttk.Label(frame, text="Book Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.book_name_entry = ttk.Entry(frame, width=30)
        self.book_name_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Author
        ttk.Label(frame, text="Author:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.author_entry = ttk.Entry(frame, width=30)
        self.author_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Price
        ttk.Label(frame, text="Price:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.price_entry = ttk.Entry(frame, width=30)
        self.price_entry.grid(row=4, column=1, pady=5, padx=5)
        
        # Publisher
        ttk.Label(frame, text="Publisher:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.publisher_entry = ttk.Entry(frame, width=30)
        self.publisher_entry.grid(row=5, column=1, pady=5, padx=5)
        
        # Quantity
        ttk.Label(frame, text="Quantity:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.quantity_entry = ttk.Entry(frame, width=30)
        self.quantity_entry.grid(row=6, column=1, pady=5, padx=5)
        
        # Date of Purchase
        ttk.Label(frame, text="Date of Purchase:").grid(row=7, column=0, sticky=tk.W, pady=5)
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=7, column=1, pady=5, padx=5)
        
        # Date, Month, Year entries
        self.day_entry = ttk.Combobox(date_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.day_entry.set("Day")
        self.day_entry.pack(side=tk.LEFT, padx=2)
        
        self.month_entry = ttk.Combobox(date_frame, width=5, values=[str(i) for i in range(1, 13)])
        self.month_entry.set("Month")
        self.month_entry.pack(side=tk.LEFT, padx=2)
        
        self.year_entry = ttk.Combobox(date_frame, width=8, 
                                      values=[str(i) for i in range(2000, 2026)])
        self.year_entry.set("Year")
        self.year_entry.pack(side=tk.LEFT, padx=2)
        
        # Add Book Button
        add_button = ttk.Button(frame, text="Add Book", command=self.add_book)
        add_button.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Status Label
        self.add_book_status = ttk.Label(frame, text="", foreground="blue")
        self.add_book_status.grid(row=9, column=0, columnspan=2, pady=5)
        
        # Clear Fields Button
        clear_button = ttk.Button(frame, text="Clear Fields", command=self.clear_book_fields)
        clear_button.grid(row=10, column=0, columnspan=2, pady=5)
    
    def setup_display_books_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Book Records", style="Header.TLabel")
        header_label.pack(pady=(0, 20))
        
        # Create a frame for the scrolled text and buttons
        display_frame = ttk.Frame(frame)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Book Display Area
        self.book_display = scrolledtext.ScrolledText(display_frame, width=80, height=20, wrap=tk.WORD)
        self.book_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Refresh Button
        refresh_button = ttk.Button(frame, text="Refresh Book List", command=self.display_books)
        refresh_button.pack(pady=10)
    
    def setup_search_book_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Search Book", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Book Code
        ttk.Label(frame, text="Enter Book Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.search_book_entry = ttk.Entry(frame, width=30)
        self.search_book_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Search Button
        search_button = ttk.Button(frame, text="Search Book", command=self.search_book)
        search_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results Area
        ttk.Label(frame, text="Search Results:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.search_results = scrolledtext.ScrolledText(frame, width=60, height=15)
        self.search_results.grid(row=4, column=0, columnspan=2, pady=5)
    
    def setup_delete_book_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Delete Book", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Book Code
        ttk.Label(frame, text="Enter Book Code to Delete:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.delete_book_entry = ttk.Entry(frame, width=30)
        self.delete_book_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Delete Button
        delete_button = ttk.Button(frame, text="Delete Book", command=self.delete_book)
        delete_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Status Label
        self.delete_book_status = ttk.Label(frame, text="", foreground="blue")
        self.delete_book_status.grid(row=3, column=0, columnspan=2, pady=5)
    
    def setup_update_book_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Update Book", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Book Code - for searching the book to update
        ttk.Label(frame, text="Enter Book Code to Update:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.update_book_code_entry = ttk.Entry(frame, width=30)
        self.update_book_code_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Search Button
        search_update_button = ttk.Button(frame, text="Search", command=self.fetch_book_for_update)
        search_update_button.grid(row=1, column=2, pady=5, padx=5)
        
        # Separator
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        
        # New data fields
        ttk.Label(frame, text="Enter New Data", style="SubHeader.TLabel").grid(row=3, column=0, columnspan=3, pady=10)
        
        # Book Name
        ttk.Label(frame, text="Book Name:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.update_book_name_entry = ttk.Entry(frame, width=30)
        self.update_book_name_entry.grid(row=4, column=1, columnspan=2, pady=5, padx=5)
        
        # Author
        ttk.Label(frame, text="Author:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.update_author_entry = ttk.Entry(frame, width=30)
        self.update_author_entry.grid(row=5, column=1, columnspan=2, pady=5, padx=5)
        
        # Price
        ttk.Label(frame, text="Price:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.update_price_entry = ttk.Entry(frame, width=30)
        self.update_price_entry.grid(row=6, column=1, columnspan=2, pady=5, padx=5)
        
        # Publisher
        ttk.Label(frame, text="Publisher:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.update_publisher_entry = ttk.Entry(frame, width=30)
        self.update_publisher_entry.grid(row=7, column=1, columnspan=2, pady=5, padx=5)
        
        # Quantity
        ttk.Label(frame, text="Quantity:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.update_quantity_entry = ttk.Entry(frame, width=30)
        self.update_quantity_entry.grid(row=8, column=1, columnspan=2, pady=5, padx=5)
        
        # Date of Purchase
        ttk.Label(frame, text="Date of Purchase:").grid(row=9, column=0, sticky=tk.W, pady=5)
        update_date_frame = ttk.Frame(frame)
        update_date_frame.grid(row=9, column=1, columnspan=2, pady=5, padx=5)
        
        # Date, Month, Year entries for update
        self.update_day_entry = ttk.Combobox(update_date_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.update_day_entry.set("Day")
        self.update_day_entry.pack(side=tk.LEFT, padx=2)
        
        self.update_month_entry = ttk.Combobox(update_date_frame, width=5, values=[str(i) for i in range(1, 13)])
        self.update_month_entry.set("Month")
        self.update_month_entry.pack(side=tk.LEFT, padx=2)
        
        self.update_year_entry = ttk.Combobox(update_date_frame, width=8, 
                                            values=[str(i) for i in range(2000, 2026)])
        self.update_year_entry.set("Year")
        self.update_year_entry.pack(side=tk.LEFT, padx=2)
        
        # Update Button
        update_button = ttk.Button(frame, text="Update Book", command=self.update_book)
        update_button.grid(row=10, column=0, columnspan=3, pady=20)
        
        # Status Label
        self.update_book_status = ttk.Label(frame, text="", foreground="blue")
        self.update_book_status.grid(row=11, column=0, columnspan=3, pady=5)
    
    def setup_member_management(self):
        # Create a notebook for member management options
        member_notebook = ttk.Notebook(self.member_frame)
        member_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add Member Tab
        add_member_frame = ttk.Frame(member_notebook)
        member_notebook.add(add_member_frame, text="Add Member")
        self.setup_add_member_frame(add_member_frame)
        
        # Display Members Tab
        display_members_frame = ttk.Frame(member_notebook)
        member_notebook.add(display_members_frame, text="Display Members")
        self.setup_display_members_frame(display_members_frame)
        
        # Search Member Tab
        search_member_frame = ttk.Frame(member_notebook)
        member_notebook.add(search_member_frame, text="Search Member")
        self.setup_search_member_frame(search_member_frame)
        
        # Delete Member Tab
        delete_member_frame = ttk.Frame(member_notebook)
        member_notebook.add(delete_member_frame, text="Delete Member")
        self.setup_delete_member_frame(delete_member_frame)
        
        # Update Member Tab
        update_member_frame = ttk.Frame(member_notebook)
        member_notebook.add(update_member_frame, text="Update Member")
        self.setup_update_member_frame(update_member_frame)
    
    def setup_add_member_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Add New Member", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Member Code
        ttk.Label(frame, text="Member Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.member_code_entry = ttk.Entry(frame, width=30)
        self.member_code_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Member Name
        ttk.Label(frame, text="Member Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.member_name_entry = ttk.Entry(frame, width=30)
        self.member_name_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Mobile Number
        ttk.Label(frame, text="Mobile Number:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.mobile_entry = ttk.Entry(frame, width=30)
        self.mobile_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Date of Membership
        ttk.Label(frame, text="Date of Membership:").grid(row=4, column=0, sticky=tk.W, pady=5)
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=4, column=1, pady=5, padx=5)
        
        # Date, Month, Year entries
        self.member_day_entry = ttk.Combobox(date_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.member_day_entry.set("Day")
        self.member_day_entry.pack(side=tk.LEFT, padx=2)
        
        self.member_month_entry = ttk.Combobox(date_frame, width=5, values=[str(i) for i in range(1, 13)])
        self.member_month_entry.set("Month")
        self.member_month_entry.pack(side=tk.LEFT, padx=2)
        
        self.member_year_entry = ttk.Combobox(date_frame, width=8, 
                                             values=[str(i) for i in range(2000, 2026)])
        self.member_year_entry.set("Year")
        self.member_year_entry.pack(side=tk.LEFT, padx=2)
        
        # Address
        ttk.Label(frame, text="Address:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.address_entry = ttk.Entry(frame, width=30)
        self.address_entry.grid(row=5, column=1, pady=5, padx=5)
        
        # Add Member Button
        add_button = ttk.Button(frame, text="Add Member", command=self.add_member)
        add_button.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Status Label
        self.add_member_status = ttk.Label(frame, text="", foreground="blue")
        self.add_member_status.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Clear Fields Button
        clear_button = ttk.Button(frame, text="Clear Fields", command=self.clear_member_fields)
        clear_button.grid(row=8, column=0, columnspan=2, pady=5)
    
    def setup_display_members_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Member Records", style="Header.TLabel")
        header_label.pack(pady=(0, 20))
        
        # Create a frame for the scrolled text and buttons
        display_frame = ttk.Frame(frame)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Member Display Area
        self.member_display = scrolledtext.ScrolledText(display_frame, width=80, height=20, wrap=tk.WORD)
        self.member_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Refresh Button
        refresh_button = ttk.Button(frame, text="Refresh Member List", command=self.display_members)
        refresh_button.pack(pady=10)

    def setup_search_member_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Search Member", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Search Type
        ttk.Label(frame, text="Search By:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.search_type = tk.StringVar(value="code")
        code_radio = ttk.Radiobutton(frame, text="Member Code", variable=self.search_type, value="code")
        code_radio.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        
        name_radio = ttk.Radiobutton(frame, text="Member Name", variable=self.search_type, value="name")
        name_radio.grid(row=1, column=2, pady=5, padx=5, sticky=tk.W)
        
        # Search Term
        ttk.Label(frame, text="Search Term:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.search_member_entry = ttk.Entry(frame, width=30)
        self.search_member_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=5)
        
        # Search Button
        search_button = ttk.Button(frame, text="Search Member", command=self.search_member)
        search_button.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Results Area
        ttk.Label(frame, text="Search Results:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.member_search_results = scrolledtext.ScrolledText(frame, width=60, height=15)
        self.member_search_results.grid(row=5, column=0, columnspan=3, pady=5)
    
    def setup_delete_member_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Delete Member", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Member Code
        ttk.Label(frame, text="Enter Member Code to Delete:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.delete_member_entry = ttk.Entry(frame, width=30)
        self.delete_member_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Delete Button
        delete_button = ttk.Button(frame, text="Delete Member", command=self.delete_member)
        delete_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Status Label
        self.delete_member_status = ttk.Label(frame, text="", foreground="blue")
        self.delete_member_status.grid(row=3, column=0, columnspan=2, pady=5)
    
    def setup_update_member_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Update Member", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Member Code - for searching the member to update
        ttk.Label(frame, text="Enter Member Code to Update:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.update_member_code_entry = ttk.Entry(frame, width=30)
        self.update_member_code_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Search Button
        search_update_button = ttk.Button(frame, text="Search", command=self.fetch_member_for_update)
        search_update_button.grid(row=1, column=2, pady=5, padx=5)
        
        # Separator
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        
        # New data fields
        ttk.Label(frame, text="Enter New Data", style="SubHeader.TLabel").grid(row=3, column=0, columnspan=3, pady=10)
        
        # Member Name
        ttk.Label(frame, text="Member Name:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.update_member_name_entry = ttk.Entry(frame, width=30)
        self.update_member_name_entry.grid(row=4, column=1, columnspan=2, pady=5, padx=5)
        
        # Mobile
        ttk.Label(frame, text="Mobile Number:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.update_mobile_entry = ttk.Entry(frame, width=30)
        self.update_mobile_entry.grid(row=5, column=1, columnspan=2, pady=5, padx=5)
        
        # Address
        ttk.Label(frame, text="Address:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.update_address_entry = ttk.Entry(frame, width=30)
        self.update_address_entry.grid(row=6, column=1, columnspan=2, pady=5, padx=5)
        
        # Date of Membership
        ttk.Label(frame, text="Date of Membership:").grid(row=7, column=0, sticky=tk.W, pady=5)
        update_date_frame = ttk.Frame(frame)
        update_date_frame.grid(row=7, column=1, columnspan=2, pady=5, padx=5)
        
        # Date, Month, Year entries for update
        self.update_member_day_entry = ttk.Combobox(update_date_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.update_member_day_entry.set("Day")
        self.update_member_day_entry.pack(side=tk.LEFT, padx=2)
        
        self.update_member_month_entry = ttk.Combobox(update_date_frame, width=5, values=[str(i) for i in range(1, 13)])
        self.update_member_month_entry.set("Month")
        self.update_member_month_entry.pack(side=tk.LEFT, padx=2)
        
        self.update_member_year_entry = ttk.Combobox(update_date_frame, width=8, 
                                                   values=[str(i) for i in range(2000, 2026)])
        self.update_member_year_entry.set("Year")
        self.update_member_year_entry.pack(side=tk.LEFT, padx=2)
        
        # Update Button
        update_button = ttk.Button(frame, text="Update Member", command=self.update_member)
        update_button.grid(row=8, column=0, columnspan=3, pady=20)
        
        # Status Label
        self.update_member_status = ttk.Label(frame, text="", foreground="blue")
        self.update_member_status.grid(row=9, column=0, columnspan=3, pady=5)
    
    def setup_issue_return(self):
        # Create a notebook for issue/return options
        issue_return_notebook = ttk.Notebook(self.issue_return_frame)
        issue_return_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Issue Book Tab
        issue_frame = ttk.Frame(issue_return_notebook)
        issue_return_notebook.add(issue_frame, text="Issue Book")
        self.setup_issue_book_frame(issue_frame)
        
        # Return Book Tab
        return_frame = ttk.Frame(issue_return_notebook)
        issue_return_notebook.add(return_frame, text="Return Book")
        self.setup_return_book_frame(return_frame)
        
        # View Issued Books Tab
        view_issued_frame = ttk.Frame(issue_return_notebook)
        issue_return_notebook.add(view_issued_frame, text="View Issued Books")
        self.setup_view_issued_frame(view_issued_frame)
    
    def setup_issue_book_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Issue Book", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Book Code
        ttk.Label(frame, text="Book Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.issue_book_code_entry = ttk.Entry(frame, width=30)
        self.issue_book_code_entry.grid(row=1, column=1, pady=5, padx=5)
        
        book_search_button = ttk.Button(frame, text="Verify", command=self.verify_book_for_issue)
        book_search_button.grid(row=1, column=2, pady=5, padx=5)
        
        # Book verification status
        self.book_verify_label = ttk.Label(frame, text="", foreground="blue")
        self.book_verify_label.grid(row=2, column=0, columnspan=3, pady=5)
        
        # Member Code
        ttk.Label(frame, text="Member Code:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.issue_member_code_entry = ttk.Entry(frame, width=30)
        self.issue_member_code_entry.grid(row=3, column=1, pady=5, padx=5)
        
        member_search_button = ttk.Button(frame, text="Verify", command=self.verify_member_for_issue)
        member_search_button.grid(row=3, column=2, pady=5, padx=5)
        
        # Member verification status
        self.member_verify_label = ttk.Label(frame, text="", foreground="blue")
        self.member_verify_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Date of Issue
        ttk.Label(frame, text="Date of Issue:").grid(row=5, column=0, sticky=tk.W, pady=5)
        issue_date_frame = ttk.Frame(frame)
        issue_date_frame.grid(row=5, column=1, columnspan=2, pady=5, padx=5)
        
        # Today's date by default
        today = date.today()
        
        # Date, Month, Year entries
        self.issue_day_entry = ttk.Combobox(issue_date_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.issue_day_entry.set(str(today.day))
        self.issue_day_entry.pack(side=tk.LEFT, padx=2)
        
        self.issue_month_entry = ttk.Combobox(issue_date_frame, width=5, values=[str(i) for i in range(1, 13)])
        self.issue_month_entry.set(str(today.month))
        self.issue_month_entry.pack(side=tk.LEFT, padx=2)
        
        self.issue_year_entry = ttk.Combobox(issue_date_frame, width=8, 
                                           values=[str(i) for i in range(2000, 2026)])
        self.issue_year_entry.set(str(today.year))
        self.issue_year_entry.pack(side=tk.LEFT, padx=2)
        
        # Expected Return Date
        ttk.Label(frame, text="Expected Return Date:").grid(row=6, column=0, sticky=tk.W, pady=5)
        return_date_frame = ttk.Frame(frame)
        return_date_frame.grid(row=6, column=1, columnspan=2, pady=5, padx=5)
        
        # Date, Month, Year entries for return
        self.return_day_entry = ttk.Combobox(return_date_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.return_day_entry.set(str(today.day))
        self.return_day_entry.pack(side=tk.LEFT, padx=2)
        
        self.return_month_entry = ttk.Combobox(return_date_frame, width=5, values=[str(i) for i in range(1, 13)])
        self.return_month_entry.set(str(today.month))
        self.return_month_entry.pack(side=tk.LEFT, padx=2)
        
        self.return_year_entry = ttk.Combobox(return_date_frame, width=8, 
                                            values=[str(i) for i in range(2000, 2026)])
        self.return_year_entry.set(str(today.year))
        self.return_year_entry.pack(side=tk.LEFT, padx=2)
        
        # Issue Button
        issue_button = ttk.Button(frame, text="Issue Book", command=self.issue_book)
        issue_button.grid(row=7, column=0, columnspan=3, pady=20)
        
        # Status Label
        self.issue_status = ttk.Label(frame, text="", foreground="blue")
        self.issue_status.grid(row=8, column=0, columnspan=3, pady=5)
    
    def setup_return_book_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Return Book", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Book Code
        ttk.Label(frame, text="Book Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.return_book_code_entry = ttk.Entry(frame, width=30)
        self.return_book_code_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Member Code
        ttk.Label(frame, text="Member Code:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.return_member_code_entry = ttk.Entry(frame, width=30)
        self.return_member_code_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Verify Button
        verify_button = ttk.Button(frame, text="Verify Issue", command=self.verify_issue)
        verify_button.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Issue verification status
        self.issue_verify_label = ttk.Label(frame, text="", foreground="blue")
        self.issue_verify_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Return Date
        ttk.Label(frame, text="Return Date:").grid(row=5, column=0, sticky=tk.W, pady=5)
        actual_return_date_frame = ttk.Frame(frame)
        actual_return_date_frame.grid(row=5, column=1, columnspan=2, pady=5, padx=5)
        
        # Today's date by default
        today = date.today()
        
        # Date, Month, Year entries for actual return
        self.actual_return_day_entry = ttk.Combobox(actual_return_date_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.actual_return_day_entry.set(str(today.day))
        self.actual_return_day_entry.pack(side=tk.LEFT, padx=2)
        
        self.actual_return_month_entry = ttk.Combobox(actual_return_date_frame, width=5, values=[str(i) for i in range(1, 13)])
        self.actual_return_month_entry.set(str(today.month))
        self.actual_return_month_entry.pack(side=tk.LEFT, padx=2)
        
        self.actual_return_year_entry = ttk.Combobox(actual_return_date_frame, width=8, 
                                                   values=[str(i) for i in range(2000, 2026)])
        self.actual_return_year_entry.set(str(today.year))
        self.actual_return_year_entry.pack(side=tk.LEFT, padx=2)
        
        # Return Button
        return_button = ttk.Button(frame, text="Return Book", command=self.return_book)
        return_button.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Status Label
        self.return_status = ttk.Label(frame, text="", foreground="blue")
        self.return_status.grid(row=7, column=0, columnspan=3, pady=5)
    
    def setup_view_issued_frame(self, parent):
        frame = ttk.Frame(parent, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_label = ttk.Label(frame, text="Issued Books", style="Header.TLabel")
        header_label.pack(pady=(0, 20))
        
        # Create a frame for the scrolled text and buttons
        display_frame = ttk.Frame(frame)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Issued Books Display Area
        self.issued_books_display = scrolledtext.ScrolledText(display_frame, width=80, height=20, wrap=tk.WORD)
        self.issued_books_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Refresh Button
        refresh_button = ttk.Button(frame, text="Refresh Issued Books List", command=self.display_issued_books)
        refresh_button.pack(pady=10)
    
    # Book Management Methods
    def add_book(self):
        try:
            book_code = self.book_code_entry.get()
            book_name = self.book_name_entry.get()
            author = self.author_entry.get()
            price = self.price_entry.get()
            publisher = self.publisher_entry.get()
            quantity = self.quantity_entry.get()
            
            # Validate inputs
            if not book_code or not book_code.isdigit():
                self.add_book_status.config(text="Book Code must be a valid integer", foreground="red")
                return
                
            if not book_name:
                self.add_book_status.config(text="Book Name is required", foreground="red")
                return
                
            if price and not self.is_valid_decimal(price):
                self.add_book_status.config(text="Price must be a valid number", foreground="red")
                return
                
            if quantity and not quantity.isdigit():
                self.add_book_status.config(text="Quantity must be a valid integer", foreground="red")
                return
                
            # Check date
            day = self.day_entry.get()
            month = self.month_entry.get()
            year = self.year_entry.get()
            
            if day == "Day" or month == "Month" or year == "Year":
                purchase_date = date.today()
            else:
                try:
                    purchase_date = date(int(year), int(month), int(day))
                except ValueError:
                    self.add_book_status.config(text="Invalid date", foreground="red")
                    return
            
            # Check if book code already exists
            cursor = self.cnx.cursor()
            cursor.execute("SELECT Bno FROM bookrecord WHERE Bno = %s", (book_code,))
            existing_book = cursor.fetchone()
            
            if existing_book:
                self.add_book_status.config(text=f"Book with code {book_code} already exists", foreground="red")
                return
            
            # Insert book record
            cursor.execute("INSERT INTO bookrecord (Bno, Bname, Author, Price, publ, qty, d_o_purchase) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                          (book_code, book_name, author, price, publisher, quantity, purchase_date))
            
            self.cnx.commit()
            self.add_book_status.config(text=f"Book '{book_name}' added successfully!", foreground="green")
            self.clear_book_fields()
            
        except Exception as e:
            self.add_book_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def clear_book_fields(self):
        self.book_code_entry.delete(0, tk.END)
        self.book_name_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.publisher_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.day_entry.set("Day")
        self.month_entry.set("Month")
        self.year_entry.set("Year")
        self.book_code_entry.focus()
    
    def display_books(self):
        try:
            cursor = self.cnx.cursor()
            cursor.execute("SELECT * FROM bookrecord ORDER BY Bno")
            books = cursor.fetchall()
            
            self.book_display.delete(1.0, tk.END)
            
            if not books:
                self.book_display.insert(tk.END, "No books found in the database.")
                return
            
            # Display column headers
            headers = "Book Code | Book Name | Author | Price | Publisher | Quantity | Purchase Date\n"
            self.book_display.insert(tk.END, headers)
            self.book_display.insert(tk.END, "-" * 100 + "\n")
            
            # Display book data
            for book in books:
                book_info = f"{book[0]} | {book[1]} | {book[2] or 'N/A'} | {book[3] or 'N/A'} | {book[4] or 'N/A'} | {book[5] or 'N/A'} | {book[6]}\n"
                self.book_display.insert(tk.END, book_info)
                
        except Exception as e:
            self.book_display.delete(1.0, tk.END)
            self.book_display.insert(tk.END, f"Error: {str(e)}")
    
    def search_book(self):
        try:
            book_code = self.search_book_entry.get()
            
            if not book_code or not book_code.isdigit():
                self.search_results.delete(1.0, tk.END)
                self.search_results.insert(tk.END, "Please enter a valid Book Code")
                return
            
            cursor = self.cnx.cursor()
            cursor.execute("SELECT * FROM bookrecord WHERE Bno = %s", (book_code,))
            book = cursor.fetchone()
            
            self.search_results.delete(1.0, tk.END)
            
            if not book:
                self.search_results.insert(tk.END, f"No book found with Book Code: {book_code}")
                return
            
            # Display book information
            self.search_results.insert(tk.END, "Book Details:\n")
            self.search_results.insert(tk.END, "-" * 50 + "\n")
            self.search_results.insert(tk.END, f"Book Code: {book[0]}\n")
            self.search_results.insert(tk.END, f"Book Name: {book[1]}\n")
            self.search_results.insert(tk.END, f"Author: {book[2] or 'N/A'}\n")
            self.search_results.insert(tk.END, f"Price: {book[3] or 'N/A'}\n")
            self.search_results.insert(tk.END, f"Publisher: {book[4] or 'N/A'}\n")
            self.search_results.insert(tk.END, f"Quantity: {book[5] or 'N/A'}\n")
            self.search_results.insert(tk.END, f"Purchase Date: {book[6]}\n")
            
            # Check if book is issued
            cursor.execute("SELECT Mno, doi, dor FROM issue WHERE Bno = %s", (book_code,))
            issue_info = cursor.fetchone()
            
            if issue_info:
                self.search_results.insert(tk.END, "\nIssue Status: Currently Issued\n")
                self.search_results.insert(tk.END, f"Issued to Member: {issue_info[0]}\n")
                self.search_results.insert(tk.END, f"Issue Date: {issue_info[1]}\n")
                if issue_info[2]:
                    self.search_results.insert(tk.END, f"Expected Return Date: {issue_info[2]}\n")
            else:
                self.search_results.insert(tk.END, "\nIssue Status: Available\n")
                
        except Exception as e:
            self.search_results.delete(1.0, tk.END)
            self.search_results.insert(tk.END, f"Error: {str(e)}")
    
    def delete_book(self):
        try:
            book_code = self.delete_book_entry.get()
            
            if not book_code or not book_code.isdigit():
                self.delete_book_status.config(text="Please enter a valid Book Code", foreground="red")
                return
            
            cursor = self.cnx.cursor()
            
            # Check if book exists
            cursor.execute("SELECT Bname FROM bookrecord WHERE Bno = %s", (book_code,))
            book = cursor.fetchone()
            
            if not book:
                self.delete_book_status.config(text=f"No book found with Book Code: {book_code}", foreground="red")
                return
            
            # Check if book is issued
            cursor.execute("SELECT COUNT(*) FROM issue WHERE Bno = %s", (book_code,))
            issue_count = cursor.fetchone()[0]
            
            if issue_count > 0:
                self.delete_book_status.config(text=f"Cannot delete book (Code: {book_code}) as it is currently issued", foreground="red")
                return
            
            # Delete the book
            cursor.execute("DELETE FROM bookrecord WHERE Bno = %s", (book_code,))
            self.cnx.commit()
            
            self.delete_book_status.config(text=f"Book '{book[0]}' (Code: {book_code}) deleted successfully", foreground="green")
            self.delete_book_entry.delete(0, tk.END)
            
        except Exception as e:
            self.delete_book_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def fetch_book_for_update(self):
        try:
            book_code = self.update_book_code_entry.get()
            
            if not book_code or not book_code.isdigit():
                self.update_book_status.config(text="Please enter a valid Book Code", foreground="red")
                return
            
            cursor = self.cnx.cursor()
            cursor.execute("SELECT * FROM bookrecord WHERE Bno = %s", (book_code,))
            book = cursor.fetchone()
            
            if not book:
                self.update_book_status.config(text=f"No book found with Book Code: {book_code}", foreground="red")
                return
            
            # Fill the update fields with current data
            self.update_book_name_entry.delete(0, tk.END)
            self.update_book_name_entry.insert(0, book[1])
            
            self.update_author_entry.delete(0, tk.END)
            if book[2]:
                self.update_author_entry.insert(0, book[2])
            
            self.update_price_entry.delete(0, tk.END)
            if book[3]:
                self.update_price_entry.insert(0, str(book[3]))
            
            self.update_publisher_entry.delete(0, tk.END)
            if book[4]:
                self.update_publisher_entry.insert(0, book[4])
            
            self.update_quantity_entry.delete(0, tk.END)
            if book[5]:
                self.update_quantity_entry.insert(0, str(book[5]))
            
            # Set date if available
            if book[6]:
                purchase_date = book[6]
                self.update_day_entry.set(str(purchase_date.day))
                self.update_month_entry.set(str(purchase_date.month))
                self.update_year_entry.set(str(purchase_date.year))
            
            self.update_book_status.config(text=f"Book '{book[1]}' (Code: {book_code}) loaded for update", foreground="green")
            
        except Exception as e:
            self.update_book_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def update_book(self):
        try:
            book_code = self.update_book_code_entry.get()
            book_name = self.update_book_name_entry.get()
            author = self.update_author_entry.get()
            price = self.update_price_entry.get()
            publisher = self.update_publisher_entry.get()
            quantity = self.update_quantity_entry.get()
            
            # Validate inputs
            if not book_code or not book_code.isdigit():
                self.update_book_status.config(text="Book Code must be a valid integer", foreground="red")
                return
                
            if not book_name:
                self.update_book_status.config(text="Book Name is required", foreground="red")
                return
                
            if price and not self.is_valid_decimal(price):
                self.update_book_status.config(text="Price must be a valid number", foreground="red")
                return
                
            if quantity and not quantity.isdigit():
                self.update_book_status.config(text="Quantity must be a valid integer", foreground="red")
                return
                
            # Check date
            day = self.update_day_entry.get()
            month = self.update_month_entry.get()
            year = self.update_year_entry.get()
            
            if day == "Day" or month == "Month" or year == "Year":
                purchase_date = date.today()
            else:
                try:
                    purchase_date = date(int(year), int(month), int(day))
                except ValueError:
                    self.update_book_status.config(text="Invalid date", foreground="red")
                    return
            
            # Update book record
            cursor = self.cnx.cursor()
            cursor.execute("""
                UPDATE bookrecord 
                SET Bname = %s, Author = %s, Price = %s, publ = %s, qty = %s, d_o_purchase = %s
                WHERE Bno = %s
            """, (book_name, author, price, publisher, quantity, purchase_date, book_code))
            
            self.cnx.commit()
            self.update_book_status.config(text=f"Book '{book_name}' updated successfully!", foreground="green")
            
        except Exception as e:
            self.update_book_status.config(text=f"Error: {str(e)}", foreground="red")
    
    # Member Management Methods
    def add_member(self):
        try:
            member_code = self.member_code_entry.get()
            member_name = self.member_name_entry.get()
            mobile = self.mobile_entry.get()
            address = self.address_entry.get()
            
            # Validate inputs
            if not member_code or not member_code.isdigit():
                self.add_member_status.config(text="Member Code must be a valid integer", foreground="red")
                return
                
            if not member_name:
                self.add_member_status.config(text="Member Name is required", foreground="red")
                return
                
            if mobile and not mobile.isdigit():
                self.add_member_status.config(text="Mobile number must contain only digits", foreground="red")
                return
            
            # Check date
            day = self.member_day_entry.get()
            month = self.member_month_entry.get()
            year = self.member_year_entry.get()
            
            if day == "Day" or month == "Month" or year == "Year":
                membership_date = date.today()
            else:
                try:
                    membership_date = date(int(year), int(month), int(day))
                except ValueError:
                    self.add_member_status.config(text="Invalid date", foreground="red")
                    return
            
            # Check if member code already exists
            cursor = self.cnx.cursor()
            cursor.execute("SELECT Mno FROM member WHERE Mno = %s", (member_code,))
            existing_member = cursor.fetchone()
            
            if existing_member:
                self.add_member_status.config(text=f"Member with code {member_code} already exists", foreground="red")
                return
            
            # Insert member record
            cursor.execute("INSERT INTO member (Mno, Mname, mob, addr, d_o_m) VALUES (%s, %s, %s, %s, %s)",
                          (member_code, member_name, mobile, address, membership_date))
            
            self.cnx.commit()
            self.add_member_status.config(text=f"Member '{member_name}' added successfully!", foreground="green")
            self.clear_member_fields()
            
        except Exception as e:
            self.add_member_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def clear_member_fields(self):
        self.member_code_entry.delete(0, tk.END)
        self.member_name_entry.delete(0, tk.END)
        self.mobile_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.member_day_entry.set("Day")
        self.member_month_entry.set("Month")
        self.member_year_entry.set("Year")
        self.member_code_entry.focus()
    
    def display_members(self):
        try:
            cursor = self.cnx.cursor()
            cursor.execute("SELECT * FROM member ORDER BY Mno")
            members = cursor.fetchall()
            
            self.member_display.delete(1.0, tk.END)
            
            if not members:
                self.member_display.insert(tk.END, "No members found in the database.")
                return
            
            # Display column headers
            headers = "Member Code | Member Name | Mobile | Address | Date of Membership\n"
            self.member_display.insert(tk.END, headers)
            self.member_display.insert(tk.END, "-" * 100 + "\n")
            
            # Display member data
            for member in members:
                member_info = f"{member[0]} | {member[1]} | {member[2] or 'N/A'} | {member[3] or 'N/A'} | {member[4]}\n"
                self.member_display.insert(tk.END, member_info)
                
        except Exception as e:
            self.member_display.delete(1.0, tk.END)
            self.member_display.insert(tk.END, f"Error: {str(e)}")
    
    def search_member(self):
        try:
            search_term = self.search_member_entry.get()
            search_type = self.search_type.get()
            
            if not search_term:
                self.member_search_results.delete(1.0, tk.END)
                self.member_search_results.insert(tk.END, "Please enter a search term")
                return
            
            cursor = self.cnx.cursor()
            
            if search_type == "code":
                if not search_term.isdigit():
                    self.member_search_results.delete(1.0, tk.END)
                    self.member_search_results.insert(tk.END, "Member Code must be a valid integer")
                    return
                    
                cursor.execute("SELECT * FROM member WHERE Mno = %s", (search_term,))
            else:  # search by name
                cursor.execute("SELECT * FROM member WHERE Mname LIKE %s", (f"%{search_term}%",))
                
            members = cursor.fetchall()
            
            self.member_search_results.delete(1.0, tk.END)
            
            if not members:
                self.member_search_results.insert(tk.END, f"No members found matching: {search_term}")
                return
            
            # Display column headers
            headers = "Member Code | Member Name | Mobile | Address | Date of Membership\n"
            self.member_search_results.insert(tk.END, headers)
            self.member_search_results.insert(tk.END, "-" * 100 + "\n")
            
            # Display member data
            for member in members:
                member_info = f"{member[0]} | {member[1]} | {member[2] or 'N/A'} | {member[3] or 'N/A'} | {member[4]}\n"
                self.member_search_results.insert(tk.END, member_info)
                
                # Check if member has issued books
                cursor.execute("""
                    SELECT b.Bno, b.Bname, i.doi, i.dor
                    FROM issue i
                    JOIN bookrecord b ON i.Bno = b.Bno
                    WHERE i.Mno = %s
                """, (member[0],))
                
                issued_books = cursor.fetchall()
                
                if issued_books:
                    self.member_search_results.insert(tk.END, "\nIssued Books:\n")
                    self.member_search_results.insert(tk.END, "Book Code | Book Name | Issue Date | Expected Return Date\n")
                    self.member_search_results.insert(tk.END, "-" * 80 + "\n")
                    
                    for book in issued_books:
                        book_info = f"{book[0]} | {book[1]} | {book[2]} | {book[3] or 'N/A'}\n"
                        self.member_search_results.insert(tk.END, book_info)
                
                self.member_search_results.insert(tk.END, "\n" + "-" * 100 + "\n")
                
        except Exception as e:
            self.member_search_results.delete(1.0, tk.END)
            self.member_search_results.insert(tk.END, f"Error: {str(e)}")
    
    def delete_member(self):
        try:
            member_code = self.delete_member_entry.get()
            
            if not member_code or not member_code.isdigit():
                self.delete_member_status.config(text="Please enter a valid Member Code", foreground="red")
                return
            
            cursor = self.cnx.cursor()
            
            # Check if member exists
            cursor.execute("SELECT Mname FROM member WHERE Mno = %s", (member_code,))
            member = cursor.fetchone()
            
            if not member:
                self.delete_member_status.config(text=f"No member found with Member Code: {member_code}", foreground="red")
                return
            
            # Check if member has issued books
            cursor.execute("SELECT COUNT(*) FROM issue WHERE Mno = %s", (member_code,))
            issue_count = cursor.fetchone()[0]
            
            if issue_count > 0:
                self.delete_member_status.config(
                    text=f"Cannot delete member (Code: {member_code}) as they have issued books", 
                    foreground="red"
                )
                return
            
            # Delete the member
            cursor.execute("DELETE FROM member WHERE Mno = %s", (member_code,))
            self.cnx.commit()
            
            self.delete_member_status.config(
                text=f"Member '{member[0]}' (Code: {member_code}) deleted successfully", 
                foreground="green"
            )
            self.delete_member_entry.delete(0, tk.END)
            
        except Exception as e:
            self.delete_member_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def fetch_member_for_update(self):
        try:
            member_code = self.update_member_code_entry.get()
            
            if not member_code or not member_code.isdigit():
                self.update_member_status.config(text="Please enter a valid Member Code", foreground="red")
                return
            
            cursor = self.cnx.cursor()
            cursor.execute("SELECT * FROM member WHERE Mno = %s", (member_code,))
            member = cursor.fetchone()
            
            if not member:
                self.update_member_status.config(text=f"No member found with Member Code: {member_code}", foreground="red")
                return
            
            # Fill the update fields with current data
            self.update_member_name_entry.delete(0, tk.END)
            self.update_member_name_entry.insert(0, member[1])
            
            self.update_mobile_entry.delete(0, tk.END)
            if member[2]:
                self.update_mobile_entry.insert(0, member[2])
            
            self.update_address_entry.delete(0, tk.END)
            if member[4]:
                self.update_address_entry.insert(0, member[4])
            
            # Set date if available
            if member[3]:
                membership_date = member[3]
                self.update_member_day_entry.set(str(membership_date.day))
                self.update_member_month_entry.set(str(membership_date.month))
                self.update_member_year_entry.set(str(membership_date.year))
            
            self.update_member_status.config(
                text=f"Member '{member[1]}' (Code: {member_code}) loaded for update", 
                foreground="green"
            )
            
        except Exception as e:
            self.update_member_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def update_member(self):
        try:
            member_code = self.update_member_code_entry.get()
            member_name = self.update_member_name_entry.get()
            mobile = self.update_mobile_entry.get()
            address = self.update_address_entry.get()
            
            # Validate inputs
            if not member_code or not member_code.isdigit():
                self.update_member_status.config(text="Member Code must be a valid integer", foreground="red")
                return
                
            if not member_name:
                self.update_member_status.config(text="Member Name is required", foreground="red")
                return
                
            if mobile and not mobile.isdigit():
                self.update_member_status.config(text="Mobile number must contain only digits", foreground="red")
                return
            
            # Check date
            day = self.update_member_day_entry.get()
            month = self.update_member_month_entry.get()
            year = self.update_member_year_entry.get()
            
            if day == "Day" or month == "Month" or year == "Year":
                membership_date = date.today()
            else:
                try:
                    membership_date = date(int(year), int(month), int(day))
                except ValueError:
                    self.update_member_status.config(text="Invalid date", foreground="red")
                    return
            
            # Update member record
            cursor = self.cnx.cursor()
            cursor.execute("""
                UPDATE member 
                SET Mname = %s, mob = %s, dom = %s , adr = %s
                WHERE Mno = %s
            """, (member_name, mobile, membership_date, address, member_code))
            
            self.cnx.commit()
            self.update_member_status.config(text=f"Member '{member_name}' updated successfully!", foreground="green")
            
        except Exception as e:
            self.update_member_status.config(text=f"Error: {str(e)}", foreground="red")
    
    # Issue/Return Book Methods
    def verify_book_for_issue(self):
        try:
            book_code = self.issue_book_code_entry.get()
            
            if not book_code or not book_code.isdigit():
                self.book_verify_label.config(text="Please enter a valid Book Code", foreground="red")
                return False
            
            cursor = self.cnx.cursor()
            
            # Check if book exists
            cursor.execute("SELECT Bname, qty FROM bookrecord WHERE Bno = %s", (book_code,))
            book = cursor.fetchone()
            
            if not book:
                self.book_verify_label.config(text=f"No book found with Book Code: {book_code}", foreground="red")
                return False
            
            # Check if book has available quantity
            if book[1] <= 0:
                self.book_verify_label.config(text=f"Book '{book[0]}' is out of stock", foreground="red")
                return False
            
            # Check if book is already issued
            cursor.execute("SELECT COUNT(*) FROM issue WHERE Bno = %s", (book_code,))
            issue_count = cursor.fetchone()[0]
            
            if issue_count > 0:
                self.book_verify_label.config(text=f"Book '{book[0]}' is already issued", foreground="red")
                return False
            
            self.book_verify_label.config(text=f"Book '{book[0]}' is available for issue", foreground="green")
            return True
            
        except Exception as e:
            self.book_verify_label.config(text=f"Error: {str(e)}", foreground="red")
            return False
    
    def verify_member_for_issue(self):
        try:
            member_code = self.issue_member_code_entry.get()
            
            if not member_code or not member_code.isdigit():
                self.member_verify_label.config(text="Please enter a valid Member Code", foreground="red")
                return False
            
            cursor = self.cnx.cursor()
            
            # Check if member exists
            cursor.execute("SELECT Mname FROM member WHERE Mno = %s", (member_code,))
            member = cursor.fetchone()
            
            if not member:
                self.member_verify_label.config(text=f"No member found with Member Code: {member_code}", foreground="red")
                return False
            
            # Check if member has reached maximum books limit (e.g., 3 books)
            cursor.execute("SELECT COUNT(*) FROM issue WHERE Mno = %s", (member_code,))
            issue_count = cursor.fetchone()[0]
            
            if issue_count >= 3:
                self.member_verify_label.config(
                    text=f"Member '{member[0]}' has already issued maximum allowed books", 
                    foreground="red"
                )
                return False
            
            self.member_verify_label.config(text=f"Member '{member[0]}' verified for book issue", foreground="green")
            return True
            
        except Exception as e:
            self.member_verify_label.config(text=f"Error: {str(e)}", foreground="red")
            return False
    
    def issue_book(self):
        try:
            book_code = self.issue_book_code_entry.get()
            member_code = self.issue_member_code_entry.get()
            
            # Verify book and member
            if not self.verify_book_for_issue() or not self.verify_member_for_issue():
                return
            
            # Check dates
            try:
                issue_day = self.issue_day_entry.get()
                issue_month = self.issue_month_entry.get()
                issue_year = self.issue_year_entry.get()
                issue_date = date(int(issue_year), int(issue_month), int(issue_day))
                
                return_day = self.return_day_entry.get()
                return_month = self.return_month_entry.get()
                return_year = self.return_year_entry.get()
                return_date = date(int(return_year), int(return_month), int(return_day))
                
                # Ensure return date is after issue date
                if return_date <= issue_date:
                    self.issue_status.config(
                        text="Expected return date must be after issue date", 
                        foreground="red"
                    )
                    return
                    
            except ValueError:
                self.issue_status.config(text="Invalid date format", foreground="red")
                return
            
            cursor = self.cnx.cursor()
            
            # Insert issue record
            cursor.execute("INSERT INTO issue (Bno, Mno, doi, dor) VALUES (%s, %s, %s, %s)",
                         (book_code, member_code, issue_date, return_date))
            
            # Update book quantity
            cursor.execute("UPDATE bookrecord SET qty = qty - 1 WHERE Bno = %s", (book_code,))
            
            self.cnx.commit()
            
            # Get book and member details for confirmation message
            cursor.execute("SELECT Bname FROM bookrecord WHERE Bno = %s", (book_code,))
            book_name = cursor.fetchone()[0]
            
            cursor.execute("SELECT Mname FROM member WHERE Mno = %s", (member_code,))
            member_name = cursor.fetchone()[0]
            
            self.issue_status.config(
                text=f"Book '{book_name}' issued to '{member_name}' successfully",
                foreground="green"
            )
            
            # Clear fields
            self.issue_book_code_entry.delete(0, tk.END)
            self.issue_member_code_entry.delete(0, tk.END)
            self.book_verify_label.config(text="")
            self.member_verify_label.config(text="")
            
            # Update the issued books display
            self.display_issued_books()
            
        except Exception as e:
            self.issue_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def verify_issue(self):
        try:
            book_code = self.return_book_code_entry.get()
            member_code = self.return_member_code_entry.get()
            
            if not book_code or not book_code.isdigit() or not member_code or not member_code.isdigit():
                self.issue_verify_label.config(text="Please enter valid Book and Member Codes", foreground="red")
                return False
            
            cursor = self.cnx.cursor()
            
            # Check if book is issued to the member
            cursor.execute("""
                SELECT i.doi, i.dor, b.Bname, m.Mname FROM issue i
                JOIN bookrecord b ON i.Bno = b.Bno
                JOIN member m ON i.Mno = m.Mno
                WHERE i.Bno = %s AND i.Mno = %s
            """, (book_code, member_code))
            
            issue_info = cursor.fetchone()
            
            if not issue_info:
                self.issue_verify_label.config(
                    text=f"No record found of book (Code: {book_code}) issued to member (Code: {member_code})",
                    foreground="red"
                )
                return False
            
            self.issue_verify_label.config(
                text=f"Book '{issue_info[2]}' issued to '{issue_info[3]}' on {issue_info[0]} verified",
                foreground="green"
            )
            return True
            
        except Exception as e:
            self.issue_verify_label.config(text=f"Error: {str(e)}", foreground="red")
            return False
    
    def return_book(self):
        try:
            book_code = self.return_book_code_entry.get()
            member_code = self.return_member_code_entry.get()
            
            # Verify issue record
            if not self.verify_issue():
                return
            
            # Check actual return date
            try:
                return_day = self.actual_return_day_entry.get()
                return_month = self.actual_return_month_entry.get()
                return_year = self.actual_return_year_entry.get()
                actual_return_date = date(int(return_year), int(return_month), int(return_day))
                
            except ValueError:
                self.return_status.config(text="Invalid return date format", foreground="red")
                return
            
            cursor = self.cnx.cursor()
            
            # Get expected return date to calculate fine
            cursor.execute("SELECT dor FROM issue WHERE Bno = %s AND Mno = %s", (book_code, member_code))
            expected_return_date = cursor.fetchone()[0]
            
            # Calculate fine (if returned late - Rs. 10 per day)
            fine = 0
            if actual_return_date > expected_return_date:
                days_late = (actual_return_date - expected_return_date).days
                fine = days_late * 10
            
            # Delete issue record
            cursor.execute("DELETE FROM issue WHERE Bno = %s AND Mno = %s", (book_code, member_code))
            
            # Update book quantity
            cursor.execute("UPDATE bookrecord SET qty = qty + 1 WHERE Bno = %s", (book_code,))
            
            self.cnx.commit()
            
            # Get book and member details for confirmation message
            cursor.execute("SELECT Bname FROM bookrecord WHERE Bno = %s", (book_code,))
            book_name = cursor.fetchone()[0]
            
            cursor.execute("SELECT Mname FROM member WHERE Mno = %s", (member_code,))
            member_name = cursor.fetchone()[0]
            
            if fine > 0:
                self.return_status.config(
                    text=f"Book '{book_name}' returned by '{member_name}'. Fine: Rs. {fine} (Late by {days_late} days)",
                    foreground="blue"
                )
            else:
                self.return_status.config(
                    text=f"Book '{book_name}' returned by '{member_name}' successfully. No fine.",
                    foreground="green"
                )
            
            # Clear fields
            self.return_book_code_entry.delete(0, tk.END)
            self.return_member_code_entry.delete(0, tk.END)
            self.issue_verify_label.config(text="")
            
            # Update the issued books display
            self.display_issued_books()
            
        except Exception as e:
            self.return_status.config(text=f"Error: {str(e)}", foreground="red")
    
    def display_issued_books(self):
        try:
            cursor = self.cnx.cursor()
            cursor.execute("""
                SELECT i.Bno, b.Bname, i.Mno, m.Mname, i.doi, i.dor
                FROM issue i
                JOIN bookrecord b ON i.Bno = b.Bno
                JOIN member m ON i.Mno = m.Mno
                ORDER BY i.doi
            """)
            
            issues = cursor.fetchall()
            
            self.issued_books_display.delete(1.0, tk.END)
            
            if not issues:
                self.issued_books_display.insert(tk.END, "No books are currently issued.")
                return
            
            # Display column headers
            headers = "Book Code | Book Name | Member Code | Member Name | Issue Date | Expected Return Date\n"
            self.issued_books_display.insert(tk.END, headers)
            self.issued_books_display.insert(tk.END, "-" * 120 + "\n")
            
            # Display issue data
            for issue in issues:
                today = date.today()
                status = ""
                
                # Check if book is overdue
                if issue[5] < today:
                    days_overdue = (today - issue[5]).days
                    status = f" - OVERDUE by {days_overdue} days"
                
                issue_info = f"{issue[0]} | {issue[1]} | {issue[2]} | {issue[3]} | {issue[4]} | {issue[5]}{status}\n"
                self.issued_books_display.insert(tk.END, issue_info)
                
        except Exception as e:
            self.issued_books_display.delete(1.0, tk.END)
            self.issued_books_display.insert(tk.END, f"Error: {str(e)}")
    
    # Helper Methods
    def is_valid_decimal(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def set_background_image(self, image_path):
        try:
            # Create a PhotoImage object
            background_image = tk.PhotoImage(file=image_path)
            
            # Create a label with the image
            background_label = tk.Label(self.root, image=background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Keep a reference to prevent garbage collection
            background_label.image = background_image
            
        except Exception as e:
            print(f"Error loading background image: {str(e)}")

    def run(self):
        self.root.mainloop()


# Main application startup
if __name__ == "__main__":
    try:
        # Initialize application
        root = tk.Tk()
        app = LibraryManagementSystem(root)
        
        # Uncomment the following line when you have the background image
        app.set_background_image("D:\Downloads\abc.jpg")
        
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {str(e)}")
    
                

