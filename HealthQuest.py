#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import random
import json
from datetime import datetime

# Global SQL credentials
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_PASSWORD = 'Firepower#132'
SQL_DATABASE = 'healthquest'

class QuestApp:
    def __init__(self, root):
        self.root = root
        self.quests = self.fetch_all_quests()  # Prefetch all quests
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Health Quest")
        self.root.geometry("360x640")

        # Notebook (tab control)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", side=tk.TOP)
    
        # Quests tab
        self.quests_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.quests_tab, text='Quests')
    
        # Initialize dynamic_widgets_frame within quests_tab for custom UIs
        self.dynamic_widgets_frame = tk.Frame(self.quests_tab)
        self.dynamic_widgets_frame.pack(pady=20)
    
        # Profile tab
        self.profile_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.profile_tab, text='Profile')
        self.setup_profile_tab()

        # Generate Random Quest button
        self.generate_quest_btn = tk.Button(self.root, text="Generate Random Quest", command=self.display_random_quest)
        self.generate_quest_btn.pack(side=tk.BOTTOM, pady=10)
    
        # Quest Display Area
        self.quest_display = tk.Text(self.quests_tab, height=10, width=50, state=tk.DISABLED)
        self.quest_display.pack(pady=10)


    def fetch_all_quests(self):
        # Fetch all quests from your database or predefined list
        # Placeholder for database fetching logic
        return [
            (1, 'boolean', 'Do you exercise daily?'),
            (2, 'timer', 'Time your meditation session.'),
            (3, 'counting', 'Count glasses of water drunk today.'),
        ]

    def display_random_quest(self):
        self.clear_quest_display_area()
        quest = random.choice(self.quests)
        self.current_quest = quest
        quest_info = f"ID: {quest[0]}\nType: {quest[1]}\nBody: {quest[2]}"
        self.quest_display.config(state=tk.NORMAL)
        self.quest_display.insert(tk.END, quest_info)
        self.quest_display.config(state=tk.DISABLED)

        # Display interface based on qtype
        if quest[1] == 'boolean':
            self.display_boolean_interface()
        elif quest[1] == 'timer':
            self.display_timer_interface()
        elif quest[1] == 'counting':
            self.display_counting_interface()

    def clear_quest_display_area(self):
        # Clear any dynamic widgets from a previous quest
        for widget in self.quests_tab.winfo_children():
            if widget != self.quest_display:
                widget.destroy()

    def display_boolean_interface(self):
        self.boolean_var = tk.BooleanVar(value=True)  # Default value

        tk.Radiobutton(self.dynamic_widgets_frame, text="True", variable=self.boolean_var, value=True).pack(side=tk.LEFT)
        tk.Radiobutton(self.dynamic_widgets_frame, text="False", variable=self.boolean_var, value=False).pack(side=tk.LEFT)

        self.add_submit_button("boolean")

    def display_timer_interface(self):
        # Timer quest interface with Start and Stop buttons
        self.timer_start_time = None
        self.timer_end_time = None
        self.timer_label = tk.Label(self.dynamic_widgets_frame, text="0 s")
        self.timer_label.pack()

        start_btn = tk.Button(self.dynamic_widgets_frame, text="Start", command=self.start_timer)
        start_btn.pack(side=tk.LEFT)

        stop_btn = tk.Button(self.dynamic_widgets_frame, text="Stop", command=self.stop_timer)
        stop_btn.pack(side=tk.LEFT)

        self.add_submit_button("timer")

    def display_counting_interface(self):
        # Counting quest interface with an Entry widget
        self.count_var = tk.IntVar(value=0)
        count_entry = tk.Entry(self.dynamic_widgets_frame, textvariable=self.count_var)
        count_entry.pack()
        
        self.add_submit_button("counting")
    def add_submit_button(self, quest_type):
        submit_btn = tk.Button(self.dynamic_widgets_frame, text="Submit", command=lambda: self.submit_quest(quest_type))
        submit_btn.pack(side=tk.BOTTOM, pady=10)

    def submit_quest(self, quest_type):
        if quest_type == "boolean":
            result = str(self.boolean_var.get())
        elif quest_type == "timer":
            if self.timer_start_time and self.timer_end_time:
                elapsed_time = (self.timer_end_time - self.timer_start_time).total_seconds()
                result = f"{elapsed_time} s"
            else:
                messagebox.showerror("Error", "Timer has not been started/stopped properly.")
                return
        elif quest_type == "counting":
            result = str(self.count_var.get())

        self.log_quest_result(self.current_quest, result)

    def log_quest_result(self, quest, result):
        profile_id = "1"  # Example profile ID, replace with actual dynamic profile ID logic
        log_file_name = f"{profile_id}_log.json"
        entry = {
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "quest_type": quest[1],
            "qiod": quest[0],
            "description": quest[2],
            "results": result
        }

        try:
            with open(log_file_name, "r") as file:
                logs = json.load(file)
        except FileNotFoundError:
            logs = []

        logs.append(entry)
        with open(log_file_name, "w") as file:
            json.dump(logs, file, indent=4)

        messagebox.showinfo("Quest Completed", "Your quest result has been saved.")

    def start_timer(self):
        if self.timer_start_time:
            self.timer_end_time = datetime.now()
            elapsed_time = (self.timer_end_time - self.timer_start_time).total_seconds()
            self.timer_label.config(text=f"{elapsed_time} s")

    def save_quest_result(self, result):
        # Placeholder for saving quest results to logs
        pass

    def setup_profile_tab(self):
        # Basic Profile Information
        profile_info_frame = tk.Frame(self.profile_tab)
        profile_info_frame.pack(pady=10)

        tk.Label(profile_info_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(profile_info_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(profile_info_frame, text="Age:").grid(row=1, column=0, sticky="w")
        self.age_entry = tk.Entry(profile_info_frame)
        self.age_entry.grid(row=1, column=1, sticky="ew")

        # Assuming diseases are predefined and static, you can create checkboxes for them
        diseases_frame = tk.Frame(self.profile_tab)
        diseases_frame.pack(pady=10)
        tk.Label(diseases_frame, text="Chronic Diseases:").pack(anchor="w")

        self.diseases_vars = {}
        diseases = ["Diabetes", "Hypertension", "Heart Disease", "Asthma", "COPD", "Arthritis"]
        for disease in diseases:
            self.diseases_vars[disease] = tk.BooleanVar()
            tk.Checkbutton(diseases_frame, text=disease, variable=self.diseases_vars[disease]).pack(anchor="w")

        # Medications
        medications_frame = tk.Frame(self.profile_tab)
        medications_frame.pack(pady=10)
        tk.Label(medications_frame, text="Medications:").pack(anchor="w")
        self.medications_text = tk.Text(medications_frame, height=4, width=50)
        self.medications_text.pack()
        
        
    
    def fetch_profiles(self):
        profiles = []
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='SQL_USER',
                password='SQL_PASSWORD',
                database='SQL_DATABASE'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT profile_id, name, age FROM profiles")
            for profile_id, name, age in cursor:
                profiles.append((profile_id, name, age))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn and conn.is_connected():
                conn.close()
        return profiles

    def add_new_profile(self):
        # Simple dialog to input name and age
        name = simpledialog.askstring("New Profile", "Enter profile name:")
        age = simpledialog.askstring("New Profile", "Enter profile age:")
        
        if name and age.isdigit():
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user='SQL_USER',
                    password='SQL_PASSWORD',
                    database='SQL_DATABASE'
                )
                cursor = conn.cursor()
                cursor.execute("INSERT INTO profiles (name, age) VALUES (%s, %s)", (name, age))
                conn.commit()
                self.current_user_id = cursor.lastrowid  # Set the newly created profile as the current user
                messagebox.showinfo("Success", "Profile created successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))
            finally:
                if conn and conn.is_connected():
                    conn.close()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid name and age.")
    
        self.update_profile_dropdown()  # Refresh the profile dropdown list
    def add_new_profile(self):
        # Simple dialog to input name and age
        name = simpledialog.askstring("New Profile", "Enter profile name:")
        age = simpledialog.askstring("New Profile", "Enter profile age:")
        
        if name and age.isdigit():
            try:
                conn = mysql.connector.connect(
                host='localhost',
                user='SQL_USER',
                password='SQL_PASSWORD',
                database='SQL_DATABASE'
            )
                cursor = conn.cursor()
                cursor.execute("INSERT INTO profiles (name, age) VALUES (%s, %s)", (name, age))
                conn.commit()
                self.current_user_id = cursor.lastrowid  # Set the newly created profile as the current user
                messagebox.showinfo("Success", "Profile created successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))
            finally:
                if conn and conn.is_connected():
                    conn.close()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid name and age.")
        
        self.update_profile_dropdown()  # Refresh the profile dropdown list

    
    def submit_profile(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        medications = self.medications_text.get("1.0", tk.END).strip()

        if not name or not age.isdigit():
            messagebox.showerror("Error", "Please fill in the name and age correctly.")
            return

        try:
            conn = mysql.connector.connect(
                host=SQL_HOST,
                user=SQL_USER,
                password=SQL_PASSWORD,
                database=SQL_DATABASE
            )
            cursor = conn.cursor()

            cursor.execute("INSERT INTO profiles (name, age) VALUES (%s, %s)", (name, age))
            profile_id = cursor.lastrowid

            for disease, var in self.diseases.items():
                if var.get():
                    cursor.execute("SELECT disease_id FROM chronic_diseases WHERE disease_name = %s", (disease,))
                    disease_result = cursor.fetchone()
                    if disease_result:
                        disease_id = disease_result[0]
                        cursor.execute("INSERT INTO profile_diseases (profile_id, disease_id) VALUES (%s, %s)", (profile_id, disease_id))

            if medications:
                for medication in medications.split(','):
                    medication_name = medication.strip()
                    if medication_name:
                        cursor.execute("INSERT INTO medications (profile_id, medication_name) VALUES (%s, %s)", (profile_id, medication_name))

            conn.commit()
            messagebox.showinfo("Success", "Profile information submitted successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if conn.is_connected():
                conn.close()

    def display_random_quest(self):
        self.clear_quest_display_area()
        quest = random.choice(self.quests)
        self.current_quest = quest
        quest_info = f"ID: {quest[0]}\nType: {quest[1]}\nBody: {quest[2]}"
        self.quest_display.config(state=tk.NORMAL)
        self.quest_display.delete('1.0', tk.END)
        self.quest_display.insert(tk.END, quest_info)
        self.quest_display.config(state=tk.DISABLED)

        # Clear previously dynamic widgets
        for widget in self.dynamic_widgets_frame.winfo_children():
            widget.destroy()

        # Display interface based on qtype
        if quest[1] == 'boolean':
            self.display_boolean_interface()
        elif quest[1] == 'timer':
            self.display_timer_interface()
        elif quest[1] == 'counting':
            self.display_counting_interface()
            
    def fetch_all_quests(self):
        quests = []
        try:
            conn = mysql.connector.connect(
                host=SQL_HOST,
                user=SQL_USER,
                password=SQL_PASSWORD,
                database=SQL_DATABASE
            )
            cursor = conn.cursor()
            cursor.execute("SELECT qiod, qtype, qbody FROM quests")
            quests = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:setup
            if conn and conn.is_connected():
                conn.close()
        return quests

    # Assuming definitions for display_boolean_interface, display_timer_interface,
    # display_counting_interface, start_timer, end_timer, and save_quest_result methods follow...

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestApp(root)
    root.mainloop()


# In[ ]:




