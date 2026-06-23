from crewai import Agent, Task, Crew, Process

from src.config import OPENAI_API_KEY, OPENAI_MODEL, SKILLS_DIR
from src.tools import SMART_CLINIC_TOOLS


def load_clinic_skill():
    skill_file = SKILLS_DIR / "clinic_agent_skill" / "SKILL.md"

    if not skill_file.exists():
        return ""

    return skill_file.read_text(encoding="utf-8")


def has_valid_api_key():
    return bool(OPENAI_API_KEY and OPENAI_API_KEY != "ضع_المفتاح_هنا")


def build_smart_clinic_agent():
    skill_content = load_clinic_skill()

    backstory = f"""
You are an experienced AI clinic assistant working for Smart Clinic AI Agent.

You support small and medium medical clinics by helping patients find clinics,
check doctor availability, book appointments, answer booking questions, and handle
emergency requests.

You must use the provided tools when you need clinic data, appointment slots,
booking actions, emergency alerts, knowledge base information, or business cost estimation.

You are not a doctor and you must not provide medical diagnosis.

Specialized skill instructions:
{skill_content}
"""

    return Agent(
        role="Smart Clinic Patient Assistant",
        goal=(
            "Help patients find the right clinic, understand clinic policies, "
            "book appointments, and send emergency alerts when needed."
        ),
        backstory=backstory,
        tools=SMART_CLINIC_TOOLS,
        verbose=True,
        allow_delegation=False,
    )


def run_smart_clinic_agent(user_request: str) -> str:
    if not has_valid_api_key():
        return (
            "OPENAI_API_KEY is missing. Add your OpenAI API key inside the .env file "
            "to run the real CrewAI agent. Do not share the key in chat."
        )

    agent = build_smart_clinic_agent()

    task = Task(
        description=f"""
Patient request:
{user_request}

Your job:
1. Understand what the patient needs.
2. Use the correct tool when needed.
3. If the patient wants a clinic, search by city and specialty.
4. If the patient wants available appointments, check doctor availability.
5. If the patient confirms booking, use the appointment booking tool.
6. If the patient asks about rules or FAQ, use the knowledge base tool.
7. If the patient describes an emergency, use the emergency alert tool.
8. Never provide medical diagnosis.
9. Return a clear, organized answer.
""",
        expected_output=(
            "A clear patient-facing response that includes the relevant clinic, "
            "doctor, appointment, booking code, policy answer, or emergency alert result."
        ),
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)


if __name__ == "__main__":
    test_request = (
        "I am Ahmad, my phone is 0599999999. "
        "I need a dentist in Nablus and I prefer Saturday 10:30. "
        "Please book an appointment."
    )

    response = run_smart_clinic_agent(test_request)
    print("\nFINAL RESPONSE:")
    print(response)