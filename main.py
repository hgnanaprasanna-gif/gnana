import sys
from typing import Optional
from hospital_queue.models import PriorityLevel
from hospital_queue.system import HospitalQueueSystem


def print_banner():
    print("=" * 60)
    print("        HOSPITAL QUEUE MANAGEMENT SYSTEM        ")
    print("=" * 60)


def print_menu():
    print("\n--- Main Menu ---")
    print("1. Register Doctor")
    print("2. Register Patient (Add to Queue)")
    print("3. Call Next Patient (Doctor)")
    print("4. Complete Consultation (Doctor)")
    print("5. Cancel Patient Queue")
    print("6. View Waiting Queue (By Department / All)")
    print("7. Check Patient Status")
    print("8. View Department Summary & Statistics")
    print("9. Load Sample Data")
    print("0. Exit")


def seed_sample_data(system: HospitalQueueSystem):
    # Register default doctors
    system.register_doctor("DOC01", "Dr. Sarah Connor", "CARDIOLOGY")
    system.register_doctor("DOC02", "Dr. John House", "GENERAL")
    system.register_doctor("DOC03", "Dr. Meredith Grey", "PEDIATRICS")

    # Register sample patients with various priorities
    system.register_patient("P01", "Alice Smith", 30, "Female", "GENERAL", PriorityLevel.NORMAL, "Routine checkup")
    system.register_patient("P02", "Bob Jones", 45, "Male", "CARDIOLOGY", PriorityLevel.EMERGENCY, "Severe chest pain")
    system.register_patient("P03", "Charlie Brown", 8, "Male", "PEDIATRICS", PriorityLevel.URGENT, "High fever")
    system.register_patient("P04", "Diana Prince", 29, "Female", "CARDIOLOGY", PriorityLevel.URGENT, "Shortness of breath")
    system.register_patient("P05", "Evan Wright", 52, "Male", "GENERAL", PriorityLevel.NORMAL, "Flu symptoms")
    print("\n[+] Sample doctors and patients loaded successfully!")


def main():
    system = HospitalQueueSystem()
    print_banner()

    while True:
        print_menu()
        choice = input("\nEnter menu choice (0-9): ").strip()

        if choice == "1":
            print("\n-- Register Doctor --")
            doc_id = input("Enter Doctor ID (e.g., DOC01): ").strip()
            name = input("Enter Doctor Name: ").strip()
            dept = input("Enter Department (e.g., CARDIOLOGY, GENERAL, PEDIATRICS): ").strip()
            if doc_id and name and dept:
                try:
                    system.register_doctor(doc_id, name, dept.upper())
                    print(f"[+] Doctor {name} registered for {dept.upper()} department.")
                except Exception as e:
                    print(f"[-] Error: {e}")
            else:
                print("[-] All fields are required.")

        elif choice == "2":
            print("\n-- Register Patient --")
            pid = input("Enter Patient ID (e.g., P101): ").strip()
            name = input("Enter Patient Name: ").strip()
            try:
                age = int(input("Enter Age: ").strip())
            except ValueError:
                print("[-] Invalid age format.")
                continue
            gender = input("Enter Gender (Male/Female/Other): ").strip()
            dept = input("Enter Department (e.g., CARDIOLOGY, GENERAL, PEDIATRICS): ").strip()
            print("Priority Levels: 1 - EMERGENCY, 2 - URGENT, 3 - NORMAL")
            prio_input = input("Enter Priority Level (1-3) [Default: 3]: ").strip() or "3"

            prio_map = {"1": PriorityLevel.EMERGENCY, "2": PriorityLevel.URGENT, "3": PriorityLevel.NORMAL}
            priority = prio_map.get(prio_input, PriorityLevel.NORMAL)
            notes = input("Enter Clinical Notes / Triage details: ").strip()

            if pid and name and dept:
                try:
                    patient = system.register_patient(
                        patient_id=pid,
                        name=name,
                        age=age,
                        gender=gender,
                        department=dept,
                        priority=priority,
                        notes=notes
                    )
                    print(f"[+] Patient {patient.name} registered and added to {patient.department} queue.")
                    print(f"    Priority: {patient.priority.name} | Queue Sequence #: {patient.sequence_number}")
                except Exception as e:
                    print(f"[-] Error: {e}")
            else:
                print("[-] Required fields missing.")

        elif choice == "3":
            print("\n-- Call Next Patient --")
            doc_id = input("Enter Doctor ID: ").strip()
            try:
                patient = system.call_next_patient(doc_id)
                if patient:
                    doctor = system.get_doctor(doc_id)
                    print(f"\n[>>> CALLING PATIENT <<<]")
                    print(f"Patient ID: {patient.patient_id} | Name: {patient.name}")
                    print(f"Priority: {patient.priority.name} | Age: {patient.age} | Gender: {patient.gender}")
                    print(f"Department: {patient.department} | Assigned Doctor: {doctor.name if doctor else doc_id}")
                    if patient.notes:
                        print(f"Notes: {patient.notes}")
                else:
                    print("[-] No waiting patients available for this doctor's department.")
            except Exception as e:
                print(f"[-] Error: {e}")

        elif choice == "4":
            print("\n-- Complete Consultation --")
            doc_id = input("Enter Doctor ID: ").strip()
            try:
                patient = system.complete_consultation(doc_id)
                if patient:
                    print(f"[+] Consultation completed for Patient {patient.name} (ID: {patient.patient_id}).")
                else:
                    print("[-] No active consultation found for this doctor.")
            except Exception as e:
                print(f"[-] Error: {e}")

        elif choice == "5":
            print("\n-- Cancel Patient Queue --")
            pid = input("Enter Patient ID: ").strip()
            success = system.cancel_patient_queue(pid)
            if success:
                print(f"[+] Queue entry for Patient ID {pid} has been cancelled.")
            else:
                print(f"[-] Failed to cancel. Patient not found or not in WAITING status.")

        elif choice == "6":
            print("\n-- Waiting Queue Status --")
            dept = input("Enter Department (leave blank for all departments): ").strip()
            dept_arg = dept.upper() if dept else None
            waiting = system.get_waiting_queue(dept_arg)

            if not waiting:
                print("[-] No patients currently in waiting queue.")
            else:
                print(f"\n{'ID':<10} {'Name':<20} {'Dept':<15} {'Priority':<12} {'Seq #':<6}")
                print("-" * 65)
                for p in waiting:
                    print(f"{p.patient_id:<10} {p.name:<20} {p.department:<15} {p.priority.name:<12} {p.sequence_number:<6}")

        elif choice == "7":
            print("\n-- Check Patient Status --")
            pid = input("Enter Patient ID: ").strip()
            patient = system.get_patient_status(pid)
            if patient:
                print(f"\nPatient ID: {patient.patient_id}")
                print(f"Name:       {patient.name}")
                print(f"Age/Gender: {patient.age} / {patient.gender}")
                print(f"Department: {patient.department}")
                print(f"Priority:   {patient.priority.name}")
                print(f"Status:     {patient.status.value}")
                print(f"Doctor:     {patient.assigned_doctor_id or 'Not Assigned'}")
                if patient.notes:
                    print(f"Notes:      {patient.notes}")
            else:
                print(f"[-] Patient ID {pid} not found.")

        elif choice == "8":
            print("\n-- Department Queue Statistics --")
            stats = system.get_department_stats()
            if not stats:
                print("[-] No registered patients in system.")
            else:
                print(f"\n{'Department':<15} {'Waiting':<10} {'In Consult':<12} {'Completed':<12} {'Cancelled':<10}")
                print("-" * 65)
                for dept, counts in stats.items():
                    print(f"{dept:<15} {counts['WAITING']:<10} {counts['IN_CONSULTATION']:<12} {counts['COMPLETED']:<12} {counts['CANCELLED']:<10}")

        elif choice == "9":
            seed_sample_data(system)

        elif choice == "0":
            print("\nExiting Hospital Queue System. Goodbye!")
            sys.exit(0)

        else:
            print("[-] Invalid choice. Please enter a number between 0 and 9.")


if __name__ == "__main__":
    main()
