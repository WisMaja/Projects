from enum import Enum
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Gender(Enum):
    MALE = "Mężczyzna"
    FEMALE = "Kobieta"


class Patient:
    appointment_hour = None

    def __init__(self, first_name, last_name, pesel, age, gender):
        if not isinstance(age, int):
            raise ValueError("Wiek musi być liczbą całkowitą")
        if age < 18:
            raise ValueError("Przykro mi, musisz mieć co najmniej 18 lat, aby umówić się na wizytę")
        if age > 120:
            raise ValueError("Pomyliłeś się podając wiek - maksymalna przyjmowana wartość to 120")
        if len(pesel) != 11:
            raise ValueError("Twój PESEL musi mieć 11 cyfr")
        if not first_name.isalpha():
            raise ValueError("Imie musi sie skłądac z samych liter")
        if not last_name.isalpha():
            raise ValueError("Nazwisko musi sie skłądac z samych liter")

        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel
        self.age = age
        self.gender = gender


class Node:
    def __init__(self, patient):
        self.patient = patient
        self.next = None


class QueueOfPatients:

    def __init__(self):
        self.head = None

    def get_number_of_patients(self):
        count = 0
        current_node = self.head

        while current_node is not None:
            count += 1
            current_node = current_node.next
        return count

    def is_pesel_in_queue(self, pesel):
        current_node = self.head
        while current_node:
            if current_node.patient.pesel == pesel:
                return True
            current_node = current_node.next
        return False

    def add_patient(self, patient):
        if self.is_pesel_in_queue(patient.pesel):
            messagebox.showerror("Błąd", f"Pacjent o numerze PESEL: {patient.pesel} już istnieje w kolejce.")
            return

        available_hours = [8, 9, 10, 11, 12, 13, 14, 15]
        current_node = self.head

        while current_node:
            if current_node.patient.appointment_hour in available_hours:
                available_hours.remove(current_node.patient.appointment_hour)
            current_node = current_node.next

        if not available_hours:
            raise ValueError("Przykro mi, nie ma już miejsc dostępnych na jutro. Spróbuj innego dnia.")
            return

        new_node = Node(patient)
        patient.appointment_hour = available_hours[0]

        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node

        self.sort_patients_by_appointment_hour()

    def add_priority_patient(self, patient, number_in_line):
        if number_in_line < 1 or number_in_line > 8:
            raise ValueError("Pozycje w kolejce może być wybrana w zakresie od 1 (8:00) do 8 (15:00)")
            return

        appointment_hour = number_in_line + 7
        new_node = Node(patient)
        new_node.patient.appointment_hour = appointment_hour

        if self.head is None:
            self.head = new_node
            return

        if self.head.patient.appointment_hour >= appointment_hour:
            # Przypadek, gdy nowy pacjent jest pierwszy w kolejce
            self.update_appointments_hours(self.head, 1)  # Przesuwamy wszystkich pacjentów
            new_node.next = self.head
            self.head = new_node
        else:
            # Znajdowanie miejsca wstawienia pacjenta
            current_node = self.head
            while current_node.next is not None and current_node.next.patient.appointment_hour < appointment_hour:
                current_node = current_node.next

            # Dodawanie nowego pacjenta do kolejki
            new_node.next = current_node.next
            current_node.next = new_node

            # Aktualizacja godzin wizyt tylko dla pacjentów z późniejszymi godzinami
            if new_node.next is not None and new_node.next.patient.appointment_hour >= appointment_hour:
                self.update_appointments_hours(new_node.next, 1)

    def update_appointments_hours(self, start_node, hour_value):
        current_node = start_node
        while current_node is not None:
            current_node.patient.appointment_hour += hour_value
            current_node = current_node.next

    def remove_patient(self, pesel):
        current_node = self.head

        if current_node is not None and current_node.patient.pesel == pesel:
            self.update_appointments_hours(self.head, -1)      #usunać zmiane godzin tez to tu
            self.head = current_node.next
            return

        prev_node = None
        while current_node is not None and current_node.patient.pesel != pesel:
            prev_node = current_node
            current_node = current_node.next

        if current_node is None:
            messagebox.showerror("Błąd", f"Pacjent o numerze PESEL: {pesel}, nie został znaleziony.")
            return

        prev_node.next = current_node.next
        self.update_appointments_hours(prev_node.next, -1)       #usunąć jak nie chcemy zeby zmieniało godziny

    def display_patients(self):
        current_node = self.head
        print("Pacjenci w kolejce:")
        while current_node:
            print(
                f"({current_node.patient.first_name} {current_node.patient.last_name}, PESEL: {current_node.patient.pesel}, godzina wizyty: {current_node.patient.appointment_hour}) -> ",
                end="")
            current_node = current_node.next
        print("\n---")

    def sort_patients_by_appointment_hour(self):
        if self.head is None or self.head.next is None:
            return

        current_node = self.head.next
        prev_node = self.head

        while current_node is not None:
            temp_node = current_node
            temp_prev_node = prev_node

            while temp_node is not None and temp_node.patient.appointment_hour < temp_prev_node.patient.appointment_hour:
                temp_prev_node.patient, temp_node.patient = temp_node.patient, temp_prev_node.patient
                temp_node = temp_node.next
                temp_prev_node = temp_prev_node.next

            prev_node = current_node
            current_node = current_node.next


def remove_patient():
    pesel = remove_pesel_entry.get()
    queue_of_patients.remove_patient(pesel)
    display_patients()
    remove_pesel_entry.delete(0, tk.END)


def add_patient():
    try:
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        pesel = first_pesel_entry.get()
        age = first_age_entry.get()
        gender = gender_combobox.get()
        if not all([first_name, last_name, pesel, age, gender]):
            messagebox.showerror("Błąd", "Wszystkie pola: imię, nazwisko, PESEL, wiek, płeć  muszą być ustawione.")
            return
        if not age.isdigit():
            raise ValueError("Wiek musi być liczbą całkowitą")
        age = int(age)

        if not pesel.isdigit() or len(pesel) != 11:
            raise ValueError("PESEL musi składać się z 11 cyfr (tylko cyfry)")

        patient = Patient(first_name, last_name, pesel, age, gender)
        queue_of_patients.add_patient(patient)
        display_patients()

        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        first_pesel_entry.delete(0, tk.END)
        first_age_entry.delete(0, tk.END)
        gender_combobox.set("")

    except ValueError as e:
        messagebox.showerror("Błąd", str(e))


def add_priority_patient():
    try:
        position_in_queue = priority_position_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        pesel = first_pesel_entry.get()
        age = first_age_entry.get()
        gender = gender_combobox.get()

        if not all([first_name, last_name, pesel, age, gender]):
            messagebox.showerror("Błąd", "Wszystkie pola: imię, nazwisko, PESEL, wiek, płeć muszą być ustawione.")
            return

        if not age.isdigit():
            raise ValueError("Wiek musi być liczbą całkowitą")
        age = int(age)

        if not pesel.isdigit() or len(pesel) != 11:
            raise ValueError("PESEL musi składać się z 11 cyfr (tylko cyfry)")

        if not position_in_queue.isdigit():
            raise ValueError("Pozycja w kolejce musi byc liczbą całkowitą")
        position_in_queue = int(position_in_queue)
        appointment_hour = position_in_queue + 7

        number_of_pateints = queue_of_patients.get_number_of_patients()
        if number_of_pateints + 1 < position_in_queue:
            raise ValueError(f"W kolejce jest tylko {number_of_pateints} pacjentów. Maksymalna pozycja do wyboru to koniec kolejki, czyli {number_of_pateints + 1}")

        patient = Patient(first_name, last_name, pesel, age, gender)
        patient.appointment_hour = appointment_hour
        queue_of_patients.add_priority_patient(patient, appointment_hour - 7)

        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        first_pesel_entry.delete(0, tk.END)
        first_age_entry.delete(0, tk.END)

        priority_position_entry.delete(0, tk.END)
        gender_combobox.set("")

        display_patients()

    except ValueError as e:
        messagebox.showerror("Błąd", str(e))



def display_patients():
    patient_list.delete(1.0, tk.END)
    current_node = queue_of_patients.head
    while current_node:
        patient_info = f"{current_node.patient.first_name} {current_node.patient.last_name}, PESEL: {current_node.patient.pesel}, godzina wizyty: {current_node.patient.appointment_hour}\n"
        patient_list.insert(tk.END, patient_info)
        current_node = current_node.next


root = tk.Tk()
root.title("System Zarządzania Kolejką Pacjentów")
root.geometry("800x600")
frame = tk.Frame(root)

first_name_label = tk.Label(frame, text="Imię:")
first_name_entry = tk.Entry(frame)
last_name_label = tk.Label(frame, text="Nazwisko:")
last_name_entry = tk.Entry(frame)
first_age_label = tk.Label(frame, text="Wiek:")
first_age_entry = tk.Entry(frame)
first_pesel_label = tk.Label(frame, text="Pesel:")
first_pesel_entry = tk.Entry(frame)
gender_label = tk.Label(frame, text="Płeć:", width=0)
gender_combobox = ttk.Combobox(frame, values=[gender.value for gender in Gender], state="readonly")
gender_combobox.set("")

remove_pesel_label = tk.Label(frame, text="Usuń pacjenta wprowadzając jego nr PESEL:")
remove_pesel_entry = tk.Entry(frame)

priority_position_label = tk.Label(frame, text="Podaj pozycje w kolejce:")
priority_position_entry = tk.Entry(frame)

add_button = tk.Button(frame, text="Dodaj Pacjenta", command=add_patient)
remove_button = tk.Button(frame, text="Usuń Pacjenta", command=remove_patient)
display_button = tk.Button(frame, text="Dodaj priorytetowego pacjenta", command=add_priority_patient)

patient_list = tk.Text(frame, height=10, width=60)

# Ustawienie elementów w ramce
first_name_label.grid(row=0, column=0, sticky="w", pady=5)
first_name_entry.grid(row=0, column=1, pady=1)
last_name_label.grid(row=1, column=0, sticky="w", pady=5)
last_name_entry.grid(row=1, column=1, pady=1)
first_age_label.grid(row=2, column=0, sticky="w", pady=5)
first_age_entry.grid(row=2, column=1, pady=1)
first_pesel_label.grid(row=3, column=0, sticky="w", pady=5)
first_pesel_entry.grid(row=3, column=1, pady=1)
gender_label.grid(row=4, column=0, sticky="w", pady=5)
gender_combobox.grid(row=4, column=1, pady=1)

remove_pesel_label.grid(row=6, column=0, sticky="w", pady=5)
remove_pesel_entry.grid(row=6, column=1, pady=1)

priority_position_label.grid(row=8, column=0, sticky="w", pady=5)
priority_position_entry.grid(row=8, column=1, pady=1)

add_button.grid(row=5, column=0, columnspan=2, pady=1)
remove_button.grid(row=7, column=0, columnspan=2, pady=1)
display_button.grid(row=9, column=0, columnspan=2, pady=1)

info_label1 = tk.Label(frame, text="Klient priorytetowy może wybrać na której pozycji w kolejce chce być.", fg="red")
info_label2 = tk.Label(frame, text="Proszę wziąć pod uwagę, że wizyta trwa godzine", fg="red")
info_label3 = tk.Label(frame, text="Pozycja nr 1 w kolejce jest przyjmowania o godzinie 8, pozycja nr 8 (ostatnia) w kolejce jest przyjowana o godzinie 15", fg="red")

info_label1.grid(row=11, column=0, columnspan=2, pady=5)
info_label2.grid(row=12, column=0, columnspan=2, pady=5)
info_label3.grid(row=13, column=0, columnspan=2, pady=5)

# Ustawienie Text do rozciągnięcia na szerokość okna
patient_list.grid(row=10, column=0, columnspan=4, sticky="nsew")

# Wyśrodkowanie ramki w oknie
frame.pack_propagate(False)
frame.place(relx=0.5, rely=0.5, anchor="center")

queue_of_patients = QueueOfPatients()

root.mainloop()