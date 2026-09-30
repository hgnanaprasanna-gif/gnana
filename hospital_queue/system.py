import heapq
from typing import Dict, List, Optional
from hospital_queue.models import Doctor, Patient, PatientStatus, PriorityLevel


class HospitalQueueSystem:
    """Core manager for hospital queue operations, department handling, doctor management,
    and priority queue servicing."""

    def __init__(self):
        self.patients: Dict[str, Patient] = {}
        self.doctors: Dict[str, Doctor] = {}
        # Department queues stored as priority queues (min-heaps based on Patient.__lt__)
        self.department_queues: Dict[str, List[Patient]] = {}
        self._sequence_counter: int = 0

    def register_doctor(self, doctor_id: str, name: str, department: str) -> Doctor:
        """Register a doctor in the system."""
        doctor = Doctor(doctor_id=doctor_id, name=name, department=department)
        self.doctors[doctor_id] = doctor
        return doctor

    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        """Retrieve doctor by ID."""
        return self.doctors.get(doctor_id)

    def register_patient(
        self,
        patient_id: str,
        name: str,
        age: int,
        gender: str,
        department: str,
        priority: PriorityLevel = PriorityLevel.NORMAL,
        notes: str = ""
    ) -> Patient:
        """Register a new patient and place them into their department's priority queue."""
        if patient_id in self.patients:
            raise ValueError(f"Patient ID '{patient_id}' is already registered.")

        self._sequence_counter += 1
        patient = Patient(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            department=department.upper(),
            priority=priority,
            sequence_number=self._sequence_counter,
            notes=notes
        )

        self.patients[patient_id] = patient
        dept = patient.department
        if dept not in self.department_queues:
            self.department_queues[dept] = []
        heapq.heappush(self.department_queues[dept], patient)
        return patient

    def call_next_patient(self, doctor_id: str) -> Optional[Patient]:
        """Call the highest priority waiting patient for a doctor's department."""
        doctor = self.doctors.get(doctor_id)
        if not doctor:
            raise ValueError(f"Doctor ID '{doctor_id}' not found.")

        dept = doctor.department.upper()
        if dept not in self.department_queues or not self.department_queues[dept]:
            return None

        # Clean up cancelled/processed patients top of queue if any
        while self.department_queues[dept]:
            candidate = self.department_queues[dept][0]
            if candidate.status == PatientStatus.WAITING:
                break
            heapq.heappop(self.department_queues[dept])

        if not self.department_queues[dept]:
            return None

        patient = heapq.heappop(self.department_queues[dept])
        patient.status = PatientStatus.IN_CONSULTATION
        patient.assigned_doctor_id = doctor_id
        doctor.is_available = False
        doctor.current_patient_id = patient.patient_id
        return patient

    def complete_consultation(self, doctor_id: str) -> Optional[Patient]:
        """Mark current consultation as completed for a given doctor."""
        doctor = self.doctors.get(doctor_id)
        if not doctor:
            raise ValueError(f"Doctor ID '{doctor_id}' not found.")

        if not doctor.current_patient_id:
            return None

        patient = self.patients.get(doctor.current_patient_id)
        if patient:
            patient.status = PatientStatus.COMPLETED

        doctor.is_available = True
        doctor.current_patient_id = None
        return patient

    def cancel_patient_queue(self, patient_id: str) -> bool:
        """Cancel a patient's queue spot if they are currently waiting."""
        patient = self.patients.get(patient_id)
        if not patient or patient.status != PatientStatus.WAITING:
            return False

        patient.status = PatientStatus.CANCELLED
        return True

    def get_waiting_queue(self, department: Optional[str] = None) -> List[Patient]:
        """Return list of waiting patients sorted by priority order for a department (or all)."""
        waiting_patients = []
        if department:
            dept = department.upper()
            q = self.department_queues.get(dept, [])
            waiting_patients = [p for p in q if p.status == PatientStatus.WAITING]
        else:
            for q in self.department_queues.values():
                waiting_patients.extend([p for p in q if p.status == PatientStatus.WAITING])

        return sorted(waiting_patients)

    def get_patient_status(self, patient_id: str) -> Optional[Patient]:
        """Get patient details and current status."""
        return self.patients.get(patient_id)

    def get_department_stats(self) -> Dict[str, Dict[str, int]]:
        """Get patient count breakdown by status for each department."""
        stats: Dict[str, Dict[str, int]] = {}
        for p in self.patients.values():
            dept = p.department
            if dept not in stats:
                stats[dept] = {"WAITING": 0, "IN_CONSULTATION": 0, "COMPLETED": 0, "CANCELLED": 0}
            stats[dept][p.status.value] += 1
        return stats
