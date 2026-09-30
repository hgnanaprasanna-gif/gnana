from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional


class PriorityLevel(IntEnum):
    """Priority levels for hospital patients. Lower values indicate higher priority."""
    EMERGENCY = 1
    URGENT = 2
    NORMAL = 3

    def __str__(self) -> str:
        return self.name.capitalize()


class PatientStatus(Enum):
    """Current status of a patient in the hospital queue system."""
    WAITING = "WAITING"
    IN_CONSULTATION = "IN_CONSULTATION"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    def __str__(self) -> str:
        return self.value


@dataclass
class Patient:
    """Represents a patient in the hospital queue."""
    patient_id: str
    name: str
    age: int
    gender: str
    department: str
    priority: PriorityLevel = PriorityLevel.NORMAL
    status: PatientStatus = PatientStatus.WAITING
    registered_at: datetime = field(default_factory=datetime.now)
    sequence_number: int = 0
    assigned_doctor_id: Optional[str] = None
    notes: str = ""

    def __lt__(self, other: "Patient") -> bool:
        """Comparison for priority queue: higher priority (lower value) comes first,
        then earlier sequence number (FIFO tie-breaker)."""
        if not isinstance(other, Patient):
            return NotImplemented
        if self.priority != other.priority:
            return self.priority.value < other.priority.value
        return self.sequence_number < other.sequence_number


@dataclass
class Doctor:
    """Represents a doctor in the hospital."""
    doctor_id: str
    name: str
    department: str
    is_available: bool = True
    current_patient_id: Optional[str] = None
