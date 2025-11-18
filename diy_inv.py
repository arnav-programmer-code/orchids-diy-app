import customtkinter as ctk
import json
import os
from PIL import Image
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.units import inch
from datetime import datetime
import uuid

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
            if os.path.exists("ORCHIDS.png"):
                logo_image = Image.open("ORCHIDS.png")
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

        # Initialize reports.json
        if not os.path.exists("reports.json"):
            with open("reports.json", "w") as f:
                json.dump({"next_report_id": 1, "reports": {}}, f)

        # Initialize inventory.json with actual DIY lab components
        if not os.path.exists("inventory.json"):
            default_components = {
                "Bow arm jig saw machine + 1 plastic box of allen keys": {
                    "image_url": "diy_images/bow arm jigsaw.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Wood turning lathe + 1 plastic box of allen keys": {
                    "image_url": "diy_images/wood turning lathe.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Mini metal milling machine + 1 plastic box of allen keys": {
                    "image_url": "diy_images/milling.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Mini metal drilling machine + 1 plastic box of allen keys": {
                    "image_url": "diy_images/drilling.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Mini metal sanding machine + 1 plastic box of allen keys": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Flexible shaft sanding/Grinding machine + 1 plastic box of allen keys": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Mini metal lathe + 1 plastic box of allen keys": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Hand saw/Bow saw": {
                    "image_url": "diy_images/handsaw.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "C-Clamp": {
                    "image_url": "diy_images/C Clamp.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Pistol Clamp": {
                    "image_url": "diy_images/pistol clamp.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Benchwise": {
                    "image_url": "diy_images/benchwise.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Hand filing tool set": {
                    "image_url": "diy_images/hand filing tool set.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Wood Carving Chisel Set": {
                    "image_url": "diy_images/chisel set.png",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "6 Piece Heavy Duty Wood Carving Chisel Set": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Wire strippers": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Soldering gun": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Solder iron": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Soldering stand": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Flux boxes": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Mini minus screw drivers": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Star screw drivers - Red": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Minus screw drivers - Yellow": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Orange allen key": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Blue allen key": {
                    "image_url": "",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                },
                "Vernier callipers": {
                    "image_url": "https://via.placeholder.com/150x100/DC143C/FFFFFF?text=Vernier+Callipers",
                    "quantity_in_hand": 0,
                    "number_working": 0,
                    "number_not_working": 0,
                    "reason": ""
                }
            }
            with open("inventory.json", "w") as f:
                json.dump(default_components, f, indent=2)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_alert(self, title, message):
        alert_window = ctk.CTkToplevel(self.root)
        alert_window.title(title)
        alert_window.geometry("400x200")
        alert_window.configure(fg_color="#FFFFFF")
        alert_window.attributes("-topmost", True)

        # Center the alert
        alert_window.transient(self.root)
        alert_window.grab_set()

        # Alert content
        alert_frame = ctk.CTkFrame(alert_window, fg_color="#DC143C", corner_radius=10)
        alert_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(alert_frame, text=title, font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color="white", width=120, height=120)
        title_label.pack(pady=(20, 10))

        message_label = ctk.CTkLabel(alert_frame, text=message, font=ctk.CTkFont(size=14), text_color="white",
                                     wraplength=300, width=120, height=120)
        message_label.pack(pady=10)

        ok_button = ctk.CTkButton(alert_frame, text="OK", command=alert_window.destroy,
                                  fg_color="white", text_color="#DC143C", hover_color="#f0f0f0")
        ok_button.pack(pady=(10, 20))

    def show_login_screen(self):
        self.clear_window()

        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#FFFFFF")
        main_frame.pack(fill="both", expand=True)

        # Header with logo
        header_frame = ctk.CTkFrame(main_frame, fg_color="#DC143C", height=240)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        if self.logo:
            logo_label = ctk.CTkLabel(header_frame, image=self.logo, text="")
            logo_label.pack(side="left", padx=20, pady=15)

        title_label = ctk.CTkLabel(header_frame, text="DIY LAB INVENTORY MANAGEMENT",
                                   font=ctk.CTkFont(size=50, weight="bold", family="Franklin Gothic Heavy"), text_color="white")
        title_label.pack(side="left", padx=20, pady=15)

        # Login form container
        login_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=30, border_width=3,
                                   border_color="#DC143C")
        login_frame.pack(pady=50, padx=200)

        # Login title
        login_title = ctk.CTkLabel(login_frame, text="LOGIN", font=ctk.CTkFont(size=28, weight="bold", family="Franklin Gothic Heavy"),
                                   text_color="#DC143C")
        login_title.pack(pady=(30, 20))

        # Username field
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=300, height=40,
                                           font=ctk.CTkFont(size=14), border_color="#DC143C")
        self.username_entry.pack(pady=10)

        # Password field
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", width=300, height=40,
                                           font=ctk.CTkFont(size=14), border_color="#DC143C")
        self.password_entry.pack(pady=10)

        # Login button
        login_button = ctk.CTkButton(login_frame, text="LOGIN", command=self.login, width=300, height=40,
                                     fg_color="#DC143C", hover_color="#B71C1C",
                                     font=ctk.CTkFont(size=16, weight="bold"))
        login_button.pack(pady=15)

        # Register link
        register_label = ctk.CTkLabel(login_frame, text="Don't have an account? Register here",
                                      text_color="#DC143C", font=ctk.CTkFont(size=12, underline=True))
        register_label.pack(pady=(5, 30))
        register_label.bind("<Button-1>", lambda e: self.show_register_screen())

    def show_register_screen(self):
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

        title_label = ctk.CTkLabel(header_frame, text="DIY LAB INVENTORY MANAGEMENT",
                                   font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        title_label.pack(side="left", padx=20, pady=15)

        # Register form
        register_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=15, border_width=2,
                                      border_color="#DC143C")
        register_frame.pack(pady=30, padx=200)

        register_title = ctk.CTkLabel(register_frame, text="REGISTER", font=ctk.CTkFont(size=28, weight="bold"),
                                      text_color="#DC143C")
        register_title.pack(pady=(30, 20))

        # Registration fields
        self.teacher_name_entry = ctk.CTkEntry(register_frame, placeholder_text="Teacher Name", width=300, height=40,
                                               font=ctk.CTkFont(size=14), border_color="#DC143C")
        self.teacher_name_entry.pack(pady=8)

        self.branch_name_entry = ctk.CTkEntry(register_frame, placeholder_text="Branch Name", width=300, height=40,
                                              font=ctk.CTkFont(size=14), border_color="#DC143C")
        self.branch_name_entry.pack(pady=8)

        self.reg_username_entry = ctk.CTkEntry(register_frame, placeholder_text="Username", width=300, height=40,
                                               font=ctk.CTkFont(size=14), border_color="#DC143C")
        self.reg_username_entry.pack(pady=8)

        self.reg_password_entry = ctk.CTkEntry(register_frame, placeholder_text="Password", show="*", width=300,
                                               height=40,
                                               font=ctk.CTkFont(size=14), border_color="#DC143C")
        self.reg_password_entry.pack(pady=8)

        # Register button
        register_button = ctk.CTkButton(register_frame, text="REGISTER", command=self.register, width=300, height=40,
                                        fg_color="#DC143C", hover_color="#B71C1C",
                                        font=ctk.CTkFont(size=16, weight="bold"))
        register_button.pack(pady=15)

        # Back to login
        back_label = ctk.CTkLabel(register_frame, text="Already have an account? Login here",
                                  text_color="#DC143C", font=ctk.CTkFont(size=12, underline=True))
        back_label.pack(pady=(5, 30))
        back_label.bind("<Button-1>", lambda e: self.show_login_screen())

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
        component_frame = ctk.CTkFrame(parent, fg_color="#f8f8f8", corner_radius=10, border_width=1,
                                       border_color="#DC143C")
        component_frame.pack(fill="x", pady=10, padx=10)

        # Left side - Image and name
        left_frame = ctk.CTkFrame(component_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)

        # Component image
        image_frame = ctk.CTkFrame(left_frame, width=120, height=80, fg_color="#DC143C")
        image_frame.pack(pady=(0, 10))
        image_frame.pack_propagate(False)

        # Try to load the actual image
        component_image = None
        image_url = data.get('image_url', '')

        # Check if it's a local file (like bowsaw.jpg)
        if image_url and not image_url.startswith('http'):
            component_image = self.load_component_image(image_url)

        if component_image:
            image_label = ctk.CTkLabel(image_frame, image=component_image, text="")
            image_label.pack(expand=True)
        else:
            # Fallback to placeholder text
            image_label = ctk.CTkLabel(image_frame, text="IMAGE", text_color="white", font=ctk.CTkFont(size=10))
            image_label.pack(expand=True)

        # Component name
        name_label = ctk.CTkLabel(left_frame, text=component_name, font=ctk.CTkFont(size=14, weight="bold"),
                                  text_color="#DC143C", wraplength=150)
        name_label.pack()



        # Right side - Input fields
        right_frame = ctk.CTkFrame(component_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # Create a grid of input fields
        fields_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        fields_frame.pack(fill="x")

        # Quantity in Hand
        qty_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        qty_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(qty_frame, text="Quantity in Hand:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        qty_entry = ctk.CTkEntry(qty_frame, width=100, height=30)
        qty_entry.pack()
        qty_entry.insert(0, str(data["quantity_in_hand"]))

        # Number Working
        working_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        working_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(working_frame, text="Number Working:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        working_entry = ctk.CTkEntry(working_frame, width=100, height=30)
        working_entry.pack()
        working_entry.insert(0, str(data["number_working"]))

        # Number Not Working
        not_working_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        not_working_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(not_working_frame, text="Number Not Working:", font=ctk.CTkFont(size=12, weight="bold")).pack(
            anchor="w")
        not_working_entry = ctk.CTkEntry(not_working_frame, width=100, height=30)
        not_working_entry.pack()
        not_working_entry.insert(0, str(data["number_not_working"]))

        # Reason
        reason_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        reason_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(reason_frame, text="Reason:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        reason_entry = ctk.CTkEntry(reason_frame, width=200, height=30)
        reason_entry.pack()
        reason_entry.insert(0, data["reason"])

        # Save button
        save_button = ctk.CTkButton(fields_frame, text="SAVE",
                                    command=lambda: self.save_component_data(component_name, qty_entry, working_entry,
                                                                             not_working_entry, reason_entry),
                                    fg_color="#DC143C", hover_color="#B71C1C", width=100, height=30)
        save_button.grid(row=0, column=2, padx=20, pady=5, rowspan=2)

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
                "branch_name": current_user_data["branch_name"] if current_user_data else "Unknown",
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
