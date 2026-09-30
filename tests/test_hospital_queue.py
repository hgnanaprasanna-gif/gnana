import pytest
from hospital_queue.models import Doctor, Patient, PatientStatus, PriorityLevel
from hospital_queue.system import HospitalQueueSystem


def test_doctor_registration():
    system = HospitalQueueSystem()
    doc = system.register_doctor("DOC01", "Dr. House", "GENERAL")
    assert doc.doctor_id == "DOC01"
    assert doc.name == "Dr. House"
    assert doc.department == "GENERAL"
    assert system.get_doctor("DOC01") == doc


def test_patient_registration_and_priority_order():
    system = HospitalQueueSystem()
    system.register_doctor("DOC01", "Dr. House", "GENERAL")

    # Register normal patient first
    p_normal = system.register_patient("P01", "Alice", 30, "F", "GENERAL", PriorityLevel.NORMAL)
    # Register emergency patient second
    p_emergency = system.register_patient("P02", "Bob", 40, "M", "GENERAL", PriorityLevel.EMERGENCY)
    # Register urgent patient third
    p_urgent = system.register_patient("P03", "Charlie", 50, "M", "GENERAL", PriorityLevel.URGENT)

    # Call next patient should prioritize EMERGENCY (Bob)
    called1 = system.call_next_patient("DOC01")
    assert called1 == p_emergency
    assert called1.status == PatientStatus.IN_CONSULTATION

    # Next call should prioritize URGENT (Charlie)
    system.complete_consultation("DOC01")
    called2 = system.call_next_patient("DOC01")
    assert called2 == p_urgent

    # Next call should get NORMAL (Alice)
    system.complete_consultation("DOC01")
    called3 = system.call_next_patient("DOC01")
    assert called3 == p_normal


def test_fifo_for_same_priority():
    system = HospitalQueueSystem()
    system.register_doctor("DOC01", "Dr. House", "GENERAL")

    p1 = system.register_patient("P01", "Alice", 30, "F", "GENERAL", PriorityLevel.URGENT)
    p2 = system.register_patient("P02", "Bob", 40, "M", "GENERAL", PriorityLevel.URGENT)

    called1 = system.call_next_patient("DOC01")
    assert called1 == p1

    system.complete_consultation("DOC01")
    called2 = system.call_next_patient("DOC01")
    assert called2 == p2


def test_queue_cancellation():
    system = HospitalQueueSystem()
    system.register_doctor("DOC01", "Dr. House", "GENERAL")

    p1 = system.register_patient("P01", "Alice", 30, "F", "GENERAL", PriorityLevel.EMERGENCY)
    p2 = system.register_patient("P02", "Bob", 40, "M", "GENERAL", PriorityLevel.NORMAL)

    # Cancel emergency patient P01
    cancelled = system.cancel_patient_queue("P01")
    assert cancelled is True
    assert p1.status == PatientStatus.CANCELLED

    # Calling next patient should skip cancelled P01 and return P02
    called = system.call_next_patient("DOC01")
    assert called == p2


def test_duplicate_patient_registration_fails():
    system = HospitalQueueSystem()
    system.register_patient("P01", "Alice", 30, "F", "GENERAL")
    with pytest.raises(ValueError, match="already registered"):
        system.register_patient("P01", "Alice Dup", 30, "F", "GENERAL")


def test_invalid_doctor_call_fails():
    system = HospitalQueueSystem()
    with pytest.raises(ValueError, match="Doctor ID 'DOC99' not found"):
        system.call_next_patient("DOC99")


def test_department_stats():
    system = HospitalQueueSystem()
    system.register_doctor("DOC01", "Dr. House", "GENERAL")

    system.register_patient("P01", "Alice", 30, "F", "GENERAL", PriorityLevel.NORMAL)
    p2 = system.register_patient("P02", "Bob", 40, "M", "GENERAL", PriorityLevel.EMERGENCY)

    system.call_next_patient("DOC01")
    system.complete_consultation("DOC01")

    stats = system.get_department_stats()
    assert stats["GENERAL"]["WAITING"] == 1
    assert stats["GENERAL"]["COMPLETED"] == 1
