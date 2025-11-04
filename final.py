import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
import os
import json
from datetime import datetime, timedelta
import time
import tkinter as tk
import calendar as cal
import uuid
import winsound # Added for sound functionality

# Set appearance mode for light theme
ctk.set_appearance_mode("light")

# --- REVISED COLOR PALETTE FOR MUTED HARMONY (BLUE THEME) ---
# Main background and general container colors
BG_COLOR = "#E0F2F7"           # A light, calming blue (similar to lightblue in CSS)
CARD_BG_COLOR = "#C6E8F3"      # A slightly deeper, but still light, blue for card backgrounds
                               # This provides a subtle differentiation from the main BG_COLOR
# Text colors
TEXT_COLOR = "#334155"          # Darker gray for body text, better contrast on light blue
HEADER_TEXT_COLOR = "#1a202c"   # Even darker for headings and navigation

# Button colors (keeping them dark for strong contrast)
BUTTON_BG_COLOR = "#111827"     # Black-ish buttons
BUTTON_TEXT_COLOR = "#ffffff"   # White text on buttons
BUTTON_HOVER_COLOR = "#374151"  # Darker hover color

# Shadow color (adjusted to blend with blue tones)
SHADOW_COLOR = "#7F9FB7"        # A deeper, more prominent blue-gray for shadows

# Accent colors for specific features (more muted and harmonious)
ACCENT_COLOR_1 = "#66BB6A" # Soft Green (e.g., for positive/completion)
ACCENT_COLOR_2 = "#64B5F6" # Muted Sky Blue (e.g., for info/active)
ACCENT_COLOR_3 = "#FFA726" # Soft Orange (e.g., for pending/attention)
ACCENT_COLOR_4 = "#EF5350" # Muted Red (e.g., for warnings/errors)
ACCENT_COLOR_5 = "#9575CD" # Muted Purple (e.g., for unique sections)
ACCENT_COLOR_6 = "#FFD54F" # Soft Gold/Yellow (new addition, good for highlighting)


# Font definitions reflecting hierarchy
FONT_LARGE = ("Inter", 48, "bold")
FONT_MEDIUM = ("Inter", 22, "bold")
FONT_BODY = ("Inter", 16)
FONT_BUTTON = ("Inter", 16, "bold")
FONT_SMALL_BOLD = ("Inter", 14, "bold")
FONT_SMALL = ("Inter", 14)


# Window sizing constants
CONTAINER_MAX_WIDTH = 1200
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 700

class PersistentData:
    """Class to handle JSON-based persistent storage for *all* users' data of a specific type."""
    def __init__(self, filepath):
        self.filepath = filepath
        # data will be a dictionary where keys are usernames
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except FileNotFoundError:
                self.data = {} # File not found, start with empty data
            except json.JSONDecodeError:
                messagebox.showwarning("Data Corrupted", f"The data file {self.filepath} is corrupted and cannot be loaded. Starting with empty data.", icon="warning")
                self.data = {} # JSON decode error, start with empty data
            except Exception as e:
                messagebox.showerror("Error Loading Data", f"An unexpected error occurred while loading {self.filepath}: {e}", icon="error")
                self.data = {}
        else:
            self.data = {}

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                # The default=str is crucial for serializing datetime objects if they were in the data directly
                # However, for this profile system, we'll ensure only JSON-serializable types are stored
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving {self.filepath}: {e}")
            messagebox.showerror("Save Error", f"Failed to save data to {self.filepath}: {e}", icon="error")

    def get_user_data(self, username, default=None):
        return self.data.get(username, default)

    def set_user_data(self, username, value):
        self.data[username] = value
        self.save()

class StudentGuideApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Student Guide - Default Theme") # Reverted title
        self.app.geometry("1920x1080") # Adjusted to 1920x1080
        self.app.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.app.configure(fg_color=BG_COLOR)

        # Centered container frame with padding
        self.container = ctk.CTkFrame(self.app, fg_color=BG_COLOR)
        self.container.pack(expand=True, padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)

        # Header and subtitle labels
        header = ctk.CTkLabel(self.container, text="🎓 Welcome to EDUMIND" \
        "",
                                 font=FONT_LARGE, text_color=HEADER_TEXT_COLOR)
        header.grid(row=0, column=0, pady=(0, 20), sticky="ew")

        subheader = ctk.CTkLabel(self.container, text="Login or Register to continue",
                                 font=FONT_MEDIUM, text_color=TEXT_COLOR)
        subheader.grid(row=1, column=0, pady=(0, 36), sticky="ew")

        # Username and Password Entries
        self.username_entry = ctk.CTkEntry(self.container, placeholder_text="Username",
                                             width=400, fg_color="#f3f4f6", # Reverted entries to slightly off-white
                                             text_color=TEXT_COLOR, font=FONT_BODY,
                                             corner_radius=10, border_color=SHADOW_COLOR,
                                             border_width=1)
        self.username_entry.grid(row=2, column=0, pady=(0, 20), sticky="ew")

        self.password_entry = ctk.CTkEntry(self.container, placeholder_text="Password", show="*",
                                             width=400, fg_color="#f3f4f6", # Reverted entries to slightly off-white
                                             text_color=TEXT_COLOR, font=FONT_BODY,
                                             corner_radius=10, border_color=SHADOW_COLOR,
                                             border_width=1)
        self.password_entry.grid(row=3, column=0, pady=(0, 36), sticky="ew")

        # Login Button
        self.login_button = ctk.CTkButton(self.container, text="Login", command=self.login,
                                             width=400, height=50,
                                             fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                             text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON,
                                             corner_radius=10)
        self.login_button.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        # Register Button
        self.register_button = ctk.CTkButton(self.container, text="Register", command=self.open_register_window,
                                             width=400, height=50,
                                             fg_color=ACCENT_COLOR_2, hover_color="#42A5F5", # Reverted hover
                                             text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON,
                                             corner_radius=10)
        self.register_button.grid(row=5, column=0, sticky="ew")


        # Prepare persistent data files and folders
        self.users_file = "users.json" # Stores user details
        self.tasks_file = "tasks.json"
        self.reminders_file = "reminders.json"
        self.moods_file = "moods.json" # Original mood tracking
        self.daily_checkins_file = "daily_checkins.json" # Still here, but not used by Wellness Panel anymore
        self.wellness_goals_file = "wellness_goals.json" # Still here, but not used by Wellness Panel anymore
        self.progress_file = "progress.json"
        self.plans_file = "plans.json"
        self.doubts_file = "doubts.json"
        self.timer_history_file = "timer_history.json" # *** ADDED for timer history

        self.doubt_folder = "saved_doubts"
        os.makedirs(self.doubt_folder, exist_ok=True)

        # Each PersistentData instance now holds data for *all* users for its specific type
        self.users_data = PersistentData(self.users_file)
        # Initialize users_data if it's empty on first run
        if not self.users_data.data:
            # Example default user with new data structure
            default_user_details = {
                "password": "password123",
                "name": "Default User",
                "email": "default@example.com",
                "course": "CSE",
                "section": "A"
            }
            self.users_data.set_user_data("default_user", default_user_details)
            self.users_data.save()

        self.tasks_data = PersistentData(self.tasks_file)
        self.reminders_data = PersistentData(self.reminders_file)
        self.moods_data = PersistentData(self.moods_file) 
        self.daily_checkins_data = PersistentData(self.daily_checkins_file) # Will not be explicitly used in Wellness Panel
        self.wellness_goals_data = PersistentData(self.wellness_goals_file) # Will not be explicitly used in Wellness Panel
        self.timer_history_data = PersistentData(self.timer_history_file) # *** ADDED for timer history

        self.progress_data = PersistentData(self.progress_file)
        self.plans_data = PersistentData(self.plans_file)
        self.doubts_data = PersistentData(self.doubts_file)

        self.current_user = None

        # Pomodoro Timer variables
        self._pomodoro_timer_window = None
        self._timer_running = False
        self._pomodoro_time_left = 0
        self._pomodoro_state = "stopped"
        self._work_minutes = 25
        self._break_minutes = 5
        self._timer_thread = None
        self._pomodoro_timer_id = None
        self.pomodoro_time_label = None
        self.timer_history_scroll_frame = None # *** ADDED
        self._current_timer_duration_minutes = 0 # *** ADDED

        # Reminder System variables
        self._reminder_thread = None
        self._reminder_thread_running = False
        self._reminder_check_interval = 1000
        self.active_reminders = {}

        self.app.mainloop()

    def open_register_window(self):
        register_win = ctk.CTkToplevel(self.app)
        register_win.title("Register New User")
        register_win.geometry("450x650") # Increased height for new fields
        register_win.configure(fg_color=BG_COLOR)
        register_win.transient(self.app)
        register_win.grab_set()

        frame = ctk.CTkFrame(register_win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)
        frame.grid_columnconfigure((0, 1), weight=1) # Configure both columns to have weight

        ctk.CTkLabel(frame, text="✨ Register", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).grid(row=0, column=0, columnspan=2, pady=(20, 15))

        # --- REORDERED AND UPDATED REGISTRATION FIELDS ---

        # Full Name
        ctk.CTkLabel(frame, text="Full Name:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.new_name_entry = ctk.CTkEntry(frame, placeholder_text="Enter your full name",
                                             width=300, fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY,
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.new_name_entry.grid(row=2, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        # Username
        ctk.CTkLabel(frame, text="Username:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.new_username_entry = ctk.CTkEntry(frame, placeholder_text="Choose a username",
                                             width=300, fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY,
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.new_username_entry.grid(row=4, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        # Password
        ctk.CTkLabel(frame, text="Password:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.new_password_entry = ctk.CTkEntry(frame, placeholder_text="Choose a password", show="*",
                                             width=300, fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY,
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.new_password_entry.grid(row=6, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        
        # Course and Section (Side-by-side)
        ctk.CTkLabel(frame, text="Course:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=7, column=0, sticky="w", pady=(0, 5))
        self.course_optionmenu = ctk.CTkOptionMenu(frame, values=["CSE", "CSM"],
                                                         command=self.update_sections, # Add command here
                                                         fg_color=BUTTON_BG_COLOR, button_color=BUTTON_BG_COLOR,
                                                         text_color=BUTTON_TEXT_COLOR,
                                                         dropdown_fg_color=BUTTON_HOVER_COLOR)
        self.course_optionmenu.grid(row=8, column=0, pady=(0, 15), sticky="ew", padx=(0, 5))

        ctk.CTkLabel(frame, text="Section:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=7, column=1, sticky="w", padx=(5,0), pady=(0, 5))
        # Initialize with CSE sections by default
        self.section_optionmenu = ctk.CTkOptionMenu(frame, values=["A", "B", "C", "D", "E", "F"],
                                                         fg_color=BUTTON_BG_COLOR, button_color=BUTTON_BG_COLOR,
                                                         text_color=BUTTON_TEXT_COLOR,
                                                         dropdown_fg_color=BUTTON_HOVER_COLOR)
        self.section_optionmenu.grid(row=8, column=1, pady=(0, 15), sticky="ew", padx=(5, 0))

        # Email ID
        ctk.CTkLabel(frame, text="Email ID:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=9, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.new_email_entry = ctk.CTkEntry(frame, placeholder_text="Enter your email address",
                                             width=300, fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY,
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.new_email_entry.grid(row=10, column=0, columnspan=2, pady=(0, 20), sticky="ew")


        # Create Account Button
        ctk.CTkButton(frame, text="Create Account", command=self.register_user,
                                 width=200, height=45, fg_color=ACCENT_COLOR_1, hover_color="#5cb85c",
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).grid(row=11, column=0, columnspan=2, pady=10)
        
        self.register_win = register_win # Store reference to the registration window

    def update_sections(self, course):
        """Updates the section dropdown based on the selected course."""
        if course == "CSE":
            sections = ["A", "B", "C", "D", "E", "F"]
        elif course == "CSM":
            sections = ["A", "B"]
        else:
            sections = [] # Should not happen
        
        self.section_optionmenu.configure(values=sections)
        self.section_optionmenu.set(sections[0] if sections else "")

    def register_user(self):
        # Reordered to match the form layout
        new_name = self.new_name_entry.get().strip()
        new_user = self.new_username_entry.get().strip()
        new_pwd = self.new_password_entry.get().strip()
        course = self.course_optionmenu.get()
        section = self.section_optionmenu.get()
        new_email = self.new_email_entry.get().strip()

        if not all([new_name, new_user, new_pwd, new_email]):
            messagebox.showerror("Registration Error", "Please fill in all required fields (Name, Username, Password, Email).", icon="error")
            return
        
        # Check if username already exists
        if new_user in self.users_data.data:
            messagebox.showerror("Registration Error", "Username already exists. Please choose a different one.", icon="error")
            return

        # Store all user details in a dictionary
        user_details = {
            "password": new_pwd, # Storing plaintext passwords. In a real app, use hashing!
            "name": new_name,
            "email": new_email,
            "course": course,
            "section": section
        }
        self.users_data.set_user_data(new_user, user_details)
        
        messagebox.showinfo("Registration Success", f"Account '{new_user}' created successfully! You can now log in.", icon="info")
        self.register_win.destroy() # Close registration window
        
        # Optionally pre-fill login fields
        self.username_entry.delete(0, "end")
        self.username_entry.insert(0, new_user)
        self.password_entry.delete(0, "end")

    def login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        # UPDATED LOGIN LOGIC for new data structure
        user_data = self.users_data.data.get(user)
        if user_data and user_data.get("password") == pwd:
            self.current_user = user
            self.open_dashboard()
            if not self._reminder_thread_running:
                self.start_reminder_checker() # Start reminder checker on login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!", icon="error")

    def open_dashboard(self):
        self.app.withdraw()

        self.dash = ctk.CTkToplevel(self.app)
        self.dash.geometry("1920x1080") # Adjusted to 1920x1080
        self.dash.minsize(800, 600)
        
        # Get user's name to display in the title
        user_data = self.users_data.get_user_data(self.current_user)
        user_display_name = user_data.get("name", self.current_user) if user_data else self.current_user
        self.dash.title(f"Welcome, {user_display_name}!")
        
        self.dash.configure(fg_color=BG_COLOR)

        # --- Integration of Tkinter Menu Bar ---
        self.menubar = tk.Menu(self.dash)
        self.dash.config(menu=self.menubar)

        # File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.exit_app)

        # Features Menu (to duplicate dashboard functionality)
        features_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Features", menu=features_menu)
        features_menu.add_command(label="Smart Task Tracker", command=self.task_tracker)
        features_menu.add_command(label="Subject-wise Planner", command=self.subject_planner)
        features_menu.add_command(label="Doubt Notebook", command=self.doubt_notebook)
        features_menu.add_command(label="Pomodoro Timer", command=self.pomodoro_timer)
        features_menu.add_command(label="Study Progress Tracker", command=self.study_progress)
        features_menu.add_command(label="Wellness Panel", command=self.wellness_panel)
        features_menu.add_command(label="Syllabus_manager", command=self.syllabus_manager)
        features_menu.add_command(label="View Uploaded Syllabus", command=self.view_uploaded_syllabus)
        features_menu.add_command(label="Calendar View", command=self.calendar_view)
        features_menu.add_command(label="Reminder System", command=self.reminder_system)
        
        # Help Menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.help_about)
        # ----------------------------------------

        # Header
        header_frame = ctk.CTkFrame(self.dash, fg_color=BG_COLOR, corner_radius=0, height=60)
        header_frame.pack(side="top", fill="x")

        ctk.CTkLabel(header_frame, text="EduMind Dashboard",
                                 font=FONT_LARGE, text_color=HEADER_TEXT_COLOR).pack(side="left", padx=40, pady=10)

        logout_button = ctk.CTkButton(header_frame, text="Logout", width=100, height=40,
                                         fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                         text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON,
                                         corner_radius=10, command=self.logout)
        logout_button.pack(side="right", padx=40, pady=10)

        # --- MODIFICATION: Replaced CTkFrame with CTkScrollableFrame ---
        # Scrollable container for features
        scrollable_container = ctk.CTkScrollableFrame(self.dash, fg_color=BG_COLOR, corner_radius=10)
        scrollable_container.pack(fill="both", expand=True, padx=40, pady=30)
        scrollable_container.grid_columnconfigure((0,1,2), weight=1, uniform="cols")
        # --- END MODIFICATION ---

        # --- REVERTED FEATURES LIST TO ORIGINAL BLUE ACCENT COLORS ---
        features = [
            ("Profile Section", self.profile_section, "👤", ACCENT_COLOR_5), # New Profile Card
            ("Smart Task Tracker", self.task_tracker, "📝", ACCENT_COLOR_2), # Muted Sky Blue
            ("Subject-wise Planner", self.subject_planner, "📚", ACCENT_COLOR_5), # Muted Purple
            ("Doubt Notebook", self.doubt_notebook, "❓", ACCENT_COLOR_4), # Muted Red
            ("Pomodoro Timer", self.pomodoro_timer, "⏰", ACCENT_COLOR_1), # Soft Green
            ("Study Progress Tracker", self.study_progress, "📈", ACCENT_COLOR_3), # Soft Orange
            ("Wellness Panel", self.wellness_panel, "🧘", ACCENT_COLOR_6), # Soft Gold/Yellow
            ("Syllabus Manager", self.syllabus_manager, "📘", ACCENT_COLOR_5), # Muted Teal
            ("View Uploaded Syllabus", self.view_uploaded_syllabus, "📗", ACCENT_COLOR_3), # Aqua Blue
            ("Calendar View", self.calendar_view, "📅", ACCENT_COLOR_2), # Muted Sky Blue (reused for balance)
            ("Reminder System", self.reminder_system, "🔔", ACCENT_COLOR_4), # Muted Red (reused for balance)
            ("Help & About", self.help_about, "ℹ️", CARD_BG_COLOR) # Use the general card background for "Help"
        ]

        for idx, (name, cmd, icon, card_color) in enumerate(features):
            # --- MODIFICATION: Changed parent from 'container' to 'scrollable_container' ---
            card = ctk.CTkFrame(scrollable_container, fg_color=card_color,
                                 corner_radius=12, border_width=1, border_color=SHADOW_COLOR,
                                 height=140, width=280)
            # --- END MODIFICATION ---
            card.grid(row=idx // 3, column=idx % 3, padx=25, pady=20, sticky="nsew")
            card.grid_propagate(False)

            # Determine text color based on the card's background color for optimal contrast
            # Reverted logic for blue tones
            if card_color in [ACCENT_COLOR_4, ACCENT_COLOR_5, BUTTON_BG_COLOR]: # Muted Red, Muted Purple, Dark Button
                text_on_card_color = BUTTON_TEXT_COLOR # White
            else: # Soft Green, Muted Sky Blue, Soft Orange, Soft Gold/Yellow, CARD_BG_COLOR
                text_on_card_color = HEADER_TEXT_COLOR # Dark Gray

            ctk.CTkLabel(card, text=f"{icon} {name}",
                                font=("Inter", 18, "bold"),
                                 text_color=text_on_card_color).pack(pady=(25, 10))

            ctk.CTkButton(card, text="Open", command=cmd, width=130,
                                 fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).pack(pady=(0,10))

        self.dash.protocol("WM_DELETE_WINDOW", self.exit_app)

    def logout(self):
        if hasattr(self, 'dash') and self.dash.winfo_exists():
            self.dash.destroy()
        self.app.deiconify() # Show the login window again
        self.stop_reminder_checker() # Stop reminder checker on logout
        self.stop_pomodoro_timer(stop_thread=True) # Ensure pomodoro thread is stopped
        self.current_user = None # Clear current user on logout

    def exit_app(self):
        if hasattr(self, 'dash') and self.dash.winfo_exists():
            self.dash.destroy()
        self.stop_reminder_checker() # Ensure reminder thread is stopped
        self.stop_pomodoro_timer(stop_thread=True) # Ensure pomodoro thread is stopped
        self.app.destroy()

    def help_about(self):
        messagebox.showinfo("Help & About",
                             "Student  app following Default design guidelines.\n"
                             "Manage your tasks, study plans, reminders, and wellness with ease,syllabus manager.\n\n"
                             "Developed with ❤️ using CustomTkinter.",
                             icon="info")
    def profile_section(self):
        user_data = self.users_data.get_user_data(self.current_user, {})
        if not user_data:
            messagebox.showerror("Error", "User data not found!", icon="error")
            return

        win = ctk.CTkToplevel(self.dash)
        win.title(f"Profile: {self.current_user}")
        win.geometry("500x600")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="👤 User Profile", font=("Inter", 28, "bold"),
                                 text_color=HEADER_TEXT_COLOR).grid(row=0, column=0, pady=(20, 15), sticky="n")
        
        # Current Username (read-only)
        ctk.CTkLabel(frame, text=f"Username: {self.current_user}", text_color=TEXT_COLOR, font=FONT_MEDIUM).grid(row=1, column=0, sticky="w", padx=20, pady=(10, 20))

        # Full Name Entry
        ctk.CTkLabel(frame, text="Full Name:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=0, sticky="w", padx=20, pady=(5, 5))
        self.profile_name_entry = ctk.CTkEntry(frame, width=400, fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.profile_name_entry.insert(0, user_data.get("name", ""))
        self.profile_name_entry.grid(row=3, column=0, pady=(0, 15), padx=20, sticky="ew")

        # Email Entry
        ctk.CTkLabel(frame, text="Email ID:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=4, column=0, sticky="w", padx=20, pady=(5, 5))
        self.profile_email_entry = ctk.CTkEntry(frame, width=400, fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.profile_email_entry.insert(0, user_data.get("email", ""))
        self.profile_email_entry.grid(row=5, column=0, pady=(0, 15), padx=20, sticky="ew")

        # Course and Section Display (Read-Only as they are foundational)
        course_text = user_data.get("course", "N/A")
        section_text = user_data.get("section", "N/A")
        
        ctk.CTkLabel(frame, text="Course:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=6, column=0, sticky="w", padx=20, pady=(5, 5))
        ctk.CTkLabel(frame, text=course_text, text_color=HEADER_TEXT_COLOR, font=FONT_BODY).grid(row=7, column=0, sticky="w", padx=20, pady=(0, 15))

        ctk.CTkLabel(frame, text="Section:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=8, column=0, sticky="w", padx=20, pady=(5, 5))
        ctk.CTkLabel(frame, text=section_text, text_color=HEADER_TEXT_COLOR, font=FONT_BODY).grid(row=9, column=0, sticky="w", padx=20, pady=(0, 20))
        
        # Save Button
        ctk.CTkButton(frame, text="Update Profile", command=lambda: self.update_profile(win),
                                 width=200, height=45, fg_color=ACCENT_COLOR_1, hover_color="#5cb85c",
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).grid(row=10, column=0, pady=10)

    def update_profile(self, win):
        """Saves updated profile information (Name, Email) to the users.json file."""
        new_name = self.profile_name_entry.get().strip()
        new_email = self.profile_email_entry.get().strip()
        
        if not new_name or not new_email:
            messagebox.showerror("Update Error", "Full Name and Email cannot be empty.", icon="error")
            return
        
        current_data = self.users_data.get_user_data(self.current_user, {})
        
        # Update only the editable fields
        current_data["name"] = new_name
        current_data["email"] = new_email
        
        # Save back to the persistent data
        self.users_data.set_user_data(self.current_user, current_data)
        
        messagebox.showinfo("Success", "Your profile information has been updated!", icon="info")
        win.destroy()

    # --- Feature Implementations ---

    # --- Smart Task Tracker ---
    def task_tracker(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Smart Task Tracker")
        win.geometry("650x600")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1) # Ensure central column expands
        frame.grid_rowconfigure(2, weight=1) # Make the task list row expandable


        ctk.CTkLabel(frame, text="📝 Smart Task Tracker", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).grid(row=0, column=0, pady=(20, 15), sticky="n")

        input_frame = ctk.CTkFrame(frame, fg_color="transparent") # Use transparent to blend with parent
        input_frame.grid(row=1, column=0, pady=10, padx=15, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(input_frame, text="Task description:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., Complete Math Homework",
                                         fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY,
                                         corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.task_entry.grid(row=1, column=0, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="Due date (YYYY-MM-DD) (Optional):", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.due_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 2025-12-31",
                                         fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY,
                                         corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.due_entry.grid(row=3, column=0, pady=(0, 15), sticky="ew")

        ctk.CTkButton(input_frame, text="Add Task", fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.add_task).grid(row=4, column=0, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Your Tasks:", font=("Inter", 18, "bold"), text_color=HEADER_TEXT_COLOR).grid(row=2, column=0, pady=(20, 10), sticky="s") # Sticky "s" for south

        list_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        list_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=(0, 10)) # Occupy an expandable row
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        self.task_scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color=CARD_BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        self.task_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.task_scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Button Frame for task actions (Correctly placed using grid) ---
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, pady=(5, 15), padx=15, sticky="ew") # Placed in its own row
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(btn_frame, text="Mark Selected as Complete", fg_color=ACCENT_COLOR_1, hover_color="#5cb85c",
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.mark_task_complete).grid(row=0, column=0, padx=5, sticky="ew")
        
        ctk.CTkButton(btn_frame, text="Revert to Pending", fg_color=ACCENT_COLOR_3, hover_color="#f0ad4e",
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.revert_task_to_pending).grid(row=0, column=1, padx=5, sticky="ew")

        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color=ACCENT_COLOR_4, hover_color="#dc3545",
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.delete_selected_tasks).grid(row=0, column=2, padx=5, sticky="ew")
        # ----------------------------------------------------------------------

        self.refresh_task_list()

    def add_task(self):
        task = self.task_entry.get().strip()
        due = self.due_entry.get().strip()
        if not task:
            messagebox.showerror("Input Error", "Task description cannot be empty.", icon="error")
            return
        if due:
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Input Error", "Due date must be in YYYY-MM-DD format.", icon="error")
                return

        tasks = self.tasks_data.get_user_data(self.current_user, [])
        tasks.append({"task": task, "due_date": due if due else "No Due Date", "status": "Pending", "created_at": datetime.now().isoformat()})
        self.tasks_data.set_user_data(self.current_user, tasks)
        self.task_entry.delete(0, "end")
        self.due_entry.delete(0, "end")
        self.refresh_task_list()
        messagebox.showinfo("Success", "Task added successfully!", icon="info")

    def refresh_task_list(self):
        for widget in self.task_scroll_frame.winfo_children():
            widget.destroy()

        tasks = self.tasks_data.get_user_data(self.current_user, [])
        if not tasks:
            ctk.CTkLabel(self.task_scroll_frame, text="No tasks added yet! Start by adding a new task.", text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=20)
            return

        for i, task_data in enumerate(tasks):
            task_frame = ctk.CTkFrame(self.task_scroll_frame, fg_color=BG_COLOR, corner_radius=8,
                                      border_width=1, border_color=SHADOW_COLOR)
            task_frame.pack(fill="x", pady=5, padx=5)
            task_frame.grid_columnconfigure(1, weight=1)

            status_color = ACCENT_COLOR_1 if task_data['status'] == "Completed" else ACCENT_COLOR_3 if task_data['status'] == "Pending" else TEXT_COLOR

            checkbox = ctk.CTkCheckBox(task_frame, text="", fg_color=BUTTON_BG_COLOR,
                                         hover_color=BUTTON_HOVER_COLOR,
                                         checkmark_color=BUTTON_TEXT_COLOR,
                                         border_color=BUTTON_BG_COLOR, border_width=2,
                                         command=lambda idx=i: self.toggle_task_selection(idx))
            checkbox.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
            if task_data.get('selected_for_action', False):
                checkbox.select()
            else:
                checkbox.deselect()

            task_text = ctk.CTkLabel(task_frame, text=f"{task_data['task']} (Due: {task_data['due_date']})",
                                     font=FONT_BODY, text_color=TEXT_COLOR)
            if task_data['status'] == "Completed":
                # Apply strikethrough and gray out text for completed tasks
                task_text.configure(text_color="gray", font=(FONT_BODY[0], FONT_BODY[1], "overstrike"))
            else:
                # Ensure normal text color and font for pending tasks
                task_text.configure(text_color=TEXT_COLOR, font=FONT_BODY)
            task_text.grid(row=0, column=1, sticky="w", padx=(0, 10))

            status_label = ctk.CTkLabel(task_frame, text=task_data['status'],
                                         font=FONT_SMALL_BOLD, text_color=status_color)
            status_label.grid(row=0, column=2, padx=(0, 10), sticky="e")

    def toggle_task_selection(self, index):
        tasks = self.tasks_data.get_user_data(self.current_user, [])
        if 0 <= index < len(tasks):
            tasks[index]['selected_for_action'] = not tasks[index].get('selected_for_action', False)
            self.tasks_data.set_user_data(self.current_user, tasks)
            self.refresh_task_list() # Re-render to update checkbox state

    def delete_selected_tasks(self):
        tasks = self.tasks_data.get_user_data(self.current_user, [])
        tasks_to_keep = []
        deleted_count = 0
        for task in tasks:
            if not task.get('selected_for_action', False):
                tasks_to_keep.append(task)
            else:
                deleted_count += 1

        if deleted_count == 0:
            messagebox.showwarning("No Selection", "Please select tasks to delete.", icon="warning")
            return

        self.tasks_data.set_user_data(self.current_user, tasks_to_keep)
        self.refresh_task_list()
        messagebox.showinfo("Success", f"{deleted_count} task(s) deleted successfully!", icon="info")

    def mark_task_complete(self):
        tasks = self.tasks_data.get_user_data(self.current_user, [])
        marked_count = 0
        for task in tasks:
            if task.get('selected_for_action', False) and task['status'] == "Pending":
                task['status'] = "Completed"
                task['selected_for_action'] = False # Deselect after action
                marked_count += 1
            elif task.get('selected_for_action', False) and task['status'] == "Completed":
                # If already completed and selected, just deselect it
                task['selected_for_action'] = False
        
        if marked_count == 0:
            messagebox.showwarning("No Pending Tasks Selected", "Please select pending tasks to mark as complete.", icon="warning")
            return

        self.tasks_data.set_user_data(self.current_user, tasks)
        self.refresh_task_list()
        messagebox.showinfo("Success", f"{marked_count} task(s) marked as complete!", icon="info")

    def revert_task_to_pending(self):
        """Reverts selected completed tasks back to 'Pending' status."""
        tasks = self.tasks_data.get_user_data(self.current_user, [])
        reverted_count = 0
        for task in tasks:
            if task.get('selected_for_action', False) and task['status'] == "Completed":
                task['status'] = "Pending"
                task['selected_for_action'] = False # Deselect after action
                reverted_count += 1
            elif task.get('selected_for_action', False) and task['status'] == "Pending":
                # If already pending and selected, just deselect it
                task['selected_for_action'] = False
        
        if reverted_count == 0:
            messagebox.showwarning("No Completed Tasks Selected", "Please select completed tasks to revert to pending.", icon="warning")
            return

        self.tasks_data.set_user_data(self.current_user, tasks)
        self.refresh_task_list()
        messagebox.showinfo("Success", f"{reverted_count} task(s) reverted to pending!", icon="info")


    # --- Subject-wise Planner (Existing) ---
    def subject_planner(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Subject-wise Planner")
        win.geometry("700x650")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)

        ctk.CTkLabel(frame, text="📚 Subject-wise Planner", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).pack(pady=(20, 15))

        input_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        input_frame.pack(pady=10, padx=15, fill="x")
        input_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(input_frame, text="Subject:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=0, column=0, sticky="w", padx=(0,10), pady=(0, 5))
        self.subject_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., Mathematics",
                                             fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.subject_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="Topic/Chapter:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=0, sticky="w", padx=(0,10), pady=(0, 5))
        self.topic_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., Algebra - Quadratic Equations",
                                             fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.topic_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="Due Date (YYYY-MM-DD):", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=4, column=0, sticky="w", padx=(0,10), pady=(0, 5))
        self.plan_due_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 2025-06-20",
                                             fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.plan_due_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15))

        self.plan_status_optionmenu = ctk.CTkOptionMenu(input_frame, values=["Planned", "In Progress", "Completed"],
                                                         fg_color=BUTTON_BG_COLOR, button_color=BUTTON_BG_COLOR,
                                                         text_color=BUTTON_TEXT_COLOR, # Ensure text is visible
                                                         dropdown_fg_color=BUTTON_HOVER_COLOR,
                                                         dropdown_hover_color=SHADOW_COLOR)
        self.plan_status_optionmenu.set("Planned")
        self.plan_status_optionmenu.grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(0, 15))


        ctk.CTkButton(input_frame, text="Add Study Plan", fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.add_study_plan).grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Your Study Plans:", font=("Inter", 18, "bold"), text_color=HEADER_TEXT_COLOR).pack(pady=(20, 10))

        list_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        self.plan_scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color=CARD_BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        self.plan_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.plan_scroll_frame.grid_columnconfigure(0, weight=1)

        btn_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        btn_frame.pack(pady=(5, 15), fill="x", padx=15)
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="Update Selected Plan Status", fg_color=ACCENT_COLOR_2, hover_color="#42A5F5", # Reverted hover
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.update_selected_plan_status).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="Delete Selected Plan", fg_color=ACCENT_COLOR_4, hover_color="#dc3545", # Reverted hover
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.delete_selected_plans).grid(row=0, column=1, padx=5, sticky="ew")

        self.refresh_study_plan_list()

    def add_study_plan(self):
        subject = self.subject_entry.get().strip()
        topic = self.topic_entry.get().strip()
        due_date = self.plan_due_entry.get().strip()
        status = self.plan_status_optionmenu.get()

        if not subject or not topic:
            messagebox.showerror("Input Error", "Subject and Topic cannot be empty.", icon="error")
            return
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Input Error", "Due date must be in YYYY-MM-DD format.", icon="error")
                return

        plans = self.plans_data.get_user_data(self.current_user, [])
        plans.append({"subject": subject, "topic": topic, "due_date": due_date, "status": status})
        self.plans_data.set_user_data(self.current_user, plans)
        self.subject_entry.delete(0, "end")
        self.topic_entry.delete(0, "end")
        self.plan_due_entry.delete(0, "end")
        self.plan_status_optionmenu.set("Planned") # Reset status
        self.refresh_study_plan_list()
        messagebox.showinfo("Success", "Study plan added successfully!", icon="info")

    def refresh_study_plan_list(self):
        for widget in self.plan_scroll_frame.winfo_children():
            widget.destroy()

        plans = self.plans_data.get_user_data(self.current_user, [])
        if not plans:
            ctk.CTkLabel(self.plan_scroll_frame, text="No study plans added yet! Start planning your subjects.", text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=20)
            return

        for i, plan_data in enumerate(plans):
            plan_frame = ctk.CTkFrame(self.plan_scroll_frame, fg_color=BG_COLOR, corner_radius=8,
                                      border_width=1, border_color=SHADOW_COLOR)
            plan_frame.pack(fill="x", pady=5, padx=5)
            plan_frame.grid_columnconfigure(1, weight=1)

            status_color = ACCENT_COLOR_1 if plan_data['status'] == "Completed" else \
                           ACCENT_COLOR_3 if plan_data['status'] == "In Progress" else \
                           ACCENT_COLOR_2 # Planned

            checkbox = ctk.CTkCheckBox(plan_frame, text="", fg_color=BUTTON_BG_COLOR,
                                         hover_color=BUTTON_HOVER_COLOR,
                                         checkmark_color=BUTTON_TEXT_COLOR,
                                         border_color=BUTTON_BG_COLOR, border_width=2,
                                         command=lambda idx=i: self.toggle_plan_selection(idx))
            checkbox.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
            if plan_data.get('selected_for_action', False):
                checkbox.select()
            else:
                checkbox.deselect()

            plan_text = ctk.CTkLabel(plan_frame, text=f"{plan_data['subject']}: {plan_data['topic']} (Due: {plan_data['due_date']})",
                                     font=FONT_BODY, text_color=TEXT_COLOR)
            if plan_data['status'] == "Completed":
                plan_text.configure(text_color="gray", font=(FONT_BODY[0], FONT_BODY[1], "overstrike"))
            else:
                plan_text.configure(text_color=TEXT_COLOR, font=FONT_BODY)
            plan_text.grid(row=0, column=1, sticky="w", padx=(0, 10))

            status_label = ctk.CTkLabel(plan_frame, text=plan_data['status'],
                                         font=FONT_SMALL_BOLD, text_color=status_color)
            status_label.grid(row=0, column=2, padx=(0, 10), sticky="e")

    def toggle_plan_selection(self, index):
        plans = self.plans_data.get_user_data(self.current_user, [])
        if 0 <= index < len(plans):
            plans[index]['selected_for_action'] = not plans[index].get('selected_for_action', False)
            self.plans_data.set_user_data(self.current_user, plans)
            self.refresh_study_plan_list()

    def update_selected_plan_status(self):
        plans = self.plans_data.get_user_data(self.current_user, [])
        selected_plans_count = 0
        for plan in plans:
            if plan.get('selected_for_action', False):
                if plan['status'] == "Planned":
                    plan['status'] = "In Progress"
                elif plan['status'] == "In Progress":
                    plan['status'] = "Completed"
                # If already completed, keep it completed.
                plan['selected_for_action'] = False # Deselect after action
                selected_plans_count += 1
        
        if selected_plans_count == 0:
            messagebox.showwarning("No Selection", "Please select at least one study plan to update.", icon="warning")
            return

        self.plans_data.set_user_data(self.current_user, plans)
        self.refresh_study_plan_list()
        messagebox.showinfo("Success", f"{selected_plans_count} plan(s) status updated!", icon="info")

    def delete_selected_plans(self):
        plans = self.plans_data.get_user_data(self.current_user, [])
        plans_to_keep = []
        deleted_count = 0
        for plan in plans:
            if not plan.get('selected_for_action', False):
                plans_to_keep.append(plan)
            else:
                deleted_count += 1

        if deleted_count == 0:
            messagebox.showwarning("No Selection", "Please select plans to delete.", icon="warning")
            return

        self.plans_data.set_user_data(self.current_user, plans_to_keep)
        self.refresh_study_plan_list()
        messagebox.showinfo("Success", f"{deleted_count} plan(s) deleted successfully!", icon="info")

    # Doubt Notebook
    def doubt_notebook(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Doubt Notebook")
        win.geometry("750x650")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)

        ctk.CTkLabel(frame, text="❓ Doubt Notebook", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).pack(pady=(20, 15))

        input_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        input_frame.pack(pady=10, padx=15, fill="x")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Doubt Title:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.doubt_title_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., Python List Comprehension",
                                             fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.doubt_title_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="Doubt Description:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.doubt_desc_textbox = ctk.CTkTextbox(input_frame, height=100,
                                                 fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                                 corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.doubt_desc_textbox.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        ctk.CTkLabel(input_frame, text="Status:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.doubt_status_optionmenu = ctk.CTkOptionMenu(input_frame, values=["Unresolved", "Resolved"],
                                                         fg_color=BUTTON_BG_COLOR, button_color=BUTTON_BG_COLOR,
                                                         text_color=BUTTON_TEXT_COLOR, # Explicitly setting to white
                                                         dropdown_fg_color=BUTTON_HOVER_COLOR,
                                                         dropdown_hover_color=SHADOW_COLOR)
        self.doubt_status_optionmenu.set("Unresolved")
        self.doubt_status_optionmenu.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        
        ctk.CTkButton(input_frame, text="Add Doubt", fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.add_doubt).grid(row=6, column=0, pady=5, sticky="w")
        
        ctk.CTkButton(input_frame, text="Load Doubt from File", fg_color=ACCENT_COLOR_2, hover_color="#42A5F5", # Reverted hover
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.load_doubt_from_file).grid(row=6, column=1, padx=(10,0), pady=5, sticky="ew")


        ctk.CTkLabel(frame, text="Your Doubts:", font=("Inter", 18, "bold"), text_color=HEADER_TEXT_COLOR).pack(pady=(20, 10))

        list_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        self.doubt_scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color=CARD_BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        self.doubt_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.doubt_scroll_frame.grid_columnconfigure(0, weight=1)
        
        btn_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        btn_frame.pack(pady=(5, 15), fill="x", padx=15)
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1) # Added 3rd column

        ctk.CTkButton(btn_frame, text="Update Status", fg_color=ACCENT_COLOR_2, hover_color="#42A5F5", # Reverted hover
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.update_selected_doubt_status).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="Save Selected to File", fg_color=ACCENT_COLOR_1, hover_color="#5cb85c",
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.save_selected_doubt_to_file).grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color=ACCENT_COLOR_4, hover_color="#dc3545", # Reverted hover
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.delete_selected_doubts).grid(row=0, column=2, padx=5, sticky="ew")

        self.refresh_doubt_list()

    def add_doubt(self):
        title = self.doubt_title_entry.get().strip()
        description = self.doubt_desc_textbox.get("1.0", "end").strip()
        status = self.doubt_status_optionmenu.get()

        if not title or not description:
            messagebox.showerror("Input Error", "Doubt title and description cannot be empty.", icon="error")
            return

        doubts = self.doubts_data.get_user_data(self.current_user, [])
        doubts.append({"title": title, "description": description, "status": status})
        self.doubts_data.set_user_data(self.current_user, doubts)
        self.doubt_title_entry.delete(0, "end")
        self.doubt_desc_textbox.delete("1.0", "end")
        self.doubt_status_optionmenu.set("Unresolved")
        self.refresh_doubt_list()
        messagebox.showinfo("Success", "Doubt added successfully!", icon="info")
        
    def load_doubt_from_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.doubt_folder,
            title="Select Doubt File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Assuming the file format is Title\nDescription
                lines = content.split('\n', 1)
                title = lines[0].replace("Title: ", "").strip() if lines else ""
                description = lines[1].replace("Description: ", "").strip() if len(lines) > 1 else ""

                self.doubt_title_entry.delete(0, "end")
                self.doubt_title_entry.insert(0, title)
                self.doubt_desc_textbox.delete("1.0", "end")
                self.doubt_desc_textbox.insert("1.0", description)
                self.doubt_status_optionmenu.set("Unresolved") # Default status on load
                messagebox.showinfo("File Loaded", "Doubt loaded from file. You can now add it.", icon="info")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}", icon="error")

    def save_selected_doubt_to_file(self):
        doubts = self.doubts_data.get_user_data(self.current_user, [])
        selected_doubts = [d for d in doubts if d.get('selected_for_action', False)]

        if not selected_doubts:
            messagebox.showwarning("No Selection", "Please select at least one doubt to save.", icon="warning")
            return

        for doubt in selected_doubts:
            # Create a filename from the doubt title, sanitizing it
            filename_safe_title = "".join([c if c.isalnum() else "_" for c in doubt['title']]).strip("_")
            if not filename_safe_title:
                filename_safe_title = f"doubt_{uuid.uuid4().hex[:8]}" # Fallback
            file_path = os.path.join(self.doubt_folder, f"{filename_safe_title}.txt")
            
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"Title: {doubt['title']}\n")
                    f.write(f"Description: {doubt['description']}\n")
                    f.write(f"Status: {doubt['status']}\n")
                doubt['selected_for_action'] = False # Deselect after saving
                messagebox.showinfo("Saved", f"Doubt '{doubt['title']}' saved to {file_path}", icon="info")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save doubt '{doubt['title']}': {e}", icon="error")
        self.refresh_doubt_list() # Refresh to clear checkboxes

    def refresh_doubt_list(self):
        for widget in self.doubt_scroll_frame.winfo_children():
            widget.destroy()

        doubts = self.doubts_data.get_user_data(self.current_user, [])
        if not doubts:
            ctk.CTkLabel(self.doubt_scroll_frame, text="No doubts added yet! Record your questions here.", text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=20)
            return

        for i, doubt_data in enumerate(doubts):
            doubt_frame = ctk.CTkFrame(self.doubt_scroll_frame, fg_color=BG_COLOR, corner_radius=8,
                                       border_width=1, border_color=SHADOW_COLOR)
            doubt_frame.pack(fill="x", pady=5, padx=5)
            doubt_frame.grid_columnconfigure(1, weight=1)

            status_color = ACCENT_COLOR_1 if doubt_data['status'] == "Resolved" else ACCENT_COLOR_4

            checkbox = ctk.CTkCheckBox(doubt_frame, text="", fg_color=BUTTON_BG_COLOR,
                                         hover_color=BUTTON_HOVER_COLOR,
                                         checkmark_color=BUTTON_TEXT_COLOR,
                                         border_color=BUTTON_BG_COLOR, border_width=2,
                                         command=lambda idx=i: self.toggle_doubt_selection(idx))
            checkbox.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
            if doubt_data.get('selected_for_action', False):
                checkbox.select()
            else:
                checkbox.deselect()

            title_label = ctk.CTkLabel(doubt_frame, text=doubt_data['title'],
                                       font=FONT_BODY, text_color=TEXT_COLOR)
            if doubt_data['status'] == "Resolved":
                title_label.configure(text_color="gray", font=(FONT_BODY[0], FONT_BODY[1], "overstrike"))
            else:
                title_label.configure(text_color=TEXT_COLOR, font=FONT_BODY)
            title_label.grid(row=0, column=1, sticky="w", padx=(0, 10))
            
            status_label = ctk.CTkLabel(doubt_frame, text=doubt_data['status'],
                                         font=FONT_SMALL_BOLD, text_color=status_color)
            status_label.grid(row=0, column=2, padx=(0, 10), sticky="e")
            
            # Add a button to view description
            view_button = ctk.CTkButton(doubt_frame, text="View", width=60,
                                        fg_color=ACCENT_COLOR_2, hover_color="#42A5F5", # Reverted hover
                                        text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=8,
                                        command=lambda desc=doubt_data['description'], title=doubt_data['title']: self.show_doubt_description(title, desc))
            view_button.grid(row=0, column=3, padx=(0, 10), sticky="e")


    def show_doubt_description(self, title, description):
        desc_win = ctk.CTkToplevel(self.dash)
        desc_win.title(f"Doubt: {title}")
        desc_win.geometry("500x300")
        desc_win.configure(fg_color=BG_COLOR)
        desc_win.transient(self.dash)
        desc_win.grab_set()

        ctk.CTkLabel(desc_win, text=f"Title: {title}", font=FONT_MEDIUM, text_color=HEADER_TEXT_COLOR).pack(pady=(15, 10))
        description_label = ctk.CTkLabel(desc_win, text=description, font=FONT_BODY, text_color=TEXT_COLOR, wraplength=450, justify="left")
        description_label.pack(padx=20, pady=(0, 15))
        
        ctk.CTkButton(desc_win, text="Close", command=desc_win.destroy,
                      fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                      text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).pack(pady=10)


    def toggle_doubt_selection(self, index):
        doubts = self.doubts_data.get_user_data(self.current_user, [])
        if 0 <= index < len(doubts):
            doubts[index]['selected_for_action'] = not doubts[index].get('selected_for_action', False)
            self.doubts_data.set_user_data(self.current_user, doubts)
            self.refresh_doubt_list()

    def update_selected_doubt_status(self):
        doubts = self.doubts_data.get_user_data(self.current_user, [])
        updated_count = 0
        for doubt in doubts:
            if doubt.get('selected_for_action', False) and doubt['status'] == "Unresolved":
                doubt['status'] = "Resolved"
                doubt['selected_for_action'] = False
                updated_count += 1
            elif doubt.get('selected_for_action', False) and doubt['status'] == "Resolved":
                doubt['selected_for_action'] = False

        if updated_count == 0:
            messagebox.showwarning("No Selection", "Please select unresolved doubts to mark as resolved.", icon="warning")
            return

        self.doubts_data.set_user_data(self.current_user, doubts)
        self.refresh_doubt_list()
        messagebox.showinfo("Success", f"{updated_count} doubt(s) status updated!", icon="info")

    def delete_selected_doubts(self):
        doubts = self.doubts_data.get_user_data(self.current_user, [])
        doubts_to_keep = []
        deleted_count = 0
        for doubt in doubts:
            if not doubt.get('selected_for_action', False):
                doubts_to_keep.append(doubt)
            else:
                deleted_count += 1

        if deleted_count == 0:
            messagebox.showwarning("No Selection", "Please select doubts to delete.", icon="warning")
            return

        self.doubts_data.set_user_data(self.current_user, doubts_to_keep)
        self.refresh_doubt_list()
        messagebox.showinfo("Success", f"{deleted_count} doubt(s) deleted successfully!", icon="info")


    # Pomodoro Timer
    def pomodoro_timer(self):
        if self._pomodoro_timer_window and self._pomodoro_timer_window.winfo_exists():
            self._pomodoro_timer_window.focus()
            return
            
        win = ctk.CTkToplevel(self.dash)
        win.title("Pomodoro Timer")
        win.geometry("400x650") # *** CHANGED: Increased height for history
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()
        self._pomodoro_timer_window = win # Store reference

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1) # *** ADDED: Make history row expandable

        ctk.CTkLabel(frame, text="⏰ Pomodoro Timer", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).grid(row=0, column=0, pady=(20, 15))

        self.pomodoro_time_label = ctk.CTkLabel(frame, text="25:00", font=("Inter", 48, "bold"), text_color=TEXT_COLOR)
        self.pomodoro_time_label.grid(row=1, column=0, pady=(10, 20))

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=(0, 20))
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(button_frame, text="Start Pomodoro", command=self.start_pomodoro_timer,
                         fg_color=ACCENT_COLOR_1, hover_color="#5cb85c",
                         text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).grid(row=0, column=0, padx=5)
        ctk.CTkButton(button_frame, text="Pause", command=self.pause_pomodoro_timer,
                         fg_color=ACCENT_COLOR_3, hover_color="#f0ad4e", # Reverted hover
                         text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).grid(row=0, column=1, padx=5)
        ctk.CTkButton(button_frame, text="Reset", command=self.reset_pomodoro_timer,
                         fg_color=ACCENT_COLOR_4, hover_color="#dc3545", # Reverted hover
                         text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).grid(row=0, column=2, padx=5)

        # --- MODIFIED: Renamed to "My Timer" ---
        my_timer_frame = ctk.CTkFrame(frame, fg_color="transparent")
        my_timer_frame.grid(row=3, column=0, pady=(10, 10)) # Added new row
        my_timer_frame.grid_columnconfigure(0, weight=1) 
        my_timer_frame.grid_columnconfigure(1, weight=1) 

        ctk.CTkLabel(my_timer_frame, text="My Timer (min):", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=0, column=0, sticky="e", padx=(0,5))
        self.my_timer_minutes_entry = ctk.CTkEntry(my_timer_frame, width=80, fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.my_timer_minutes_entry.grid(row=0, column=1, sticky="w", padx=(5,0))
        
        ctk.CTkButton(my_timer_frame, text="Start My Timer", command=self.start_my_timer_countdown,
                         fg_color=ACCENT_COLOR_2, hover_color="#42A5F5",
                         text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                         height=40).grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        # --- END MODIFIED ---

        # --- ADDED: Timer History ---
        ctk.CTkLabel(frame, text="Timer History", font=("Inter", 18, "bold"), text_color=HEADER_TEXT_COLOR).grid(row=4, column=0, pady=(20, 10))

        history_list_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        history_list_frame.grid(row=5, column=0, sticky="nsew", padx=15, pady=(0, 10))
        history_list_frame.grid_columnconfigure(0, weight=1)
        history_list_frame.grid_rowconfigure(0, weight=1)

        self.timer_history_scroll_frame = ctk.CTkScrollableFrame(history_list_frame, fg_color=CARD_BG_COLOR, corner_radius=10)
        self.timer_history_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.timer_history_scroll_frame.grid_columnconfigure(0, weight=1)
        # --- END ADDED HISTORY UI ---

        win.protocol("WM_DELETE_WINDOW", self.stop_pomodoro_timer) # Ensure thread stops on window close

        self._pomodoro_time_left = self._work_minutes * 60
        self.update_pomodoro_timer_display()
        self.refresh_timer_history() # *** ADDED: Populate history on open

    # *** RENAMED function
    def start_my_timer_countdown(self):
        """Starts a one-time countdown based on user input."""
        if self._timer_running:
            messagebox.showwarning("Timer Active", "A timer is already running. Please pause or reset it first.", icon="warning")
            return
        
        try:
            custom_minutes = int(self.my_timer_minutes_entry.get())
            if custom_minutes <= 0:
                messagebox.showerror("Invalid Input", "Please enter a positive number of minutes.", icon="error")
                return

            self._pomodoro_time_left = custom_minutes * 60
            self._pomodoro_state = "my_timer" # *** CHANGED state name
            self._current_timer_duration_minutes = custom_minutes # *** ADDED: Log duration
            
            # Start the main timer logic
            self._timer_running = True
            self._timer_thread = threading.Thread(target=self._run_pomodoro_timer_thread)
            self._timer_thread.daemon = True
            self._timer_thread.start()
            messagebox.showinfo("My Timer", f"My Timer for {custom_minutes} minutes started!", icon="info") # *** CHANGED title

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for minutes.", icon="error")
        except AttributeError:
             messagebox.showerror("Error", "Timer window elements not found. Please reopen the timer.", icon="error")

    # *** ADDED: New function to log completed timers
    def log_timer_session(self, timer_type, duration_minutes):
        """Logs a completed timer session to the user's history."""
        if not self.current_user:
            return # Don't log if no user
            
        history = self.timer_history_data.get_user_data(self.current_user, [])
        log_entry = {
            "type": timer_type,
            "duration_minutes": duration_minutes,
            "timestamp": datetime.now().isoformat()
        }
        history.append(log_entry)
        self.timer_history_data.set_user_data(self.current_user, history)
        
        # Refresh the list if it's open
        self.app.after(0, self.refresh_timer_history)

    # *** ADDED: New function to refresh history UI
    def refresh_timer_history(self):
        """Refreshes the timer history scrollable frame."""
        # Check if the frame exists (window is open)
        if not (self.timer_history_scroll_frame and self.timer_history_scroll_frame.winfo_exists()):
            return
            
        for widget in self.timer_history_scroll_frame.winfo_children():
            widget.destroy()

        history = self.timer_history_data.get_user_data(self.current_user, [])
        if not history:
            ctk.CTkLabel(self.timer_history_scroll_frame, text="No completed timers yet.",
                         text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=20)
            return

        # Show latest entries first (up to 20)
        for entry in reversed(history[-20:]):
            try:
                timestamp = datetime.fromisoformat(entry['timestamp'])
                time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = "Unknown time"
                
            duration = entry.get('duration_minutes', 0)
            timer_type = entry.get('type', 'Unknown')
            
            log_text = f"{time_str} - {timer_type} ({duration} min)"
            
            ctk.CTkLabel(self.timer_history_scroll_frame, text=log_text,
                         font=FONT_SMALL, text_color=HEADER_TEXT_COLOR).pack(anchor="w", padx=10, pady=2)


    def update_pomodoro_timer_display(self):
        if self.pomodoro_time_label and self.pomodoro_time_label.winfo_exists():
            minutes = self._pomodoro_time_left // 60
            seconds = self._pomodoro_time_left % 60
            self.pomodoro_time_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    # *** MODIFIED: To set duration for logging
    def start_pomodoro_timer(self):
        if not self._timer_running:
            self._timer_running = True
            if self._pomodoro_state == "stopped":
                self._pomodoro_time_left = self._work_minutes * 60
                self._pomodoro_state = "work"
                self._current_timer_duration_minutes = self._work_minutes # Set duration here
            elif self._pomodoro_state == "break":
                # This is when a break is starting
                self._pomodoro_time_left = self._break_minutes * 60
                self._current_timer_duration_minutes = self._break_minutes # Set duration here
            
            self._timer_thread = threading.Thread(target=self._run_pomodoro_timer_thread)
            self._timer_thread.daemon = True # Allows the program to exit even if thread is running
            self._timer_thread.start()
            messagebox.showinfo("Pomodoro", f"Pomodoro {self._pomodoro_state} session started!", icon="info")

    def pause_pomodoro_timer(self):
        if self._timer_running:
            self._timer_running = False
            messagebox.showinfo("Pomodoro", "Pomodoro timer paused.", icon="info")

    def reset_pomodoro_timer(self):
        self.stop_pomodoro_timer(stop_thread=True)
        self._pomodoro_time_left = self._work_minutes * 60
        self._pomodoro_state = "stopped"
        self.update_pomodoro_timer_display()
        messagebox.showinfo("Pomodoro", "Pomodoro timer reset.", icon="info")

    def stop_pomodoro_timer(self, stop_thread=False):
        self._timer_running = False
        if stop_thread and self._timer_thread and self._timer_thread.is_alive():
            # This is a soft stop; the thread will exit its loop naturally
            pass 
        if self._pomodoro_timer_id:
            self.app.after_cancel(self._pomodoro_timer_id)
            self._pomodoro_timer_id = None
        
        # *** ADDED: Clear history frame reference on close
        self.timer_history_scroll_frame = None 
        
        if self._pomodoro_timer_window and self._pomodoro_timer_window.winfo_exists():
            self._pomodoro_timer_window.destroy()
        self._pomodoro_timer_window = None


    # *** MODIFIED: To log sessions when they finish
    def _run_pomodoro_timer_thread(self):
        while self._timer_running and self._pomodoro_time_left > 0:
            time.sleep(1)
            if not self._timer_running: # Check again in case it was paused during sleep
                break
            self._pomodoro_time_left -= 1
            self.app.after(0, self.update_pomodoro_timer_display) # Update UI on main thread

        if self._pomodoro_time_left <= 0:
            self._timer_running = False
            
            if self._pomodoro_state == "work":
                self.log_timer_session("Pomodoro", self._current_timer_duration_minutes) # Log
                messagebox.showinfo("Pomodoro", "Work session finished! Time for a break.", icon="info")
                winsound.Beep(2500, 500) # Play a buzzing sound
                self._pomodoro_time_left = self._break_minutes * 60
                self._pomodoro_state = "break"
                self.app.after(100, self.start_pomodoro_timer) # Start break timer automatically
            
            elif self._pomodoro_state == "break":
                self.log_timer_session("Break", self._current_timer_duration_minutes) # Log
                messagebox.showinfo("Pomodoro", "Break finished! Time to work.", icon="info")
                winsound.Beep(2500, 500) # Play a buzzing sound
                self._pomodoro_time_left = self._work_minutes * 60
                self._pomodoro_state = "stopped" # Go to stopped state, user can restart
                self.app.after(0, self.update_pomodoro_timer_display) # Update to 25:00
            
            elif self._pomodoro_state == "my_timer": # *** CHANGED state name
                self.log_timer_session("My Timer", self._current_timer_duration_minutes) # Log
                messagebox.showinfo("Timer Finished", "Your timer is done!", icon="info") # *** CHANGED title
                winsound.Beep(2500, 500) # Play a buzzing sound
                self._pomodoro_time_left = self._work_minutes * 60 # Reset to default Pomodoro time
                self._pomodoro_state = "stopped" 
                self.app.after(0, self.update_pomodoro_timer_display) # Update display to 25:00

    # Study Progress Tracker
    def study_progress(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Study Progress Tracker")
        win.geometry("700x600")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)

        ctk.CTkLabel(frame, text="📈 Study Progress Tracker", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).pack(pady=(20, 15))

        input_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        input_frame.pack(pady=10, padx=15, fill="x")
        input_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(input_frame, text="Subject/Topic:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.progress_topic_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., Calculus - Integrals",
                                                 fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                                 corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.progress_topic_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="Progress (0-100%):", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.progress_slider = ctk.CTkSlider(input_frame, from_=0, to=100, number_of_steps=100,
                                             fg_color=SHADOW_COLOR, progress_color=ACCENT_COLOR_1,
                                             command=self.update_progress_label)
        self.progress_slider.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        self.progress_slider.set(0)
        self.progress_value_label = ctk.CTkLabel(input_frame, text="0%", text_color=TEXT_COLOR, font=FONT_BODY)
        self.progress_value_label.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(0, 10))

        ctk.CTkButton(input_frame, text="Add/Update Progress", fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.add_or_update_progress).grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Your Progress:", font=("Inter", 18, "bold"), text_color=HEADER_TEXT_COLOR).pack(pady=(20, 10))

        list_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        self.progress_scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color=CARD_BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        self.progress_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.progress_scroll_frame.grid_columnconfigure(0, weight=1)

        btn_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        btn_frame.pack(pady=(5, 15), fill="x", padx=15)
        btn_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(btn_frame, text="Delete Selected Progress", fg_color=ACCENT_COLOR_4, hover_color="#dc3545", # Reverted hover
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.delete_selected_progress).grid(row=0, column=0, padx=5, sticky="ew")

        self.refresh_progress_list()

    def update_progress_label(self, value):
        self.progress_value_label.configure(text=f"{int(value)}%")

    def add_or_update_progress(self):
        topic = self.progress_topic_entry.get().strip()
        progress_value = int(self.progress_slider.get())

        if not topic:
            messagebox.showerror("Input Error", "Subject/Topic cannot be empty.", icon="error")
            return

        progress_items = self.progress_data.get_user_data(self.current_user, [])
        updated = False
        for item in progress_items:
            if item["topic"].lower() == topic.lower():
                item["progress"] = progress_value
                updated = True
                break
        
        if not updated:
            progress_items.append({"topic": topic, "progress": progress_value})
        
        self.progress_data.set_user_data(self.current_user, progress_items)
        self.progress_topic_entry.delete(0, "end")
        self.progress_slider.set(0)
        self.update_progress_label(0)
        self.refresh_progress_list()
        messagebox.showinfo("Success", "Study progress updated successfully!", icon="info")

    def refresh_progress_list(self):
        for widget in self.progress_scroll_frame.winfo_children():
            widget.destroy()

        progress_items = self.progress_data.get_user_data(self.current_user, [])
        if not progress_items:
            ctk.CTkLabel(self.progress_scroll_frame, text="No progress tracked yet! Add a subject/topic to start.", text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=20)
            return

        for i, item in enumerate(progress_items):
            progress_frame = ctk.CTkFrame(self.progress_scroll_frame, fg_color=BG_COLOR, corner_radius=8,
                                          border_width=1, border_color=SHADOW_COLOR)
            progress_frame.pack(fill="x", pady=5, padx=5)
            progress_frame.grid_columnconfigure(1, weight=1)

            checkbox = ctk.CTkCheckBox(progress_frame, text="", fg_color=BUTTON_BG_COLOR,
                                         hover_color=BUTTON_HOVER_COLOR,
                                         checkmark_color=BUTTON_TEXT_COLOR,
                                         border_color=BUTTON_BG_COLOR, border_width=2,
                                         command=lambda idx=i: self.toggle_progress_selection(idx))
            checkbox.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
            if item.get('selected_for_action', False):
                checkbox.select()
            else:
                checkbox.deselect()

            ctk.CTkLabel(progress_frame, text=f"{item['topic']}: {item['progress']}%",
                                     font=FONT_BODY, text_color=TEXT_COLOR).grid(row=0, column=1, sticky="w", padx=(0, 10))

    def toggle_progress_selection(self, index):
        progress_items = self.progress_data.get_user_data(self.current_user, [])
        if 0 <= index < len(progress_items):
            progress_items[index]['selected_for_action'] = not progress_items[index].get('selected_for_action', False)
            self.progress_data.set_user_data(self.current_user, progress_items)
            self.refresh_progress_list()

    def delete_selected_progress(self):
        progress_items = self.progress_data.get_user_data(self.current_user, [])
        items_to_keep = []
        deleted_count = 0
        for item in progress_items:
            if not item.get('selected_for_action', False):
                items_to_keep.append(item)
            else:
                deleted_count += 1

        if deleted_count == 0:
            messagebox.showwarning("No Selection", "Please select progress items to delete.", icon="warning")
            return

        self.progress_data.set_user_data(self.current_user, items_to_keep)
        self.refresh_progress_list()
        messagebox.showinfo("Success", f"{deleted_count} progress item(s) deleted successfully!", icon="info")

    def start_breathing_exercise(self):
        exercise_window = ctk.CTkToplevel(self.dash)
        exercise_window.title("Breathing Exercise")
        exercise_window.geometry("400x300")
        exercise_window.configure(fg_color=BG_COLOR)
        exercise_window.transient(self.dash)
        exercise_window.grab_set()

        instructions = (
            "Follow this simple 4-7-8 breathing exercise:\n\n"
            "1. Inhale slowly through your nose for 4 seconds.\n"
            "2. Hold your breath for 7 seconds.\n"
            "3. Exhale slowly through your mouth for 8 seconds.\n\n"
            "Repeat this cycle 3-5 times."
        )

        label = ctk.CTkLabel(
            exercise_window, text=instructions,
            font=FONT_BODY, wraplength=380, justify="left"
        )
        label.pack(pady=20)

        close_btn = ctk.CTkButton(exercise_window, text="Done", 
                                 command=exercise_window.destroy,
                                 fg_color=BUTTON_BG_COLOR,
                                 hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR)
        close_btn.pack(pady=10)

    # Wellness Panel (Reverted to original Mood Tracker)
    def wellness_panel(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Wellness Panel")
        win.geometry("500x550")  # Adjust size
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                         border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)  # Center content

        # Header
        ctk.CTkLabel(frame, text="🧘 Wellness Panel", font=("Inter", 24, "bold"),
                 text_color=HEADER_TEXT_COLOR).pack(pady=(20, 15))

        # Breathing Exercise Button
        ctk.CTkButton(
            frame,
            text="Feeling Tired? Do Breathing Exercise",
            command=self.start_breathing_exercise,
            fg_color="#a2d5f2",
            hover_color="#89c9f0",
            text_color="black",
            font=("Helvetica", 11, "bold"),
            width=250,
            height=40
        ).pack(pady=(0, 20))

        # Mood input section
        ctk.CTkLabel(frame, text="How are you feeling today?", text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=(0, 5))
        self.mood_optionmenu = ctk.CTkOptionMenu(frame, values=["Good 😊", "Okay 😐", "Stressed 😟", "Happy 😄", "Sad 😢"],
                                             fg_color=BUTTON_BG_COLOR, button_color=BUTTON_BG_COLOR,
                                             text_color=BUTTON_TEXT_COLOR,
                                             dropdown_fg_color=BUTTON_HOVER_COLOR,
                                             dropdown_hover_color=SHADOW_COLOR,
                                             width=250, height=40)
        self.mood_optionmenu.set("Good 😊")  # Default value
        self.mood_optionmenu.pack(pady=(0, 20))

        ctk.CTkLabel(frame, text="Notes for today (Optional):", text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=(0, 5))
        self.mood_notes_textbox = ctk.CTkTextbox(frame, height=100, width=350,
                                             fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY,
                                             corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.mood_notes_textbox.pack(pady=(0, 20))

        ctk.CTkButton(frame, text="Log Mood", command=self.log_mood,
                  fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                  text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                  width=150, height=40).pack(pady=(0, 30))

        # Mood History section
        ctk.CTkLabel(frame, text="Your Mood History:", font=("Inter", 18, "bold"), text_color=HEADER_TEXT_COLOR).pack(pady=(0, 10))

        list_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        self.mood_history_scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color=CARD_BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        self.mood_history_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.mood_history_scroll_frame.grid_columnconfigure(0, weight=1)

        self.refresh_mood_history()

    def log_mood(self):
        mood = self.mood_optionmenu.get()
        notes = self.mood_notes_textbox.get("1.0", "end").strip()
        
        moods = self.moods_data.get_user_data(self.current_user, [])
        moods.append({
            "mood": mood,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        })
        self.moods_data.set_user_data(self.current_user, moods)
        
        self.mood_notes_textbox.delete("1.0", "end")
        self.refresh_mood_history()
        messagebox.showinfo("Success", "Mood logged successfully!", icon="info")

    def refresh_mood_history(self):
        for widget in self.mood_history_scroll_frame.winfo_children():
            widget.destroy()

        moods = self.moods_data.get_user_data(self.current_user, [])
        if not moods:
            ctk.CTkLabel(self.mood_history_scroll_frame, 
                        text="No mood entries yet! Log your first mood above.",
                        text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=20)
            return

        # Show latest entries first
        for mood_data in reversed(moods[-10:]):  # Show last 10 entries
            try:
                timestamp = datetime.fromisoformat(mood_data['timestamp'])
                time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = "Unknown time"
                
            mood_frame = ctk.CTkFrame(self.mood_history_scroll_frame, 
                                    fg_color=BG_COLOR, corner_radius=8,
                                    border_width=1, border_color=SHADOW_COLOR)
            mood_frame.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(mood_frame, text=f"{time_str}: {mood_data['mood']}", 
                        font=FONT_SMALL_BOLD, text_color=HEADER_TEXT_COLOR).pack(anchor="w", padx=10, pady=5)
            
            if mood_data.get('notes'):
                ctk.CTkLabel(mood_frame, text=mood_data['notes'], 
                            font=FONT_SMALL, text_color=TEXT_COLOR, 
                            wraplength=400, justify="left").pack(anchor="w", padx=10, pady=(0,5))

    #Syllabus Manager Feature ---
    def syllabus_manager(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Syllabus Manager")
        win.geometry("800x600")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="📘 Syllabus Manager", font=("Inter", 26, "bold"),
                     text_color=HEADER_TEXT_COLOR).pack(pady=(20, 10))

        ctk.CTkLabel(frame, text="Upload syllabus files for your subjects:",
                     font=FONT_BODY, text_color=TEXT_COLOR).pack(pady=(0, 15))

        subjects = [
            "ENGINEERING WORKSHOP",
            "ENGINEERING CHEMISTRY",
            "ENGLISH",
            "MATHS",
            "ENVIRONMENTAL SCIENCE",
            "EITK",
            "PPS"
        ]

        self.syllabus_folder = "syllabus_files"
        os.makedirs(self.syllabus_folder, exist_ok=True)

        for sub in subjects:
            sub_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR, corner_radius=8,
                                     border_width=1, border_color=SHADOW_COLOR)
            sub_frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(sub_frame, text=sub, font=FONT_SMALL_BOLD,
                         text_color=HEADER_TEXT_COLOR).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(sub_frame, text="Upload File",
                          fg_color=ACCENT_COLOR_2, hover_color="#42A5F5",
                          text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON,
                          corner_radius=8,
                          command=lambda s=sub: self.upload_syllabus_file(s)).pack(side="right", padx=10, pady=8)

        ctk.CTkLabel(frame, text="\nUploaded files are saved locally in 'syllabus_files' folder.",
                     font=FONT_SMALL, text_color=TEXT_COLOR).pack(pady=(10, 0))

    def upload_syllabus_file(self, subject):
        """Lets user pick a syllabus file and saves it with subject name."""
        file_path = filedialog.askopenfilename(
            title=f"Select Syllabus File for {subject}",
            filetypes=(("PDF files", "*.pdf"),
                       ("Word files", "*.docx"),
                       ("Text files", "*.txt"),
                       ("All files", "*.*"))
        )
        if file_path:
            try:
                ext = os.path.splitext(file_path)[1]
                dest_path = os.path.join(self.syllabus_folder, f"{subject}{ext}")
                with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())
                messagebox.showinfo("Success", f"Syllabus for {subject} uploaded successfully!", icon="info")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload file: {e}", icon="error")
        # --- 📗 View Uploaded Syllabus Files ---
    def view_uploaded_syllabus(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("View Uploaded Syllabus")
        win.geometry("800x600")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)

        ctk.CTkLabel(frame, text="📗 Uploaded Syllabus Files",
                     font=("Inter", 26, "bold"),
                     text_color=HEADER_TEXT_COLOR).pack(pady=(20, 10))

        syllabus_folder = "syllabus_files"
        os.makedirs(syllabus_folder, exist_ok=True)
        files = os.listdir(syllabus_folder)

        if not files:
            ctk.CTkLabel(frame, text="No syllabus files uploaded yet.",
                         font=FONT_BODY, text_color=TEXT_COLOR).pack(pady=20)
            return

        for f in files:
            file_path = os.path.join(syllabus_folder, f)
            sub_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR,
                                     corner_radius=8, border_width=1,
                                     border_color=SHADOW_COLOR)
            sub_frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(sub_frame, text=f, font=FONT_SMALL_BOLD,
                         text_color=HEADER_TEXT_COLOR).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(sub_frame, text="Open File",
                          fg_color=ACCENT_COLOR_2, hover_color="#42A5F5",
                          text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON,
                          corner_radius=8,
                          command=lambda path=file_path: self.open_file(path)
                          ).pack(side="right", padx=10, pady=8)

    def open_file(self, path):
        """Open the selected file using default system viewer."""
        try:
            os.startfile(path)  # Works on Windows
        except AttributeError:
            import subprocess, sys
            if sys.platform == "darwin":  # macOS
                subprocess.call(("open", path))
            else:  # Linux
                subprocess.call(("xdg-open", path))


    # Calendar View (Enhanced)
    def calendar_view(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Calendar View")
        win.geometry("800x700") # Increased size for better calendar display
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="📅 Calendar View", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).grid(row=0, column=0, pady=(20, 15))

        calendar_controls_frame = ctk.CTkFrame(frame, fg_color="transparent")
        calendar_controls_frame.grid(row=1, column=0, pady=10)
        calendar_controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.current_month_year_label = ctk.CTkLabel(calendar_controls_frame, text="",
                                                     font=FONT_MEDIUM, text_color=HEADER_TEXT_COLOR)
        self.current_month_year_label.grid(row=0, column=1, padx=20)

        ctk.CTkButton(calendar_controls_frame, text="< Prev", font=FONT_BUTTON,
                                 fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, corner_radius=8,
                                 command=self.show_prev_month).grid(row=0, column=0)
        ctk.CTkButton(calendar_controls_frame, text="Next >", font=FONT_BUTTON,
                                 fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, corner_radius=8,
                                 command=self.show_next_month).grid(row=0, column=2)

        self.calendar_display_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        self.calendar_display_frame.grid(row=2, column=0, pady=15, padx=15, sticky="nsew")
        self.calendar_display_frame.grid_columnconfigure(tuple(range(7)), weight=1, uniform="cal_cols")
        self.calendar_display_frame.grid_rowconfigure(tuple(range(7)), weight=1, uniform="cal_rows") # For 6 weeks + day names

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.draw_calendar()

    def draw_calendar(self):
        # Clear existing widgets in the calendar grid
        for widget in self.calendar_display_frame.winfo_children():
            widget.destroy()

        self.current_month_year_label.configure(text=f"{cal.month_name[self.current_month]} {self.current_year}")

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(day_names):
            ctk.CTkLabel(self.calendar_display_frame, text=day, font=FONT_SMALL_BOLD,
                                 text_color=HEADER_TEXT_COLOR, fg_color=CARD_BG_COLOR, corner_radius=5).grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

        cal_obj = cal.Calendar()
        month_days = cal_obj.monthdayscalendar(self.current_year, self.current_month)
        today = datetime.now().day if self.current_year == datetime.now().year and self.current_month == datetime.now().month else -1

        row_offset = 1 # Start drawing days from the second row (after day names)
        for week in month_days:
            for col, day_num in enumerate(week):
                day_frame = ctk.CTkFrame(self.calendar_display_frame, width=80, height=80, # Increased size for better content display
                                         fg_color=BG_COLOR, corner_radius=8,
                                         border_color=SHADOW_COLOR, border_width=1)
                day_frame.grid(row=row_offset, column=col, padx=2, pady=2, sticky="nsew")
                day_frame.grid_propagate(False) # Prevent frame from shrinking to content size

                if day_num != 0:
                    day_text_color = TEXT_COLOR
                    day_bg_color = BG_COLOR
                    if day_num == today:
                        day_bg_color = ACCENT_COLOR_3 # Highlight today's date
                        day_text_color = BUTTON_TEXT_COLOR # White text on highlighted day

                    day_label = ctk.CTkLabel(day_frame, text=str(day_num),
                                             font=FONT_BODY, text_color=day_text_color, fg_color=day_bg_color)
                    day_label.pack(side="top", anchor="ne", padx=5, pady=2) # Align day number to top-right

                    # Check for tasks and reminders on this specific day
                    tasks_on_day = []
                    reminders_on_day = []

                    all_tasks = self.tasks_data.get_user_data(self.current_user, [])
                    for task_data in all_tasks:
                        if task_data['due_date'] != "No Due Date":
                            try:
                                due_date_dt = datetime.strptime(task_data['due_date'], "%Y-%m-%d")
                                if due_date_dt.year == self.current_year and due_date_dt.month == self.current_month and due_date_dt.day == day_num:
                                    tasks_on_day.append(task_data)
                            except ValueError:
                                pass # Skip malformed dates

                    all_reminders = self.reminders_data.get_user_data(self.current_user, [])
                    for reminder_data in all_reminders:
                        try:
                            reminder_dt = datetime.fromisoformat(reminder_data['datetime'])
                            if reminder_dt.year == self.current_year and reminder_dt.month == self.current_month and reminder_dt.day == day_num and reminder_data['status'] == 'active':
                                reminders_on_day.append(reminder_data)
                        except ValueError:
                            pass # Skip malformed dates

                    has_events = False
                    if tasks_on_day or reminders_on_day:
                        has_events = True
                        event_indicator = ctk.CTkLabel(day_frame, text="•", font=("Inter", 20, "bold"), text_color=ACCENT_COLOR_4)
                        event_indicator.pack(side="bottom", pady=(0, 2))
                    
                    # Make the day clickable to show details
                    day_frame.bind("<Button-1>", lambda event, day=day_num, tasks=tasks_on_day, reminders=reminders_on_day: self.show_day_details_popup(day, tasks, reminders))

                else: # Empty day (from previous/next month)
                    day_frame.configure(fg_color=SHADOW_COLOR) # Differentiate empty cells
                    ctk.CTkLabel(day_frame, text="", fg_color=SHADOW_COLOR).pack(fill="both", expand=True) # Empty label to fill space
            row_offset += 1

    def show_day_details_popup(self, day, tasks, reminders):
        popup_window = ctk.CTkToplevel(self.app)
        popup_window.title(f"Events on {self.current_month_year_label.cget('text')} - Day {day}")
        popup_window.geometry("500x400")
        popup_window.configure(fg_color=CARD_BG_COLOR)
        popup_window.transient(self.app)
        popup_window.grab_set()

        ctk.CTkLabel(popup_window, text=f"Events for {cal.month_name[self.current_month]} {day}, {self.current_year}",
                                 font=FONT_MEDIUM, text_color=HEADER_TEXT_COLOR).pack(pady=(15, 10))

        content_frame = ctk.CTkScrollableFrame(popup_window, fg_color=BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        content_frame.pack(padx=20, pady=(0, 15), fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=1)

        if not tasks and not reminders:
            ctk.CTkLabel(content_frame, text="No events scheduled for this day.",
                                     font=FONT_BODY, text_color=TEXT_COLOR).pack(pady=20)
        else:
            if tasks:
                ctk.CTkLabel(content_frame, text="Tasks:", font=FONT_SMALL_BOLD, text_color=HEADER_TEXT_COLOR).pack(anchor="w", padx=10, pady=(10, 5))
                for task in tasks:
                    task_text = f"• {task['task']} (Due: {task['due_date']})"
                    ctk.CTkLabel(content_frame, text=task_text, font=FONT_SMALL, text_color=TEXT_COLOR, wraplength=400, justify="left").pack(anchor="w", padx=20, pady=2)
            
            if reminders:
                ctk.CTkLabel(content_frame, text="Reminders:", font=FONT_SMALL_BOLD, text_color=HEADER_TEXT_COLOR).pack(anchor="w", padx=10, pady=(10, 5))
                for reminder in reminders:
                    try:
                        rem_dt = datetime.fromisoformat(reminder['datetime'])
                        rem_time_str = rem_dt.strftime("%H:%M")
                        reminder_text = f"• {reminder['message']} at {rem_time_str}"
                    except ValueError:
                        reminder_text = f"• {reminder['message']} (Invalid Time)"
                    ctk.CTkLabel(content_frame, text=reminder_text, font=FONT_SMALL, text_color=TEXT_COLOR, wraplength=400, justify="left").pack(anchor="w", padx=20, pady=2)

        ctk.CTkButton(popup_window, text="Close", command=popup_window.destroy,
                      fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                      text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).pack(pady=10)


    def show_prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.draw_calendar()

    def show_next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.draw_calendar()

    # Reminder System
    def reminder_system(self):
        win = ctk.CTkToplevel(self.dash)
        win.title("Reminder System")
        win.geometry("600x600")
        win.configure(fg_color=BG_COLOR)
        win.transient(self.dash)
        win.grab_set()

        frame = ctk.CTkFrame(win, fg_color=CARD_BG_COLOR, corner_radius=12,
                             border_width=1, border_color=SHADOW_COLOR)
        frame.pack(padx=25, pady=25, fill="both", expand=True)

        ctk.CTkLabel(frame, text="🔔 Reminder System", font=("Inter", 24, "bold"),
                                 text_color=HEADER_TEXT_COLOR).pack(pady=(20, 15))

        input_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        input_frame.pack(pady=10, padx=15, fill="x")
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(input_frame, text="Reminder Message:", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.reminder_message_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., Call Mom at 5 PM",
                                                     fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                                     corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.reminder_message_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="Date (YYYY-MM-DD):", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.reminder_date_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 2025-06-30",
                                                 fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                                 corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.reminder_date_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(input_frame, text="Time (HH:MM):", text_color=TEXT_COLOR, font=FONT_BODY).grid(row=2, column=1, sticky="w", padx=(10,0), pady=(0, 5))
        self.reminder_time_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 17:00",
                                                 fg_color="#f3f4f6", text_color=TEXT_COLOR, font=FONT_BODY, # Reverted entries
                                                 corner_radius=8, border_color=SHADOW_COLOR, border_width=1)
        self.reminder_time_entry.grid(row=3, column=1, sticky="ew", padx=(10,0), pady=(0, 10))

        ctk.CTkButton(input_frame, text="Set Reminder", fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.add_reminder).grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

        ctk.CTkLabel(frame, text="Your Reminders:", font=("Inter", 18, "bold"), text_color=HEADER_TEXT_COLOR).pack(pady=(20, 10))

        list_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        self.reminder_scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color=CARD_BG_COLOR, corner_radius=10, border_color=SHADOW_COLOR, border_width=1)
        self.reminder_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.reminder_scroll_frame.grid_columnconfigure(0, weight=1)

        btn_frame = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        btn_frame.pack(pady=(5, 15), fill="x", padx=15)
        btn_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(btn_frame, text="Delete Selected Reminders", fg_color=ACCENT_COLOR_4, hover_color="#dc3545", # Reverted hover
                                 text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10,
                                 command=self.delete_selected_reminders).grid(row=0, column=0, padx=5, sticky="ew")

        self.refresh_reminder_list()

    def add_reminder(self):
        message = self.reminder_message_entry.get().strip()
        date_str = self.reminder_date_entry.get().strip()
        time_str = self.reminder_time_entry.get().strip()

        if not message or not date_str or not time_str:
            messagebox.showerror("Input Error", "All reminder fields must be filled.", icon="error")
            return

        try:
            # Combine date and time into a single datetime object
            reminder_datetime_str = f"{date_str} {time_str}"
            reminder_datetime = datetime.strptime(reminder_datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD and Time HH:MM (24-hour format).", icon="error")
            return

        # Generate a unique ID for the reminder
        reminder_id = str(uuid.uuid4())

        reminders = self.reminders_data.get_user_data(self.current_user, [])
        reminders.append({
            "id": reminder_id,
            "message": message,
            "datetime": reminder_datetime.isoformat(), # Store as ISO format string
            "status": "active" # New status: 'active' or 'dismissed'
        })
        self.reminders_data.set_user_data(self.current_user, reminders)

        self.reminder_message_entry.delete(0, "end")
        self.reminder_date_entry.delete(0, "end")
        self.reminder_time_entry.delete(0, "end")
        self.refresh_reminder_list()
        messagebox.showinfo("Success", "Reminder set successfully!", icon="info")

    def refresh_reminder_list(self):
        for widget in self.reminder_scroll_frame.winfo_children():
            widget.destroy()

        reminders = self.reminders_data.get_user_data(self.current_user, [])
        if not reminders:
            ctk.CTkLabel(self.reminder_scroll_frame, text="No reminders set yet! Add a new reminder.", text_color=TEXT_COLOR, font=FONT_BODY).pack(pady=20)
            return

        for i, reminder_data in enumerate(reminders):
            reminder_frame = ctk.CTkFrame(self.reminder_scroll_frame, fg_color=BG_COLOR, corner_radius=8,
                                          border_width=1, border_color=SHADOW_COLOR)
            reminder_frame.pack(fill="x", pady=5, padx=5)
            reminder_frame.grid_columnconfigure(1, weight=1)

            checkbox = ctk.CTkCheckBox(reminder_frame, text="", fg_color=BUTTON_BG_COLOR,
                                         hover_color=BUTTON_HOVER_COLOR,
                                         checkmark_color=BUTTON_TEXT_COLOR,
                                         border_color=BUTTON_BG_COLOR, border_width=2,
                                         command=lambda idx=i: self.toggle_reminder_selection(idx))
            checkbox.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
            if reminder_data.get('selected_for_action', False):
                checkbox.select()
            else:
                checkbox.deselect()
            
            # Display time in a readable format
            try:
                dt_obj = datetime.fromisoformat(reminder_data['datetime'])
                display_time = dt_obj.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                display_time = "Invalid Date/Time"

            status_color = ACCENT_COLOR_1 if reminder_data['status'] == "dismissed" else ACCENT_COLOR_3
            if reminder_data['status'] == "dismissed":
                text_content = f"<s>[{display_time}] {reminder_data['message']}</s>"
            else:
                text_content = f"[{display_time}] {reminder_data['message']}"

            reminder_text_label = ctk.CTkLabel(reminder_frame, text=text_content,
                                               font=FONT_BODY, text_color=TEXT_COLOR)
            if reminder_data['status'] == "dismissed":
                reminder_text_label.configure(text_color="gray", font=(FONT_BODY[0], FONT_BODY[1], "overstrike"))
            else:
                reminder_text_label.configure(text_color=TEXT_COLOR, font=FONT_BODY)
            reminder_text_label.grid(row=0, column=1, sticky="w", padx=(0, 10))

            status_label = ctk.CTkLabel(reminder_frame, text=reminder_data['status'].capitalize(),
                                         font=FONT_SMALL_BOLD, text_color=status_color)
            status_label.grid(row=0, column=2, padx=(0, 10), sticky="e")


    def toggle_reminder_selection(self, index):
        reminders = self.reminders_data.get_user_data(self.current_user, [])
        if 0 <= index < len(reminders):
            reminders[index]['selected_for_action'] = not reminders[index].get('selected_for_action', False)
            self.reminders_data.set_user_data(self.current_user, reminders)
            self.refresh_reminder_list()

    def delete_selected_reminders(self):
        reminders = self.reminders_data.get_user_data(self.current_user, [])
        reminders_to_keep = []
        deleted_count = 0
        for reminder in reminders:
            if not reminder.get('selected_for_action', False):
                reminders_to_keep.append(reminder)
            else:
                deleted_count += 1
        
        if deleted_count == 0:
            messagebox.showwarning("No Selection", "Please select reminders to delete.", icon="warning")
            return

        self.reminders_data.set_user_data(self.current_user, reminders_to_keep)
        self.refresh_reminder_list()
        messagebox.showinfo("Success", f"{deleted_count} reminder(s) deleted successfully!", icon="info")
        
        # Also remove from active_reminders if deleted
        for rem_id in list(self.active_reminders.keys()):
            if rem_id not in [r['id'] for r in reminders_to_keep]:
                del self.active_reminders[rem_id]


    def start_reminder_checker(self):
        if not self._reminder_thread_running:
            self._reminder_thread_running = True
            self._reminder_thread = threading.Thread(target=self._run_reminder_checker_thread, daemon=True)
            self._reminder_thread.start()

    def stop_reminder_checker(self):
        self._reminder_thread_running = False
        if self._reminder_thread and self._reminder_thread.is_alive():
            # Join with a timeout to prevent hanging, though daemon ensures exit
            self._reminder_thread.join(timeout=1) 
        self.active_reminders.clear() # Clear active reminders on stop

    def _run_reminder_checker_thread(self):
        while self._reminder_thread_running:
            self.check_reminders()
            time.sleep(1) # Check every second

    def check_reminders(self):
        reminders = self.reminders_data.get_user_data(self.current_user, [])
        now = datetime.now()

        for reminder in reminders:
            if reminder['status'] == 'active':
                reminder_id = reminder['id']
                try:
                    reminder_time = datetime.fromisoformat(reminder['datetime'])
                    # Check if reminder time is in the past or now
                    if reminder_time <= now and reminder_id not in self.active_reminders:
                        self.active_reminders[reminder_id] = reminder # Add to active
                        self.app.after(0, self.show_reminder_popup, reminder) # Show popup on main thread
                except ValueError:
                    print(f"Warning: Could not parse datetime format for ID {reminder.get('id')}")
                    # Optionally, mark this reminder as invalid or dismissed if parsing fails

    def show_reminder_popup(self, reminder_data):
        winsound.Beep(2500, 500) # Play a buzzing sound
        popup_window = ctk.CTkToplevel(self.app)
        popup_window.title("Reminder!")
        popup_window.geometry("400x180")
        popup_window.configure(fg_color=ACCENT_COLOR_4)
        popup_window.transient(self.app)
        popup_window.grab_set()

        ctk.CTkLabel(popup_window, text="🔔 REMINDER!", font=FONT_MEDIUM, text_color=BUTTON_TEXT_COLOR).pack(pady=15)
        ctk.CTkLabel(popup_window, text=reminder_data['message'], font=FONT_BODY, text_color=BUTTON_TEXT_COLOR, wraplength=350).pack(pady=(0, 10))

        def dismiss_reminder():
            if reminder_data['id'] in self.active_reminders:
                # Update status in persistent data
                current_reminders = self.reminders_data.get_user_data(self.current_user, [])
                for r in current_reminders:
                    if r['id'] == reminder_data['id']:
                        r['status'] = 'dismissed'
                        break
                self.reminders_data.set_user_data(self.current_user, current_reminders)
                del self.active_reminders[reminder_data['id']]
            popup_window.destroy()
            self.refresh_reminder_list() # Refresh the list to show dismissed status

        ctk.CTkButton(popup_window, text="Dismiss", command=dismiss_reminder,
                         fg_color=BUTTON_BG_COLOR, hover_color=BUTTON_HOVER_COLOR,
                          text_color=BUTTON_TEXT_COLOR, font=FONT_BUTTON, corner_radius=10).pack(pady=10)
        
        popup_window.protocol("WM_DELETE_WINDOW", dismiss_reminder) # Dismiss reminder if window is closed by user

if __name__ == "__main__":
    app = StudentGuideApp()

