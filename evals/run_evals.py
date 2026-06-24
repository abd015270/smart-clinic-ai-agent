import json
from pathlib import Path

from src.tools import (
    book_appointment_logic,
    ask_knowledge_base_logic,
    send_emergency_alert_logic,
    get_availability_logic,
)


BASE_DIR = Path(__file__).resolve().parent.parent
EVAL_CASES_FILE = BASE_DIR / "evals" / "eval_cases.json"


def load_eval_cases():
    with open(EVAL_CASES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def contains_expected_keywords(response: str, expected_keywords: list[str]):
    response_lower = response.lower()
    found_keywords = []

    for keyword in expected_keywords:
        if keyword.lower() in response_lower:
            found_keywords.append(keyword)

    score = len(found_keywords) / len(expected_keywords)

    return score, found_keywords


def run_fast_eval_case(case):
    case_id = case["id"]

    if case_id == 1:
        result = book_appointment_logic(
            patient_name="Daniel",
            patient_phone="0501112233",
            city="Tel Aviv",
            specialty="Dentistry",
            preferred_slot="Sunday 10:30",
        )
        response = json.dumps(result, ensure_ascii=False)

    elif case_id == 2:
        result = ask_knowledge_base_logic("Can I cancel my appointment?")
        response = json.dumps(result, ensure_ascii=False)

    elif case_id == 3:
        result = send_emergency_alert_logic(
            patient_name="Ariel",
            patient_phone="0502223333",
            city="Jerusalem",
            symptoms="Severe pain and swelling",
            urgency_level="high",
        )
        response = json.dumps(result, ensure_ascii=False)

    elif case_id == 4:
        result = get_availability_logic("Haifa", "Pediatrics")
        response = json.dumps(result, ensure_ascii=False)

    elif case_id == 5:
        result = ask_knowledge_base_logic("Does this system replace a real doctor?")
        response = json.dumps(result, ensure_ascii=False)

    else:
        response = "Unsupported eval case."

    keyword_score, found_keywords = contains_expected_keywords(
        response=response,
        expected_keywords=case["expected_keywords"],
    )

    passed = keyword_score >= 0.6

    return {
        "id": case["id"],
        "name": case["name"],
        "passed": passed,
        "score": round(keyword_score, 2),
        "found_keywords": found_keywords,
        "response_preview": response[:300],
    }


def run_all_evals():
    cases = load_eval_cases()
    results = []

    for case in cases:
        result = run_fast_eval_case(case)
        results.append(result)

    passed_count = sum(1 for result in results if result["passed"])
    total_count = len(results)
    success_rate = round((passed_count / total_count) * 100, 2)

    print("=" * 60)
    print("SMART CLINIC AI AGENT - EVAL RESULTS")
    print("=" * 60)

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] Case {result['id']}: {result['name']}")
        print(f"Score: {result['score']}")
        print(f"Found Keywords: {result['found_keywords']}")
        print("-" * 60)

    print(f"Passed: {passed_count}/{total_count}")
    print(f"Success Rate: {success_rate}%")

    return {
        "passed": passed_count,
        "total": total_count,
        "success_rate": success_rate,
        "results": results,
    }


if __name__ == "__main__":
    run_all_evals()