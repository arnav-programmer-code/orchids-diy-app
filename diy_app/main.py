import customtkinter as ctk
import json
import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime

# Set theme and color scheme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class InventoryApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("DIY Lab Inventory Management")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#FFFFFF")

        # Initialize data files
        self.init_data_files()

        # make it full screen
        self.root.attributes("-fullscreen", True)

        # Current user
        self.current_user = None

        # Load logo
        self.load_logo()

        # Start with login screen
        self.show_login_screen()

    def load_component_image(self, image_path):
        """Load and return a CTkImage for component display"""
        try:
            if os.path.exists(image_path):
                component_image = Image.open(image_path)
                component_image = component_image.resize((120, 80), Image.Resampling.LANCZOS)
                return ctk.CTkImage(light_image=component_image, size=(120, 80))
            else:
                return None
        except Exception as e:
            print(f"Error loading component image {image_path}: {e}")
            return None

    def load_logo(self):
        try:
            if os.path.exists("logo.png"):
                logo_image = Image.open("logo.png")
                logo_image = logo_image.resize((120, 120), Image.Resampling.LANCZOS)
                self.logo = ctk.CTkImage(light_image=logo_image, size=(120, 120))
            else:
                self.logo = None
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.logo = None

    def init_data_files(self):
        # Initialize users.json
        if not os.path.exists("users.json"):
            with open("users.json", "w") as f:
                json.dump({}, f)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_alert(self, title, message):
        alert_window = ctk.CTkToplevel(self.root)
        alert_window.title(title)
        alert_window.resizable(False, False)
        alert_window.geometry("450x250")
        alert_window.configure(fg_color="#FFFFFF")
        alert_window.attributes("-topmost", True)
        
        
        # Outer frame with shadow effect
        outer_frame = ctk.CTkFrame(alert_window, fg_color="#FFFFFF", corner_radius=15)
        outer_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Alert content with gradient-like design
        alert_frame = ctk.CTkFrame(outer_frame, fg_color="#DC143C", corner_radius=15, 
                                   border_width=2, border_color="#9e0e26")
        alert_frame.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Icon based on alert type
        icon_text = "✓" if title.lower() == "success" else "❌"
        icon_label = ctk.CTkLabel(alert_frame, text=icon_text, font=ctk.CTkFont(size=40),
                               text_color="white")
        icon_label.pack(pady=(20, 5))
        
        # Title with shadow effect
        shadow_title = ctk.CTkLabel(alert_frame, text=title.upper(), font=ctk.CTkFont(size=22, weight="bold"),
                                  text_color="#9e0e26")
        shadow_title.place(relx=0.5, y=83, anchor="center")
        
        title_label = ctk.CTkLabel(alert_frame, text=title.upper(), font=ctk.CTkFont(size=22, weight="bold"),
                                 text_color="white")
        title_label.place(relx=0.5, y=80, anchor="center")
        
        # Divider line
        divider_frame = ctk.CTkFrame(alert_frame, height=2, fg_color="#FFFFFF", width=350)
        divider_frame.place(relx=0.5, y=105, anchor="center")
        
        # Message with better styling
        message_label = ctk.CTkLabel(alert_frame, text=message, font=ctk.CTkFont(size=14), 
                                   text_color="white", wraplength=350, justify="center")
        message_label.place(relx=0.5, y=145, anchor="center")
        
        # Sleek, modern button
        ok_button = ctk.CTkButton(alert_frame, text="OK", command=alert_window.destroy,
                                fg_color="#FFFFFF", text_color="#DC143C", 
                                hover_color="#f8f8f8", width=120, height=35,
                                corner_radius=20, font=ctk.CTkFont(size=14, weight="bold"))
        ok_button.place(relx=0.5, y=195, anchor="center")
        
        # Add animation effect (fade in)
        alert_window.attributes("-alpha", 0.0)
        for i in range(1, 11):
            alert_window.attributes("-alpha", i/10)
            alert_window.update()
            alert_window.after(20)

    def show_login_screen(self):
        self.clear_window()

        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#FFFFFF")
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#DC143C", height=280)
        header_frame.pack(fill="x", padx=0, pady=0)

        # Title (now on the left)
        shadow_label = ctk.CTkLabel(header_frame, text="DIY LAB INVENTORY MANAGEMENT",
                                  font=ctk.CTkFont(size=50, weight="bold", family="Impact"), 
                                  text_color="#9e0e26")
        shadow_label.place(x=50, y=103)
        
        title_label = ctk.CTkLabel(header_frame, text="DIY LAB INVENTORY MANAGEMENT",
                                  font=ctk.CTkFont(size=50, weight="bold", family="Impact"), 
                                  text_color="#9e0e26")
        title_label.place(x=50, y=103)

        title_label = ctk.CTkLabel(header_frame, text="DIY LAB INVENTORY MANAGEMENT",
                                  font=ctk.CTkFont(size=50, weight="bold", family="Impact"), 
                                  text_color="white")
        title_label.place(x=47, y=100)

        # Logo on the right
        if self.logo:
            logo_label = ctk.CTkLabel(header_frame, image=self.logo, text="")
            logo_label.place(relx=0.95, y=100, anchor="e")  # relx=0.95 places it at 95% from left

        # Login form 
        login_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=30, 
                                  border_width=2, border_color="#DC143C")
        login_frame.pack(pady=50, padx=200, ipady=15, ipadx=15)
        
        
        # Login title
        login_title = ctk.CTkLabel(login_frame, text="LOGIN", 
                                  font=ctk.CTkFont(size=36, weight="bold", family="Franklin Gothic Heavy"),
                                  text_color="#DC143C")
        login_title.pack(pady=(40, 20))

        # Username field 
        username_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        username_frame.pack(pady=10)
        
        username_icon = ctk.CTkLabel(username_frame, text="👤", font=ctk.CTkFont(size=20))
        username_icon.pack(side="left", padx=(0, 10))
        
        self.username_entry = ctk.CTkEntry(username_frame, placeholder_text="Username", width=300, height=45,
                                         font=ctk.CTkFont(size=16), border_color="#DC143C", 
                                         corner_radius=15)
        self.username_entry.pack(side="left")

        # Password field
        password_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        password_frame.pack(pady=10)
        
        password_icon = ctk.CTkLabel(password_frame, text="🔒", font=ctk.CTkFont(size=20))
        password_icon.pack(side="left", padx=(0, 10))
        
        self.password_entry = ctk.CTkEntry(password_frame, placeholder_text="Password", show="•", width=300, height=45,
                                         font=ctk.CTkFont(size=16), border_color="#DC143C",
                                         corner_radius=15)
        self.password_entry.pack(side="left")

        # Login button
        login_button = ctk.CTkButton(login_frame, text="LOGIN", command=self.login, width=350, height=50,
                                   fg_color="#DC143C", hover_color="#FF1744", corner_radius=25,
                                   font=ctk.CTkFont(size=18, weight="bold"))
        login_button.pack(pady=25)

        # Register link with better styling
        register_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        register_frame.pack(pady=(5, 35))
        
        register_text = ctk.CTkLabel(register_frame, text="Don't have an account? ", text_color="#555555", 
                                    font=ctk.CTkFont(size=14))
        register_text.pack(side="left")
        
        register_button = ctk.CTkButton(register_frame, text="Register here", 
                  text_color="#DC143C",
                  fg_color="transparent", 
                  hover_color="#ffffff",
                  font=ctk.CTkFont(size=14, underline=True, weight="bold"),
                  command=self.show_register_screen,
                  width=80,
                  height=25)
        register_button.pack(side="left")
        
    def show_register_screen(self):
        self.clear_window()

        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#FFFFFF")
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#DC143C", height=200)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        if self.logo:
            logo_label = ctk.CTkLabel(header_frame, image=self.logo, text="")
            logo_label.place(x=50, y=40)

        # Title
        title_label = ctk.CTkLabel(header_frame, text="CREATE NEW ACCOUNT",
                                  font=ctk.CTkFont(size=40, weight="bold", family="Impact"), 
                                  text_color="#9e0e26")
        title_label.place(x=203, y=83)

        title_label = ctk.CTkLabel(header_frame, text="CREATE NEW ACCOUNT",
                                  font=ctk.CTkFont(size=40, weight="bold", family="Impact"), 
                                  text_color="white")
        title_label.place(x=200, y=80)

        # Register form with enhanced styling
        register_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=30, 
                                    border_width=2, border_color="#DC143C")
        register_frame.pack(pady=40, padx=200, ipady=20, ipadx=20)

        register_title = ctk.CTkLabel(register_frame, text="REGISTER", 
                                    font=ctk.CTkFont(size=32, weight="bold", family="Franklin Gothic Heavy"),
                                    text_color="#DC143C")
        register_title.pack(pady=(30, 25))

        # Teacher Name field
        teacher_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
        teacher_frame.pack(pady=8)
        
        teacher_icon = ctk.CTkLabel(teacher_frame, text="👨", font=ctk.CTkFont(size=20))
        teacher_icon.pack(side="left", padx=(0, 10))
        
        self.teacher_name_entry = ctk.CTkEntry(teacher_frame, placeholder_text="Teacher Name", width=300, height=45,
                                             font=ctk.CTkFont(size=16), border_color="#DC143C", 
                                             corner_radius=15)
        self.teacher_name_entry.pack(side="left")

        # Branch Name field
        branch_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
        branch_frame.pack(pady=8)
        
        branch_icon = ctk.CTkLabel(branch_frame, text="🏫", font=ctk.CTkFont(size=20))
        branch_icon.pack(side="left", padx=(0, 10))
        
        self.branch_name_entry = ctk.CTkEntry(branch_frame, placeholder_text="Branch Name", width=300, height=45,
                                            font=ctk.CTkFont(size=16), border_color="#DC143C", 
                                            corner_radius=15)
        self.branch_name_entry.pack(side="left")

        # Username field
        username_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
        username_frame.pack(pady=8)
        
        username_icon = ctk.CTkLabel(username_frame, text="👤", font=ctk.CTkFont(size=20))
        username_icon.pack(side="left", padx=(0, 10))
        
        self.reg_username_entry = ctk.CTkEntry(username_frame, placeholder_text="Username", width=300, height=45,
                                             font=ctk.CTkFont(size=16), border_color="#DC143C", 
                                             corner_radius=15)
        self.reg_username_entry.pack(side="left")

        # Password field
        password_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
        password_frame.pack(pady=8)
        
        password_icon = ctk.CTkLabel(password_frame, text="🔒", font=ctk.CTkFont(size=20))
        password_icon.pack(side="left", padx=(0, 10))
        
        self.reg_password_entry = ctk.CTkEntry(password_frame, placeholder_text="Password", show="•", width=300, height=45,
                                             font=ctk.CTkFont(size=16), border_color="#DC143C",
                                             corner_radius=15)
        self.reg_password_entry.pack(side="left")

        # Register button
        register_button = ctk.CTkButton(register_frame, text="CREATE ACCOUNT", command=self.register, 
                                      width=350, height=50, fg_color="#DC143C", hover_color="#FF1744", 
                                      corner_radius=25, font=ctk.CTkFont(size=18, weight="bold"))
        register_button.pack(pady=25)

        # Back to login
        login_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
        login_frame.pack(pady=(5, 30))
        
        back_text = ctk.CTkLabel(login_frame, text="Already have an account? ", text_color="#555555", 
                               font=ctk.CTkFont(size=14))
        back_text.pack(side="left")
        
        back_button = ctk.CTkButton(login_frame, text="Login here", 
                      text_color="#DC143C",
                      fg_color="transparent", 
                      hover_color="#ffffff",
                      font=ctk.CTkFont(size=14, underline=True, weight="bold"),
                      command=self.show_login_screen,
                      width=80,
                      height=25)
        back_button.pack(side="left")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.show_alert("Error", "Please enter both username and password")
            return

        try:
            with open("users.json", "r") as f:
                users = json.load(f)

            if username in users and users[username]["password"] == password:
                self.current_user = users[username]["teacher_name"]
                self.show_inventory_screen()
            else:
                self.show_alert("Error", "Invalid username or password")
        except Exception as e:
            self.show_alert("Error", f"Login failed: {str(e)}")

    def register(self):
        teacher_name = self.teacher_name_entry.get().strip()
        branch_name = self.branch_name_entry.get().strip()
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()

        if not all([teacher_name, branch_name, username, password]):
            self.show_alert("Error", "Please fill in all fields")
            return

        try:
            with open("users.json", "r") as f:
                users = json.load(f)

            if username in users:
                self.show_alert("Error", "Username already exists")
                return

            users[username] = {
                "teacher_name": teacher_name,
                "branch_name": branch_name,
                "password": password
            }

            with open("users.json", "w") as f:
                json.dump(users, f, indent=2)

            self.show_alert("Success", "Registration successful! Please login.")
            self.show_login_screen()
        except Exception as e:
            self.show_alert("Error", f"Registration failed: {str(e)}")

    def show_inventory_screen(self):
        self.clear_window()

        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#FFFFFF")
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#DC143C", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        if self.logo:
            logo_label = ctk.CTkLabel(header_frame, image=self.logo, text="")
            logo_label.pack(side="left", padx=20, pady=15)

        title_label = ctk.CTkLabel(header_frame, text=f"INVENTORY - Welcome, {self.current_user}",
                                   font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        title_label.pack(side="left", padx=20, pady=15)

        # Button frame
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=20, pady=15)

        generate_button = ctk.CTkButton(button_frame, text="EXPORT TO PDF", command=self.generate_and_export_report,
                                        fg_color="white", text_color="#DC143C", hover_color="#f0f0f0", width=120)
        generate_button.pack(side="left", padx=(0, 10))

        logout_button = ctk.CTkButton(button_frame, text="LOGOUT", command=self.show_login_screen,
                                      fg_color="white", text_color="#DC143C", hover_color="#f0f0f0", width=80)
        logout_button.pack(side="left")

        # Scrollable frame for inventory
        scrollable_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Load inventory data
        try:
            with open("inventory.json", "r") as f:
                inventory = json.load(f)

            row = 0
            for component_name, data in inventory.items():
                self.create_component_row(scrollable_frame, component_name, data, row)
                row += 1

        except Exception as e:
            error_label = ctk.CTkLabel(scrollable_frame, text=f"Error loading inventory: {str(e)}",
                                       text_color="#DC143C", font=ctk.CTkFont(size=16))
            error_label.pack(pady=50)

    def create_component_row(self, parent, component_name, data, row):
        # Component frame 
        component_frame = ctk.CTkFrame(parent, fg_color="#f9f9f9", corner_radius=15, border_width=2,
                                       border_color="#DC143C")
        component_frame.pack(fill="x", pady=15, padx=20, ipady=10)

        # Left side - Image and name with better styling
        left_frame = ctk.CTkFrame(component_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)

        # Component image with sleek rounded design
        image_frame = ctk.CTkFrame(left_frame, width=150, height=100, fg_color="#DC143C", 
                                  corner_radius=15)
        image_frame.pack(pady=(0, 12))
        image_frame.pack_propagate(False)

        # Try to load the actual image
        component_image = None
        image_url = data.get('image_url', '')

        # Check if it's a local file
        if image_url and not image_url.startswith('http'):
            component_image = self.load_component_image(image_url)

        if component_image:
            image_label = ctk.CTkLabel(image_frame, image=component_image, text="")
            image_label.pack(expand=True)
        else:
            # Stylish placeholder with icon
            image_label = ctk.CTkLabel(image_frame, text="📷\nCOMPONENT", text_color="white", 
                                      font=ctk.CTkFont(size=14, weight="bold"))
            image_label.pack(expand=True)

        # Component name with stylish badge look
        name_badge = ctk.CTkFrame(left_frame, fg_color="#DC143C", corner_radius=10)
        name_badge.pack(fill="x")
        name_label = ctk.CTkLabel(name_badge, text=component_name, 
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 text_color="white", wraplength=150)
        name_label.pack(padx=10, pady=8)

        # Right side - Input fields with modern styling
        right_frame = ctk.CTkFrame(component_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=15)

        # Create a grid of input fields with better spacing
        fields_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        fields_frame.pack(fill="x")

        # Quantity in Hand with icon and better styling
        qty_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        qty_frame.grid(row=0, column=0, padx=15, pady=8, sticky="w")
        qty_label_frame = ctk.CTkFrame(qty_frame, fg_color="transparent")
        qty_label_frame.pack(anchor="w", fill="x")
        ctk.CTkLabel(qty_label_frame, text="🔢", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0,5))
        ctk.CTkLabel(qty_label_frame, text="Quantity in Hand:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        qty_entry = ctk.CTkEntry(qty_frame, width=220, height=35, 
                               corner_radius=10, border_color="#DC143C", 
                               font=ctk.CTkFont(size=14))
        qty_entry.pack(pady=(5,0))
        qty_entry.insert(0, str(data["quantity_in_hand"]))

        # Number Working with icon and better styling
        working_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        working_frame.grid(row=0, column=1, padx=15, pady=8, sticky="w")
        working_label_frame = ctk.CTkFrame(working_frame, fg_color="transparent")
        working_label_frame.pack(anchor="w", fill="x")
        ctk.CTkLabel(working_label_frame, text="✅", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0,5))
        ctk.CTkLabel(working_label_frame, text="Number Working:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        working_entry = ctk.CTkEntry(working_frame, width=220, height=35, 
                                   corner_radius=10, border_color="#26a69a", 
                                   font=ctk.CTkFont(size=14))
        working_entry.pack(pady=(5,0))
        working_entry.insert(0, str(data["number_working"]))

        # Number Not Working with icon and better styling
        not_working_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        not_working_frame.grid(row=1, column=0, padx=15, pady=8, sticky="w")
        not_working_label_frame = ctk.CTkFrame(not_working_frame, fg_color="transparent")
        not_working_label_frame.pack(anchor="w", fill="x")
        ctk.CTkLabel(not_working_label_frame, text="❌", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0,5))
        ctk.CTkLabel(not_working_label_frame, text="Number Not Working:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        not_working_entry = ctk.CTkEntry(not_working_frame, width=220, height=35, 
                                       corner_radius=10, border_color="#ef5350", 
                                       font=ctk.CTkFont(size=14))
        not_working_entry.pack(pady=(5,0))
        not_working_entry.insert(0, str(data["number_not_working"]))

        # Reason with icon and better styling
        reason_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        reason_frame.grid(row=1, column=1, padx=15, pady=8, sticky="w")
        reason_label_frame = ctk.CTkFrame(reason_frame, fg_color="transparent")
        reason_label_frame.pack(anchor="w", fill="x")
        ctk.CTkLabel(reason_label_frame, text="📝", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0,5))
        ctk.CTkLabel(reason_label_frame, text="Reason:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        reason_entry = ctk.CTkEntry(reason_frame, width=220, height=35, 
                                  corner_radius=10, border_color="#9575cd", 
                                  font=ctk.CTkFont(size=14))
        reason_entry.pack(pady=(5,0))
        reason_entry.insert(0, data["reason"])

        # Modern gradient save button with animation effect
        save_button_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        save_button_frame.grid(row=0, column=2, padx=25, pady=5, rowspan=2)
        
        save_button = ctk.CTkButton(save_button_frame, text="SAVE CHANGES", 
                                  command=lambda: self.save_component_data(component_name, qty_entry, working_entry,
                                                                         not_working_entry, reason_entry),
                                  fg_color="#DC143C", hover_color="#B71C1C", 
                                  corner_radius=25, width=150, height=50,
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  border_width=2, border_color="#f8d7da")
        save_button.pack(pady=10)
        
        # Add status indicator
        status_label = ctk.CTkLabel(save_button_frame, text="Last updated: Today", 
                                  text_color="#888888", font=ctk.CTkFont(size=10))
        status_label.pack()

    def save_component_data(self, component_name, qty_entry, working_entry, not_working_entry, reason_entry):
        try:
            # Get current values
            new_qty = int(qty_entry.get() or 0)
            new_working = int(working_entry.get() or 0)
            new_not_working = int(not_working_entry.get() or 0)
            new_reason = reason_entry.get().strip()

            # Load current inventory
            with open("inventory.json", "r") as f:
                inventory = json.load(f)

            # Check if not working increased
            old_not_working = inventory[component_name]["number_not_working"]
            if new_not_working > old_not_working:
                self.show_alert("Alert",
                                f"Warning: Number of non-working {component_name} increased from {old_not_working} to {new_not_working}!")

            # Update data
            inventory[component_name].update({
                "quantity_in_hand": new_qty,
                "number_working": new_working,
                "number_not_working": new_not_working,
                "reason": new_reason
            })

            # Save to file
            with open("inventory.json", "w") as f:
                json.dump(inventory, f, indent=2)

            self.show_alert("Success", f"Data saved successfully for {component_name}!")

        except ValueError:
            self.show_alert("Error", "Please enter valid numbers for quantity fields")
        except Exception as e:
            self.show_alert("Error", f"Failed to save data: {str(e)}")

    def generate_and_export_report(self):
        try:
            # Load current inventory
            with open("inventory.json", "r") as f:
                inventory = json.load(f)

            # Generate timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"inventory_report_{timestamp}.pdf"

            # Create report data
            report_data = {
                "generated_by": self.current_user,
                "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "inventory_data": inventory.copy()
            }

            # Generate PDF directly
            self.create_pdf_report(report_data, pdf_filename)

            self.show_alert("Success", f"Inventory report exported successfully!\nPDF saved as: {pdf_filename}")

        except Exception as e:
            self.show_alert("Error", f"Failed to export report: {str(e)}")

    def create_pdf_report(self, report_data, filename):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#DC143C'),
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("DIY LAB INVENTORY REPORT", title_style))

        # Report info
        info_style = ParagraphStyle(
            'CustomInfo',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.HexColor('#333333')
        )

        story.append(Paragraph(f"<b>Report Title:</b> DIY Lab Inventory Status", info_style))
        story.append(Paragraph(f"<b>Generated By:</b> {report_data['generated_by']}", info_style))
        story.append(Paragraph(f"<b>Generated Date:</b> {report_data['generated_date']}", info_style))
        story.append(Spacer(1, 20))

        # Inventory table
        table_data = [['Component Name', 'Qty in Hand', 'Working', 'Not Working', 'Reason']]

        for component, data in report_data['inventory_data'].items():
            table_data.append([
                component[:30] + '...' if len(component) > 30 else component,
                str(data['quantity_in_hand']),
                str(data['number_working']),
                str(data['number_not_working']),
                data['reason'][:20] + '...' if len(data['reason']) > 20 else data['reason']
            ])

        table = Table(table_data, colWidths=[3 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC143C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))

        story.append(table)
        story.append(Spacer(1, 20))

        # Summary
        total_components = len(report_data['inventory_data'])
        total_qty = sum(data['quantity_in_hand'] for data in report_data['inventory_data'].values())
        total_working = sum(data['number_working'] for data in report_data['inventory_data'].values())
        total_not_working = sum(data['number_not_working'] for data in report_data['inventory_data'].values())

        summary_style = ParagraphStyle(
            'CustomSummary',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=5,
            textColor=colors.HexColor('#DC143C'),
            leftIndent=20
        )

        story.append(Paragraph("<b>SUMMARY:</b>", title_style))
        story.append(Paragraph(f"Total Components: {total_components}", summary_style))
        story.append(Paragraph(f"Total Quantity: {total_qty}", summary_style))
        story.append(Paragraph(f"Total Working: {total_working}", summary_style))
        story.append(Paragraph(f"Total Not Working: {total_not_working}", summary_style))

        doc.build(story)

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = InventoryApp()
    app.run()