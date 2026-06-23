import streamlit as st
import pandas as pd

from src.database import (
    init_database,
    get_all_appointments,
    get_all_emergency_alerts,
)
from src.agent import run_smart_clinic_agent
from src.tools import (
    find_clinics_logic,
    get_availability_logic,
    book_appointment_logic,
    send_emergency_alert_logic,
    ask_knowledge_base_logic,
    estimate_cost_logic,
)


init_database()

st.set_page_config(
    page_title="Smart Clinic AI Agent",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Smart Clinic AI Agent")
st.caption("AI-powered clinic assistant for booking, clinic search, FAQ, and emergency alerts.")


menu = st.sidebar.radio(
    "Navigation",
    [
        "AI Agent Chat",
        "Find Clinic",
        "Book Appointment",
        "Emergency Alert",
        "Knowledge Base RAG",
        "Business Cost",
        "Dashboard",
    ],
)


if menu == "AI Agent Chat":
    st.header("🤖 AI Agent Chat")

    st.info(
        "This page uses the real CrewAI Agent with role, goal, backstory, tools, and decisions."
    )

    example = (
        "I am Ahmad, my phone is 0599999999. "
        "I need a dentist in Nablus and I prefer Saturday 10:30. "
        "Please book an appointment."
    )

    user_request = st.text_area(
        "Write the patient request",
        value=example,
        height=150,
    )

    if st.button("Run AI Agent"):
        if not user_request.strip():
            st.warning("Please write a patient request.")
        else:
            with st.spinner("Smart Clinic AI Agent is working..."):
                response = run_smart_clinic_agent(user_request)

            st.subheader("Agent Response")
            st.write(response)


elif menu == "Find Clinic":
    st.header("🔍 Find a Suitable Clinic")

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox(
            "City",
            ["Nablus", "Hebron", "Ramallah", "Jenin", "Bethlehem"],
        )

    with col2:
        specialty = st.selectbox(
            "Specialty",
            ["Dentistry", "Family Medicine", "Pediatrics", "Cardiology", "Dermatology"],
        )

    if st.button("Search Clinic"):
        results = find_clinics_logic(city, specialty)

        if not results:
            st.error("No clinic found for this city and specialty.")
        else:
            st.success(f"{len(results)} clinic found.")
            for clinic in results:
                st.markdown("---")
                st.subheader(clinic["name"])
                st.write(f"**City:** {clinic['city']}")
                st.write(f"**Specialty:** {clinic['specialty']}")
                st.write(f"**Address:** {clinic['address']}")
                st.write(f"**Phone:** {clinic['phone']}")
                st.write(f"**Rating:** {clinic['rating']}")
                st.write(f"**Working Hours:** {clinic['working_hours']}")
                st.write(
                    f"**Emergency Available:** {'Yes' if clinic['emergency_available'] else 'No'}"
                )


elif menu == "Book Appointment":
    st.header("📅 Book an Appointment")

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name", value="Ahmad")
        city = st.selectbox(
            "City",
            ["Nablus", "Hebron", "Ramallah", "Jenin", "Bethlehem"],
            key="book_city",
        )
        specialty = st.selectbox(
            "Specialty",
            ["Dentistry", "Family Medicine", "Pediatrics", "Cardiology", "Dermatology"],
            key="book_specialty",
        )

    with col2:
        patient_phone = st.text_input("Patient Phone", value="0599999999")
        preferred_slot = st.text_input(
            "Preferred Slot",
            value="Saturday 10:30",
            help="Example: Saturday 10:30",
        )

    if st.button("Show Available Doctors"):
        availability = get_availability_logic(city, specialty)

        if not availability["success"]:
            st.error(availability["message"])
        else:
            st.success(availability["message"])
            st.json(availability["data"])

    if st.button("Confirm Booking"):
        if not patient_name.strip() or not patient_phone.strip():
            st.warning("Patient name and phone are required.")
        else:
            result = book_appointment_logic(
                patient_name=patient_name,
                patient_phone=patient_phone,
                city=city,
                specialty=specialty,
                preferred_slot=preferred_slot,
            )

            if result["success"]:
                st.success("Appointment booked successfully.")
                st.markdown("### Booking Details")
                st.write(f"**Patient:** {result['patient_name']}")
                st.write(f"**Phone:** {result['patient_phone']}")
                st.write(f"**Clinic:** {result['clinic_name']}")
                st.write(f"**Doctor:** {result['doctor_name']}")
                st.write(f"**Time:** {result['appointment_slot']}")
                st.write(f"**Booking Code:** `{result['booking_code']}`")
                st.info(result["important_note"])
            else:
                st.error(result["message"])


elif menu == "Emergency Alert":
    st.header("🚨 Emergency Alert")

    st.warning(
        "This feature is for demo purposes. If symptoms are life-threatening, contact local emergency services immediately."
    )

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name", value="Emergency Patient")
        patient_phone = st.text_input("Patient Phone", value="0598888888")
        city = st.selectbox(
            "City",
            ["Nablus", "Hebron", "Ramallah", "Jenin", "Bethlehem"],
            key="emergency_city",
        )

    with col2:
        urgency_level = st.selectbox(
            "Urgency Level",
            ["low", "medium", "high"],
            index=2,
        )
        symptoms = st.text_area(
            "Symptoms",
            value="Severe pain and swelling",
            height=120,
        )

    if st.button("Send Emergency Alert"):
        result = send_emergency_alert_logic(
            patient_name=patient_name,
            patient_phone=patient_phone,
            city=city,
            symptoms=symptoms,
            urgency_level=urgency_level,
        )

        if result["success"]:
            st.success("Emergency alert sent successfully.")
            st.write(f"**Clinic:** {result['clinic_name']}")
            st.write(f"**Clinic Phone:** {result['clinic_phone']}")
            st.write(f"**Urgency:** {result['urgency_level']}")
            st.info(result["safety_note"])
        else:
            st.error(result["message"])


elif menu == "Knowledge Base RAG":
    st.header("📚 Knowledge Base RAG")

    st.info(
        "This page demonstrates RAG by searching local clinic FAQ, booking policy, and emergency guideline files."
    )

    question = st.text_input(
        "Ask a question",
        value="Can I cancel my appointment?",
    )

    if st.button("Search Knowledge Base"):
        result = ask_knowledge_base_logic(question)

        st.subheader("RAG Result")
        st.write(f"**Question:** {result['question']}")
        st.text_area(
            "Retrieved Context",
            value=result["knowledge_context"],
            height=350,
        )


elif menu == "Business Cost":
    st.header("💰 Business Cost Estimator")

    monthly_patients = st.number_input(
        "Expected monthly patients",
        min_value=100,
        max_value=100000,
        value=1000,
        step=100,
    )

    if st.button("Estimate Cost"):
        result = estimate_cost_logic(monthly_patients)

        col1, col2, col3 = st.columns(3)

        col1.metric("AI Cost / Month", f"${result['estimated_ai_cost_usd']}")
        col2.metric("Server Cost / Month", f"${result['server_monthly_cost_usd']}")
        col3.metric("Total Cost / Month", f"${result['estimated_total_cost_usd']}")

        st.write(f"**Suggested Subscription Price:** ${result['suggested_subscription_price_usd']} / clinic / month")
        st.info(result["business_note"])


elif menu == "Dashboard":
    st.header("📊 Clinic Dashboard")

    appointments = get_all_appointments()
    emergency_alerts = get_all_emergency_alerts()

    col1, col2 = st.columns(2)

    col1.metric("Total Appointments", len(appointments))
    col2.metric("Emergency Alerts", len(emergency_alerts))

    st.markdown("---")

    st.subheader("Recent Appointments")

    if appointments:
        appointments_df = pd.DataFrame(
            appointments,
            columns=[
                "ID",
                "Patient",
                "Phone",
                "City",
                "Specialty",
                "Clinic",
                "Doctor",
                "Slot",
                "Booking Code",
                "Status",
                "Created At",
            ],
        )
        st.dataframe(appointments_df, use_container_width=True)
    else:
        st.info("No appointments yet.")

    st.subheader("Recent Emergency Alerts")

    if emergency_alerts:
        emergency_df = pd.DataFrame(
            emergency_alerts,
            columns=[
                "ID",
                "Patient",
                "Phone",
                "City",
                "Clinic",
                "Symptoms",
                "Urgency",
                "Status",
                "Created At",
            ],
        )
        st.dataframe(emergency_df, use_container_width=True)
    else:
        st.info("No emergency alerts yet.")