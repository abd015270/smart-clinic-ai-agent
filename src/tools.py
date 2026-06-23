from crewai.tools import tool

from src.config import CLINICS_FILE, DOCTORS_FILE
from src.database import save_appointment, save_emergency_alert, init_database
from src.rag import build_rag_context
from src.utils import load_json_file, format_json, normalize_text, generate_booking_code


def load_clinics():
    return load_json_file(CLINICS_FILE)


def load_doctors():
    return load_json_file(DOCTORS_FILE)


def find_clinics_logic(city: str, specialty: str):
    clinics = load_clinics()

    city_normalized = normalize_text(city)
    specialty_normalized = normalize_text(specialty)

    results = []

    for clinic in clinics:
        clinic_city = normalize_text(clinic.get("city", ""))
        clinic_specialty = normalize_text(clinic.get("specialty", ""))

        city_matches = city_normalized in clinic_city or clinic_city in city_normalized
        specialty_matches = (
            specialty_normalized in clinic_specialty
            or clinic_specialty in specialty_normalized
        )

        if city_matches and specialty_matches:
            results.append(clinic)

    return results


def get_doctors_by_clinic_id(clinic_id: int):
    doctors = load_doctors()

    return [
        doctor
        for doctor in doctors
        if int(doctor.get("clinic_id")) == int(clinic_id)
    ]


def get_availability_logic(city: str, specialty: str):
    clinics = find_clinics_logic(city, specialty)

    if not clinics:
        return {
            "success": False,
            "message": "No clinic was found for the selected city and specialty.",
            "data": [],
        }

    availability = []

    for clinic in clinics:
        doctors = get_doctors_by_clinic_id(clinic["id"])

        availability.append(
            {
                "clinic": clinic["name"],
                "city": clinic["city"],
                "specialty": clinic["specialty"],
                "address": clinic["address"],
                "phone": clinic["phone"],
                "emergency_available": clinic["emergency_available"],
                "doctors": [
                    {
                        "doctor_name": doctor["name"],
                        "specialty": doctor["specialty"],
                        "available_slots": doctor["available_slots"],
                    }
                    for doctor in doctors
                ],
            }
        )

    return {
        "success": True,
        "message": "Available clinics and doctors were found.",
        "data": availability,
    }


def book_appointment_logic(
    patient_name: str,
    patient_phone: str,
    city: str,
    specialty: str,
    preferred_slot: str = "",
):
    init_database()

    clinics = find_clinics_logic(city, specialty)

    if not clinics:
        return {
            "success": False,
            "message": "No clinic found. Please check the city and specialty.",
        }

    selected_clinic = clinics[0]
    doctors = get_doctors_by_clinic_id(selected_clinic["id"])

    if not doctors:
        return {
            "success": False,
            "message": "No doctors found for this clinic.",
        }

    selected_doctor = doctors[0]
    available_slots = selected_doctor.get("available_slots", [])

    if not available_slots:
        return {
            "success": False,
            "message": "No available appointment slots for this doctor.",
        }

    selected_slot = None

    if preferred_slot:
        for slot in available_slots:
            if normalize_text(preferred_slot) in normalize_text(slot):
                selected_slot = slot
                break

    if selected_slot is None:
        selected_slot = available_slots[0]

    booking_code = generate_booking_code()

    appointment_id = save_appointment(
        patient_name=patient_name,
        patient_phone=patient_phone,
        city=city,
        specialty=specialty,
        clinic_name=selected_clinic["name"],
        doctor_name=selected_doctor["name"],
        appointment_slot=selected_slot,
        booking_code=booking_code,
    )

    return {
        "success": True,
        "message": "Appointment booked successfully.",
        "appointment_id": appointment_id,
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "clinic_name": selected_clinic["name"],
        "doctor_name": selected_doctor["name"],
        "appointment_slot": selected_slot,
        "booking_code": booking_code,
        "important_note": "Please bring your personal ID and show the booking code at reception.",
    }


def send_emergency_alert_logic(
    patient_name: str,
    patient_phone: str,
    city: str,
    symptoms: str,
    urgency_level: str = "high",
):
    init_database()

    clinics = load_clinics()
    city_normalized = normalize_text(city)

    emergency_clinics = []

    for clinic in clinics:
        clinic_city = normalize_text(clinic.get("city", ""))

        if city_normalized in clinic_city or clinic_city in city_normalized:
            if clinic.get("emergency_available") is True:
                emergency_clinics.append(clinic)

    if not emergency_clinics:
        return {
            "success": False,
            "message": "No emergency-supported clinic was found in this city. Please contact local emergency services immediately if the case is serious.",
        }

    selected_clinic = emergency_clinics[0]

    alert_id = save_emergency_alert(
        patient_name=patient_name,
        patient_phone=patient_phone,
        city=city,
        clinic_name=selected_clinic["name"],
        symptoms=symptoms,
        urgency_level=urgency_level,
    )

    return {
        "success": True,
        "message": "Emergency alert sent successfully.",
        "alert_id": alert_id,
        "patient_name": patient_name,
        "patient_phone": patient_phone,
        "clinic_name": selected_clinic["name"],
        "clinic_phone": selected_clinic["phone"],
        "symptoms": symptoms,
        "urgency_level": urgency_level,
        "safety_note": "If symptoms are life-threatening, contact local emergency services immediately.",
    }


def ask_knowledge_base_logic(question: str):
    context = build_rag_context(question)

    return {
        "success": True,
        "question": question,
        "knowledge_context": context,
    }


def estimate_cost_logic(monthly_patients: int = 1000):
    token_cost_per_patient = 0.003
    server_monthly_cost = 10
    database_monthly_cost = 0

    ai_cost = monthly_patients * token_cost_per_patient
    total_cost = ai_cost + server_monthly_cost + database_monthly_cost

    suggested_subscription_price = 29

    return {
        "monthly_patients": monthly_patients,
        "estimated_ai_cost_usd": round(ai_cost, 2),
        "server_monthly_cost_usd": server_monthly_cost,
        "database_monthly_cost_usd": database_monthly_cost,
        "estimated_total_cost_usd": round(total_cost, 2),
        "suggested_subscription_price_usd": suggested_subscription_price,
        "business_note": "The project can be sold to small and medium clinics as a monthly subscription.",
    }


@tool("Clinic Search Tool")
def clinic_search_tool(city: str, specialty: str) -> str:
    """
    Search for clinics by city and medical specialty.
    Use this when the patient asks for a suitable clinic.
    """
    results = find_clinics_logic(city, specialty)

    if not results:
        return "No clinic found for the selected city and specialty."

    return format_json(results)


@tool("Doctor Availability Tool")
def doctor_availability_tool(city: str, specialty: str) -> str:
    """
    Find available doctors and appointment slots by city and specialty.
    Use this before booking an appointment.
    """
    result = get_availability_logic(city, specialty)
    return format_json(result)


@tool("Appointment Booking Tool")
def appointment_booking_tool(
    patient_name: str,
    patient_phone: str,
    city: str,
    specialty: str,
    preferred_slot: str = "",
) -> str:
    """
    Book a clinic appointment for a patient and generate a booking code.
    Use this when the patient confirms that they want to book.
    """
    result = book_appointment_logic(
        patient_name=patient_name,
        patient_phone=patient_phone,
        city=city,
        specialty=specialty,
        preferred_slot=preferred_slot,
    )

    return format_json(result)


@tool("Clinic Knowledge Tool")
def clinic_knowledge_tool(question: str) -> str:
    """
    Search the clinic knowledge base using RAG and return relevant information.
    Use this for questions about booking policy, FAQ, emergency rules, and clinic instructions.
    """
    result = ask_knowledge_base_logic(question)
    return format_json(result)


@tool("Emergency Alert Tool")
def emergency_alert_tool(
    patient_name: str,
    patient_phone: str,
    city: str,
    symptoms: str,
    urgency_level: str = "high",
) -> str:
    """
    Send an emergency alert to a clinic that supports emergency cases.
    Use this when the patient describes an urgent or emergency situation.
    """
    result = send_emergency_alert_logic(
        patient_name=patient_name,
        patient_phone=patient_phone,
        city=city,
        symptoms=symptoms,
        urgency_level=urgency_level,
    )

    return format_json(result)


@tool("Cost Estimator Tool")
def cost_estimator_tool(monthly_patients: int = 1000) -> str:
    """
    Estimate the monthly operating cost of the Smart Clinic AI Agent.
    Use this for business plan and investor questions.
    """
    result = estimate_cost_logic(monthly_patients)
    return format_json(result)


SMART_CLINIC_TOOLS = [
    clinic_search_tool,
    doctor_availability_tool,
    appointment_booking_tool,
    clinic_knowledge_tool,
    emergency_alert_tool,
    cost_estimator_tool,
]


if __name__ == "__main__":
    print("1) Clinic Search Test")
    print(format_json(find_clinics_logic("Nablus", "Dentistry")))

    print("\n2) Availability Test")
    print(format_json(get_availability_logic("Nablus", "Dentistry")))

    print("\n3) Booking Test")
    print(
        format_json(
            book_appointment_logic(
                patient_name="Test Patient",
                patient_phone="0599999999",
                city="Nablus",
                specialty="Dentistry",
                preferred_slot="Saturday 10:30",
            )
        )
    )

    print("\n4) Knowledge Base Test")
    print(format_json(ask_knowledge_base_logic("Can I cancel my appointment?")))

    print("\n5) Emergency Alert Test")
    print(
        format_json(
            send_emergency_alert_logic(
                patient_name="Emergency Patient",
                patient_phone="0598888888",
                city="Nablus",
                symptoms="Severe tooth pain and swelling",
                urgency_level="medium",
            )
        )
    )

    print("\n6) Cost Estimator Test")
    print(format_json(estimate_cost_logic(1000)))