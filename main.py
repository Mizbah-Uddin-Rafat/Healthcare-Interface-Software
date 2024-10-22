from pathlib import Path
import mysql.connector
import hashlib
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Entry, Text, messagebox, PhotoImage, Frame, ttk, Scrollbar, Label, StringVar
from tkinter.constants import END


# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Fixit#123",
    database="Healthcare"
)
cursor = db.cursor()

# Database Table Classes
class Users:
    @staticmethod
    def authenticate(username, password):
        #hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM Users WHERE username=%s AND password=%s", (username, password))
        return cursor.fetchone()



class Patient:
    @staticmethod
    def search(search_key, field):
            try:
                cursor = db.cursor(dictionary=True)

                valid_fields = ['Patient_ID', 'Patient_FName', 'Patient_LName', 'Patient_Address',
                                'Patient_Phone_Number']
                if field not in valid_fields:
                    raise ValueError(f"Invalid search field: {field}")

                query = f"SELECT * FROM Patient WHERE {field} = %s"
                #cursor.execute(query, (f"%{search_key}%",))
                cursor.execute(query, (search_key,))
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    results.append({
                        'Patient ID': row['Patient_ID'],  # Adjusted column name
                        'First Name': row['Patient_FName'],  # Adjusted column name
                        'Last Name': row['Patient_LName'],  # Adjusted column name
                        'Phone': row['Patient_Phone_Number'],  # Adjusted column name
                        'Address': row['Patient_Address']  # Adjusted column name
                    })


                return results


            except mysql.connector.Error as err:

                print(f"MySQL error: {err}")

                raise Exception(f"Database error: {err}")

            except ValueError as ve:

                print(f"ValueError: {ve}")

                raise Exception(f"ValueError: {ve}")

            except Exception as e:

                print(f"Unexpected error: {e}")

                raise Exception(f"Unexpected error: {e}")

            finally:

                if 'connection' in locals() and connection.is_connected():
                    cursor.close()

                    connection.close()



    @staticmethod
    def add(patient_id, first_name, last_name, phone, address, pharmacy_id = None):
        cursor.execute("Insert INTO Patient (Patient_ID, Patient_FName, Patient_LName, Patient_Phone_Number, Patient_Address, Pharmacy_ID) VALUES (%s, %s, %s, %s, %s, %s)",
                       (patient_id, first_name, last_name, phone, address, pharmacy_id))

        db.commit()

    @staticmethod
    def get(patient_id):
        try:
            query = "SELECT Patient_FName, Patient_LName, Patient_Phone_Number, Patient_Address FROM Patient WHERE Patient_ID = %s"
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()

            if result:
                return {
                    "first_name": result[0],
                    "last_name": result[1],
                    "phone": result[2],
                    "address": result[3]
                }
            else:
                return None

        except mysql.connector.Error as error:
            raise Exception(f"Error fetching patient record: {error}")

    @staticmethod
    def update(old_patient_id, first_name, last_name, phone, address, new_patient_id=None):
        try:
            if new_patient_id is None:
                query = """
                        UPDATE Patient
                        SET Patient_FName = %s, Patient_LName = %s, Patient_Address = %s, Patient_Phone_Number = %s
                        WHERE Patient_ID = %s
                    """
                cursor.execute(query, (first_name, last_name, address, phone, old_patient_id))
            else:
                query = """
                        UPDATE Patient
                        SET Patient_ID = %s, Patient_FName = %s, Patient_LName = %s, Patient_Address = %s, Patient_Phone_Number = %s
                        WHERE Patient_ID = %s
                    """
                cursor.execute(query, (new_patient_id, first_name, last_name, address, phone, old_patient_id))

            db.commit()  # Commit changes to the database

        except mysql.connector.Error as error:
            db.rollback()  # Rollback changes if there's an error
            raise Exception(f"Error updating patient record: {error}")


class Doctor:
    @staticmethod
    def search(name):
        query = "SELECT * FROM Doctor WHERE Doctor_FName LIKE %s OR Doctor_LName LIKE %s"
        cursor.execute(query, (f"%{name}%", f"%{name}%"))
        results = cursor.fetchall()
        results = [
            {
                'Doctor ID': row[0],
                'Doctor_FName': row[1],
                'Doctor_LName': row[2],
                'Department ID': row[3],
                'Doctor Phone Number': row[4],

            }
            for row in results
        ]
        return results


class Appointment:
    @staticmethod
    def schedule(patient_id, doctor_id, date, time):
        cursor.execute("INSERT INTO Appointment (Patient_ID, Doctor_ID, Date, Time) VALUES (%s, %s, %s, %s)",
                       (patient_id, doctor_id, date, time))
        db.commit()

class Room:
    @staticmethod
    def assign(patient_id, room_num, admission_date):
        try:
            # Assuming `db` is your existing database connection object
            cursor = db.cursor()

            query = "INSERT INTO room (patient_id, room_num, admission_date) VALUES (%s, %s, %s)"
            cursor.execute(query, (patient_id, room_num, admission_date))
            db.commit()

            cursor.close()
        except mysql.connector.Error as err:
            raise Exception(f"Database error: {err}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

class Pharmacy:
    @staticmethod
    def get_info(pharmacy_name):
        query = "SELECT Pharmacy_ID, Pharmacy_Name, Pharmacy_Address, Pharmacy_Phone_Number FROM Pharmacy WHERE pharmacy_name LIKE %s"
        cursor.execute(query, (f"%{pharmacy_name}%",))
        results = cursor.fetchall()
        results = [
            {
                'Pharmacy_ID': row[0],
                'Pharmacy_Name': row[1],
                'Pharmacy_Address': row[2],
                'Pharmacy_Phone_Number': row[3]

            }
            for row in results
        ]
        return results




# Utility function to handle asset paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Main Application Class
class HealthcareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthcare Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#d8759a")
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.frames = {}
        for F in (LoginPage, MainPage, SearchPage, SortPage, SchedulePage, AddPatientPage, UpdatePatientPage, DoctorRecordsPage, AssignRoomPage, PharmacyInfoPage):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, width=1000, height=600)

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "MainPage":
            self.root.geometry("1000x600")  # Update window size for MainPage
        else:
            self.root.geometry("706x395")  # Original window size for LoginPage
        frame.tkraise()



class LoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg="#062f67",
            height=395,
            width=706,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            310.0,
            130.0,
            anchor="nw",
            text="Username",
            fill="#FFFFFF",
            font=("Inter", 12, "bold")
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            310.0,
            190.0,
            anchor="nw",
            text="Password",
            fill="#FFFFFF",
            font=("Inter", 12, "bold")
        )
        self.image_path = "C:/Users/DellUser/PycharmProjects/Desktop Assistant/healthcare_logo.webp"
        self.logo_image_pil = Image.open(self.image_path)
        self.logo_image_resized = self.logo_image_pil.resize((110, 92))
        self.logo_image_tk = ImageTk.PhotoImage(self.logo_image_resized)

        # Place the image on the canvas
        self.canvas.create_image(353, 70, image=self.logo_image_tk, anchor='center')

        self.entry_username = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_username.place(x=272.0, y=155.0, width=160.0, height=30.0)

        self.entry_password = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0, show="*")
        self.entry_password.place(x=272.0, y=210.0, width=160.0, height=30.0)

        style = ttk.Style()
        style.configure('TButton', background='#76b5c5', foreground='#000000', font=("Inter", 10, "bold"))
        style.map('TButton', background=[('active', '#76b5c5')])

        # Create the login button with the custom style
        self.button_login = ttk.Button(
            self,
            text="Login",
            style='TButton',
            command=self.login
        )
        self.button_login.place(x=272.0, y=265.0, width=160.0, height=30.0)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = Users.authenticate(username, password)
        if user:
            self.controller.show_frame("MainPage")
        else:
            messagebox.showerror("Error", "Invalid username or password")

class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        #self.configure(bg="#d8759a")
        image_path = "C:/istockphoto-1312706413-612x612.jpg"  # Replace with your image path
        image = Image.open(image_path)
        resized_image = image.resize((1000, 600), Image.LANCZOS)  # Use Image.LANCZOS for example

        # Convert the resized image to PhotoImage
        self.background_image = ImageTk.PhotoImage(resized_image)


        # Created a canvas that covers the entire MainPage frame
        self.canvas = Canvas(
            self,
            #bg="#d8759a",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        self.header_label = ttk.Label(
            self,
            text="Healthcare Management System",
            font=("Arial", 20, "bold"),
            background="#5680c8"
        )
        self.header_label.place(x=50, y=40)

        self.button_search = ttk.Button(
            self,
            text="Search Patient",
            command=lambda: controller.show_frame("SearchPage")

        )
        self.button_search.place(x=50.0, y=100.0, width=181.0, height=67.0)

        self.button_sort = ttk.Button(
            self,
            text="Sort Patients",
            command=lambda: controller.show_frame("SortPage")
        )
        self.button_sort.place(x=50.0, y=190.0, width=181.0, height=67.0)

        self.button_schedule = ttk.Button(
            self,
            text="Schedule Appointment",
            command=lambda: controller.show_frame("SchedulePage")
        )
        self.button_schedule.place(x=50.0, y=290.0, width=181.0, height=67.0)

        self.button_record = ttk.Button(
            self,
            text="Add Patients",
            command=lambda: controller.show_frame("AddPatientPage")
        )
        self.button_record.place(x=50.0, y=380.0, width=181.0, height=67.0)

        self.button_record = ttk.Button(
            self,
            text="Update Patients Record",
            command=lambda: controller.show_frame("UpdatePatientPage")
        )
        self.button_record.place(x=380.0, y=100.0, width=161.0, height=67.0)


        self.button_doctor_records = ttk.Button(
            self,
            text="Doctor Records",
            command=lambda: controller.show_frame("DoctorRecordsPage")
        )
        self.button_doctor_records.place(x=380.0, y=190.0, width=161.0, height=67.0)

        self.button_assign_room = ttk.Button(
            self,
            text="Assign Room",
            command=lambda: controller.show_frame("AssignRoomPage")
        )
        self.button_assign_room.place(x=380.0, y=290.0, width=161.0, height=67.0)

        self.button_pharmacy_info = ttk.Button(
            self,
            text="Pharmacy Info",
            command=lambda: controller.show_frame("PharmacyInfoPage")
        )
        self.button_pharmacy_info.place(x=380.0, y=380.0, width=161.0, height=67.0)

class SearchPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.patient_data = []
        self.controller = controller

        image_path = "C:/patient 1.jpeg"  # Replace with your image path
        image = Image.open(image_path)
        resized_image = image.resize((700, 395), Image.LANCZOS)  # Use Image.LANCZOS for example

        # Convert the resized image to PhotoImage
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.canvas = Canvas(
            self,
            #bg="#BECDF6",
            height=395,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')


        self.header_label = ttk.Label(
            self,
            text="Search Results",
            font=("Arial", 12),
            background="#BECDF6"
        )
        self.header_label.place(x=40, y=30)

        self.label_search_by = ttk.Label(
            self,
            text="Search By:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_search_by.place(x=100, y=90)

        self.search_by_var = StringVar(value="Patient_FName")
        self.dropdown_search_by = ttk.OptionMenu(
            self,
            self.search_by_var,
            "Patient_FName",
            "Patient_ID",
            "Patient_FName",
            "Patient_LName",
            "Patient_PhoneNumber",
            "Patient_Address"
        )
        self.dropdown_search_by.place(x=250.0, y=90.0, width=200.0, height=30.0)

        self.entry_search = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_search.place(x=250.0, y=135.0, width=200.0, height=30.0)

        self.button_search = ttk.Button(
            self,
            text="Search",
            command=self.search_patient
        )
        self.button_search.place(x=470.0, y=135.0, width=161.0, height=43.0)

        self.tree = ttk.Treeview(self, columns=("Patient_ID", "Patient_FName", "Patient_LName", "Patient_Phone_Number", "Patient_Address"))
        self.tree.place(x=50.0, y=190.0, width=580.0, height=150.0)

        self.tree.heading("#0", text="Index")
        self.tree.heading("Patient_ID", text="Patient ID")
        self.tree.heading("Patient_FName", text="First Name")
        self.tree.heading("Patient_LName", text="Last Name")
        self.tree.heading("Patient_Phone_Number", text="Phone")
        self.tree.heading("Patient_Address", text="Address")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=630, y=190, height=150)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar_x = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.scrollbar_x.place(x=50, y=340, width=580)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        self.button_back = ttk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=550.0, y=20.0, width=150.0, height=30.0)

    def binary_search(self, search_key):
        low = 0
        high = len(self.patient_data) - 1

        while low <= high:
            mid = (low + high) // 2
            current_patient = self.patient_data[mid]
            if current_patient['Patient ID'] == search_key:
                return mid  # Found the patient, return index
            elif current_patient['Patient ID'] < search_key:
                low = mid + 1  # Search the right half
            else:
                high = mid - 1  # Search the left half

        return -1

    def search_patient(self):
        search_key = self.entry_search.get().strip()
        field = self.search_by_var.get().replace(" ", "_")

        if not search_key:
            messagebox.showinfo("Search Result", "Please enter a search term")
            return

        # Fetch patient records from the database
        results = Patient.search(search_key, field)

        if not results:
            messagebox.showinfo("Search Result", f"No patients found with {field.replace('_', ' ')} '{search_key}'")
            return

        # Update self.patient_data with fetched records
        self.patient_data = results

        # Clear previous search results
        self.tree.delete(*self.tree.get_children())

        # Populate treeview with fetched patient records
        for idx, patient in enumerate(results, start=1):
            self.tree.insert("", "end", text=f"{idx}",
                             values=(patient['Patient ID'], patient['First Name'], patient['Last Name'],
                                     patient['Phone'], patient['Address']))



class SortPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        image_path = "C:/Users/DellUser/PycharmProjects/Desktop Assistant/sort patient.jpeg" # Replace with your image path
        image = Image.open(image_path)
        resized_image = image.resize((706, 395), Image.LANCZOS)  # Use Image.LANCZOS for example

        # Convert the resized image to PhotoImage
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.canvas = Canvas(
            self,
            bg="#BECDF6",
            height=395,
            width=706,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        self.header_label = ttk.Label(
            self,
            text="Sorted Results",
            font=("Arial", 12),
            background="#BECDF6"
        )
        self.header_label.place(x=40, y=30)

        self.button_quick_asc = ttk.Button(
            self,
            text="Quick Sort ASC",
            command=lambda: self.quick_sort_patients(order="ASC")
        )
        self.button_quick_asc.place(x=60.0, y=80.0, width=111.0, height=43.0)

        self.button_quick_desc = ttk.Button(
            self,
            text="Quick Sort DESC",
            command=lambda: self.quick_sort_patients(order="DESC")
        )
        self.button_quick_desc.place(x=190.0, y=80.0, width=117.0, height=43.0)

        self.button_merge_asc = ttk.Button(
            self,
            text="Merge Sort ASC",
            command=lambda: self.merge_sort_patients(order="ASC")
        )
        self.button_merge_asc.place(x=320.0, y=80.0, width=111.0, height=43.0)

        self.button_merge_desc = ttk.Button(
            self,
            text="Merge Sort DESC",
            command=lambda: self.merge_sort_patients(order="DESC")
        )
        self.button_merge_desc.place(x=450.0, y=80.0, width=121.0, height=43.0)

        # Treeview to display sorted results
        self.tree = ttk.Treeview(self, columns=("Patient ID", "First Name", "Last Name", "Phone", "Address"))
        self.tree.place(x=50.0, y=150.0, width=580.0, height=150.0)

        self.tree.heading("#0", text="Index")
        self.tree.heading("Patient ID", text="Patient ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Address", text="Address")

        # Vertical scrollbar
        self.scrollbar_y = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar_y.place(x=630, y=150, height=150)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)

        # Horizontal scrollbar
        self.scrollbar_x = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.scrollbar_x.place(x=50, y=300, width=580)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        self.button_back = ttk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=550.0, y=20.0, width=150.0, height=30.0)

    def quick_sort_patients(self, order="ASC"):
        cursor.execute("SELECT * FROM Patient")
        results = cursor.fetchall()

        # Define quick sort function
        def quick_sort(arr, low, high, order):
            if low < high:
                # Partition the array and get the pivot index
                pivot_index = partition(arr, low, high, order)

                # Recursively apply quick sort on subarrays
                quick_sort(arr, low, pivot_index - 1, order)
                quick_sort(arr, pivot_index + 1, high, order)

        # Partition function to rearrange the array
        def partition(arr, low, high, order):
            pivot = arr[high][1]  # Use Patient_FName as pivot (assuming index 1 in each row)
            i = low - 1

            for j in range(low, high):
                if order == "ASC":
                    if arr[j][1] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                else:  # DESC
                    if arr[j][1] >= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]

            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        # Call quick_sort function to sort results array
        quick_sort(results, 0, len(results) - 1, order)

        # Display sorted results in Treeview
        self.display_sorted_results(results)

    def merge_sort_patients(self, order="ASC"):
        cursor.execute("SELECT * FROM Patient")
        results = cursor.fetchall()

        def merge_sort(arr, order):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort(arr[:mid], order)
            right = merge_sort(arr[mid:], order)
            return merge(left, right, order)

        def merge(left, right, order):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if order == "ASC":
                    if left[i][1] < right[j][1]:  # Compare Patient_FName ASC
                        result.append(left[i])
                        i += 1
                    else:
                        result.append(right[j])
                        j += 1
                else:  # DESC
                    if left[i][1] > right[j][1]:  # Compare Patient_FName DESC
                        result.append(left[i])
                        i += 1
                    else:
                        result.append(right[j])
                        j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        sorted_results = merge_sort(results, order)
        self.display_sorted_results(sorted_results)

    def display_sorted_results(self, sorted_results):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert sorted results into treeview
        for idx, row in enumerate(sorted_results, start=1):
            self.tree.insert("", "end", text=f"{idx}",
                             values=(row[0], row[1], row[2], row[4], row[3]))

class SchedulePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.configure(bg="#2feca2")
        self.canvas = Canvas(
            #bg="#2feca2",
            height=395,
            width=706,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)


        self.label_header = Label(
            self,
            text="Schedule Appointment",
            font=("Arial", 18, "bold"),
            bg="#2feca2",
            fg="#ffffff",
        )
        self.label_header.place(x=100, y=30)

        # Labels for entry fields
        self.label_patient_id = ttk.Label(
            self,
            text="Patient ID:",
            background="#BECDF6",
            font = ("Inter", 10, "bold")
        )
        self.label_patient_id.place(x=100, y=90)

        self.label_doctor_id = ttk.Label(
            self,
            text="Doctor ID:",
            background="#BECDF6",
            font = ("Inter", 10, "bold")
        )
        self.label_doctor_id.place(x=100, y=140)

        self.label_date = ttk.Label(
            self,
            text="Date (YYYY-MM-DD):",
            background="#BECDF6",
            font = ("Inter", 10, "bold")
        )
        self.label_date.place(x=100, y=190)

        self.label_time = ttk.Label(
            self,
            text="Time (HH:MM):",
            background="#BECDF6",
            font = ("Inter", 10, "bold")
        )
        self.label_time.place(x=100, y=240)

        self.entry_patient_id = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_patient_id.place(x=250.0, y=90.0, width=200.0, height=30.0)

        self.entry_doctor_id = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_doctor_id.place(x=250.0, y=140.0, width=200.0, height=30.0)

        self.entry_date = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_date.place(x=250.0, y=190.0, width=200.0, height=30.0)

        self.entry_time = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_time.place(x=250.0, y=240.0, width=200.0, height=30.0)

        self.button_schedule = ttk.Button(
            self,
            text="Schedule Appointment",
            command=self.schedule_appointment
        )
        self.button_schedule.place(x=470.0, y=140.0, width=161.0, height=43.0)

        self.button_back = ttk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=550.0, y=20.0, width=150.0, height=30.0)

    def schedule_appointment(self):
        patient_id = self.entry_patient_id.get()
        doctor_id = self.entry_doctor_id.get()
        date = self.entry_date.get()
        time = self.entry_time.get()

        try:
            Appointment.schedule(patient_id, doctor_id, date, time)
            messagebox.showinfo("Success", "Appointment scheduled successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error scheduling appointment: {e}")

class AddPatientPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.configure(bg="#6e21e4")

        self.canvas = Canvas(
            bg="#6e21e4",
            height=395,
            width=706,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)


        self.header_label = ttk.Label(
            self,
            text="Add Patient Record",
            font=("Arial", 12),
            background="#BECDF6"
        )
        self.header_label.place(x=40, y=30)

        # Labels for entry fields
        self.label_patient_id = ttk.Label(
            self,
            text="Patient ID:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_patient_id.place(x=100, y=60)

        self.label_first_name = ttk.Label(
            self,
            text="First Name:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_first_name.place(x=100, y=100)

        self.label_last_name = ttk.Label(
            self,
            text="Last Name:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_last_name.place(x=100, y=140)

        self.label_phone = ttk.Label(
            self,
            text="Phone",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_phone.place(x=100, y=220)

        self.label_address = ttk.Label(
            self,
            text="Address",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_address.place(x=100, y=260)

        self.entry_patient_id = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_patient_id.place(x=250.0, y=60.0, width=200.0, height=30.0)

        self.entry_first_name = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_first_name.place(x=250.0, y=100.0, width=200.0, height=30.0)

        self.entry_last_name = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_last_name.place(x=250.0, y=140.0, width=200.0, height=30.0)

        self.entry_phone = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_phone.place(x=250.0, y=220.0, width=200.0, height=30.0)

        self.entry_address = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_address.place(x=250.0, y=260.0, width=200.0, height=30.0)

        self.button_record = ttk.Button(
            self,
            text="Add Patient Information",
            command=self.add_record
        )
        self.button_record.place(x=470.0, y=140.0, width=161.0, height=43.0)

        self.button_back = ttk.Button(
            self,
            text="Back to Main",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=550.0, y=20.0, width=150.0, height=30.0)

    def add_record(self):
        patient_id = self.entry_patient_id.get()
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        phone = self.entry_phone.get()
        address = self.entry_address.get()

        try:
            Patient.add(patient_id, first_name, last_name, phone, address)
            messagebox.showinfo("Success", "Patient record added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding record: {e}")

class UpdatePatientPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.config(bg="#21e437", width= 1000, height= 395)

        self.canvas = Canvas(
            #bg="#BECDF6",
            #height=395,
            #width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        #self.canvas.place(x=0, y=0)

        self.header_label = ttk.Label(
            self,
            text="Update Patient Record",
            font=("Arial", 12),
            background="#BECDF6"
        )
        self.header_label.place(x=40, y=25)

        # Old Data Labels and Entry Fields
        self.label_old_data = ttk.Label(
            self,
            text="Existing Data",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_old_data.place(x=60, y=60)

        self.label_old_patient_id = ttk.Label(
            self,
            text="Patient ID:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_old_patient_id.place(x=60, y=100)

        self.label_old_first_name = ttk.Label(
            self,
            text="First Name:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_old_first_name.place(x=60, y=140)

        self.label_old_last_name = ttk.Label(
            self,
            text="Last Name:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_old_last_name.place(x=60, y=180)

        self.label_old_phone = ttk.Label(
            self,
            text="Phone:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_old_phone.place(x=60, y=220)

        self.label_old_address = ttk.Label(
            self,
            text="Address:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_old_address.place(x=60, y=260)

        self.entry_old_patient_id = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_old_patient_id.place(x=150.0, y=100.0, width=170.0, height=30.0)

        self.entry_old_first_name = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_old_first_name.place(x=150.0, y=140.0, width=170.0, height=30.0)

        self.entry_old_last_name = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_old_last_name.place(x=150.0, y=180.0, width=170.0, height=30.0)

        self.entry_old_phone = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_old_phone.place(x=150.0, y=220.0, width=170.0, height=30.0)

        self.entry_old_address = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_old_address.place(x=150.0, y=260.0, width=170.0, height=30.0)

        # New Data Labels and Entry Fields
        self.label_new_data = ttk.Label(
            self,
            text="New Data",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_new_data.place(x=360, y=60)

        self.label_new_patient_id = ttk.Label(
            self,
            text="Patient ID:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_new_patient_id.place(x=360, y=100)

        self.label_new_first_name = ttk.Label(
            self,
            text="First Name:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_new_first_name.place(x=360, y=140)

        self.label_new_last_name = ttk.Label(
            self,
            text="Last Name:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_new_last_name.place(x=360, y=180)

        self.label_new_phone = ttk.Label(
            self,
            text="Phone:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_new_phone.place(x=360, y=220)

        self.label_new_address = ttk.Label(
            self,
            text="Address:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_new_address.place(x=360, y=260)

        self.entry_new_patient_id = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_new_patient_id.place(x=440.0, y=100.0, width=170.0, height=30.0)

        self.entry_new_first_name = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_new_first_name.place(x=440.0, y=140.0, width=170.0, height=30.0)

        self.entry_new_last_name = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_new_last_name.place(x=440.0, y=180.0, width=170.0, height=30.0)

        self.entry_new_phone = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_new_phone.place(x=440.0, y=220.0, width=170.0, height=30.0)

        self.entry_new_address = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_new_address.place(x=440.0, y=260.0, width=170.0, height=30.0)

        self.button_load_record = ttk.Button(
            self,
            text="Load Patient Record",
            command=self.load_record
        )
        self.button_load_record.place(x=140.0, y=320.0, width=161.0, height=43.0)

        self.button_update_record = ttk.Button(
            self,
            text="Update Patient Record",
            command=self.update_record
        )
        self.button_update_record.place(x=400.0, y=320.0, width=161.0, height=43.0)

        self.button_back = ttk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=500.0, y=20.0, width=150.0, height=30.0)

    def load_record(self):
        patient_id = self.entry_old_patient_id.get()

        try:
            # Fetch patient record from database
            patient = Patient.get(patient_id)
            if patient:
                self.entry_old_first_name.insert(0, patient["first_name"])
                self.entry_old_last_name.insert(0, patient["last_name"])
                self.entry_old_phone.insert(0, patient["phone"])
                self.entry_old_address.insert(0, patient["address"])
            else:
                messagebox.showerror("Error", "Patient record not found")

        except Exception as e:
            messagebox.showerror("Error", f"Error loading record: {e}")

    def update_record(self):
        old_patient_id = self.entry_old_patient_id.get()
        new_patient_id = self.entry_new_patient_id.get()
        new_first_name = self.entry_new_first_name.get()
        new_last_name = self.entry_new_last_name.get()
        new_phone = self.entry_new_phone.get()
        new_address = self.entry_new_address.get()

        try:
            # Update patient record in the database
            Patient.update(
                old_patient_id,
                new_first_name,
                new_last_name,
                new_phone,
                new_address,
                new_patient_id=new_patient_id if new_patient_id else None
            )
            messagebox.showinfo("Success", "Patient record updated successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating record: {e}")



class DoctorRecordsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.doctors = []
        self.controller = controller

        self.config(bg="#d9e421")

        self.canvas = Canvas(
            self,
            bg="#d9e421",
            height=395,
            width=706,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.header_label = ttk.Label(
            self,
            text="Doctor Information",
            font=("Arial", 12),
            background="#BECDF6"
        )
        self.header_label.place(x=40, y=30)

        self.label_doctor = ttk.Label(
            self,
            text="Doctor name:",
            font=("Arial", 12, "bold"),
            background="#BECDF6"

        )
        self.label_doctor.place(x=70, y=135)

        self.entry_search = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_search.place(x=250.0, y=135.0, width=200.0, height=30.0)

        self.button_search = ttk.Button(
            self,
            text="Search",
            command=self.search_doctors
        )
        self.button_search.place(x=470.0, y=135.0, width=161.0, height=43.0)

        self.tree = ttk.Treeview(self, columns=("Doctor ID", "First Name", "Last Name", "Department ID", "Doctor Phone Number"))
        self.tree.place(x=50.0, y=190.0, width=580.0, height=150.0)

        self.tree.heading("Doctor ID", text="Doctor ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Department ID", text="Department ID")
        self.tree.heading("Doctor Phone Number", text="Doctor Phone Number")
        self.tree.column("#0", width=100)
        self.tree.column("First Name", width=200)
        self.tree.column("Last Name", width=200)
        self.tree.column("Department ID", width=200)
        self.tree.column("Doctor Phone Number", width=200)
        self.tree.place(x=50.0, y=190.0, width=580.0, height=150.0)

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=630, y=190, height=150)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar_x = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.scrollbar_x.place(x=50, y=340, width=580)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        self.button_back = ttk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=550.0, y=20.0, width=150.0, height=30.0)

    def binary_search(self, search_key):
        low = 0
        high = len(self.doctors) - 1

        while low <= high:
            mid = (low + high) // 2
            current_patient = self.doctors[mid]
            if current_patient['Doctor ID'] == search_key:
                return mid  # Found the patient, return index
            elif current_patient['Doctor ID'] < search_key:
                low = mid + 1  # Search the right half
            else:
                high = mid - 1  # Search the left half

        return -1

    def search_doctors(self):
        search_key = self.entry_search.get().strip()

        if not search_key:
            messagebox.showinfo("Search Result", "Please enter a search term")
            return

        # Fetch patient records from the database
        results = Doctor.search(search_key)

        if not results:
            messagebox.showinfo("Search Result", f"No patients found with name '{search_key}'")
            return

        # Update self.patient_data with fetched records
        self.doctors_data = results

        # Clear previous search results
        self.tree.delete(*self.tree.get_children())

        # Populate treeview with fetched patient records
        for idx, doctor in enumerate(results, start=1):
            self.tree.insert("", "end", text=f"{idx}",
                             values=(doctor['Doctor ID'], doctor['Doctor_FName'], doctor['Doctor_LName'], doctor['Department ID'],
                                      doctor['Doctor Phone Number']))


class AssignRoomPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.config(bg="#e421cb")

        self.canvas = Canvas(
            self,
            bg="#e421cb",
            height=600,  # Increased height for better visibility
            width=800,  # Increased width for better visibility
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.header_label = ttk.Label(
            self,
            text="Assign Room",
            font=("Arial", 12),
            background="#BECDF6"
        )
        self.header_label.place(x=40, y=30)

        self.label_patient_id = ttk.Label(
            self,
            text="Patient ID:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_patient_id.place(x=100, y=135)

        self.label_room_number = ttk.Label(
            self,
            text="Room Number:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_room_number.place(x=100, y=180)

        self.label_admission_date = ttk.Label(
            self,
            text="Admission Date:",
            background="#BECDF6",
            font=("Inter", 10, "bold")
        )
        self.label_admission_date.place(x=100, y=225)

        self.entry_patient_id = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_patient_id.place(x=250.0, y=135.0, width=200.0, height=30.0)

        self.entry_room_number = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_room_number.place(x=250.0, y=180.0, width=200.0, height=30.0)

        self.entry_admission_date = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_admission_date.place(x=250.0, y=225.0, width=200.0, height=30.0)

        self.button_assign = ttk.Button(
            self,
            text="Assign Room",
            command=self.assign_room
        )
        self.button_assign.place(x=470.0, y=180.0, width=161.0, height=43.0)

        self.text_results = Text(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.text_results.place(x=50.0, y=280.0, width=580.0, height=150.0)

        self.button_back = ttk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=550.0, y=20.0, width=150.0, height=30.0)

    def assign_room(self):
        patient_id = self.entry_patient_id.get()
        room_number = self.entry_room_number.get()
        admission_date = self.entry_admission_date.get()

        try:
            Room.assign(patient_id, room_number, admission_date)
            self.text_results.insert('end', f"Assigned Room {room_number} to Patient {patient_id} on {admission_date}\n")
            messagebox.showinfo("Success", "Room assigned successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error assigning room: {e}")


class PharmacyInfoPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg="#BECDF6",
            height=395,
            width=706,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.header_label = ttk.Label(
            self,
            text="Pharmacy Information",
            font=("Arial", 12, "bold"),
            background="#BECDF6"
        )
        self.header_label.place(x=40, y=30)

        self.label_pharmacy = ttk.Label(
            self,
            text = "Pharmacy name:",
            font=("Arial", 12, "bold"),
            background="#BECDF6"

        )
        self.label_pharmacy.place(x=70, y=135)

        self.entry_search = Entry(self, bd=0, bg="#FFFFFF", highlightthickness=0)
        self.entry_search.place(x=250.0, y=135.0, width=200.0, height=30.0)

        self.button_search = ttk.Button(
            self,
            text="Search",
            command=self.search_pharmacy
        )
        self.button_search.place(x=470.0, y=135.0, width=161.0, height=43.0)

        # Replace Text widget with Treeview widget
        self.tree = ttk.Treeview(self, columns=("Pharmacy_ID", "Pharmacy Name", "Pharmacy Address", "Pharmacy Phone Number"))
        self.tree.place(x=50.0, y=190.0, width=580.0, height=150.0)

        self.tree.heading("#0", text="Index")
        self.tree.heading("Pharmacy_ID", text="Pharmacy ID")
        self.tree.heading("Pharmacy Name", text="Name")
        self.tree.heading("Pharmacy Address", text="Address")
        self.tree.heading("Pharmacy Phone Number", text="Phone")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=630, y=190, height=150)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar_x = Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.scrollbar_x.place(x=50, y=340, width=580)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)

        self.button_back = ttk.Button(
            self,
            text="Back to Main Page",
            command=lambda: controller.show_frame("MainPage")
        )
        self.button_back.place(x=550.0, y=20.0, width=150.0, height=30.0)

    def search_pharmacy(self):
        pharmacy_name = self.entry_search.get()
        results = Pharmacy.get_info(pharmacy_name)

        # Clear previous search results
        self.tree.delete(*self.tree.get_children())

        # Populate treeview with fetched pharmacy records
        for idx, pharmacy in enumerate(results, start=1):
            self.tree.insert("", "end", text=f"{idx}",
                             values=(pharmacy['Pharmacy_ID'], pharmacy['Pharmacy_Name'], pharmacy['Pharmacy_Address'], pharmacy['Pharmacy_Phone_Number']))

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = HealthcareApp(root)
    root.mainloop()
