from assessment import TreatmentPlanAssistant  
import datetime

# Sample test input sets
test_cases = [
    {
        "symptoms": ["Fever", "Cough"],
        "condition": {
            "Age": "30",
            "Mobility Issues": "None",
            "Known Allergies": ["Penicillin"],
            "Chronic Conditions": ["Asthma"],
            "Recent Surgeries": "None",
            "Immunization Status": "Up to date",
            "Other Notes": "Mild fatigue"
        },
        "location": {
            "City": "Cincinnati",
            "State": "Ohio",
            "Preferred Mode of Care": "Either"
        }
    },
    {
        "symptoms": ["Headache", "Blurred vision"],
        "condition": {
            "Age": "45",
            "Mobility Issues": "None",
            "Known Allergies": ["None"],
            "Chronic Conditions": ["Hypertension"],
            "Recent Surgeries": "Eye surgery 6 months ago",
            "Immunization Status": "Incomplete",
            "Other Notes": "Occasional dizziness"
        },
        "location": {
            "City": "Cleveland",
            "State": "Ohio",
            "Preferred Mode of Care": "In person"
        }
    },
    {
        "symptoms": ["Joint pain", "Swelling"],
        "condition": {
            "Age": "60",
            "Mobility Issues": "Moderate",
            "Known Allergies": ["Sulfa drugs"],
            "Chronic Conditions": ["Arthritis", "Diabetes"],
            "Recent Surgeries": "Knee replacement",
            "Immunization Status": "Up to date",
            "Other Notes": "Takes insulin daily"
        },
        "location": {
            "City": "Columbus",
            "State": "Ohio",
            "Preferred Mode of Care": "Telehealth"
        }
    }
]

# Save results to file
output_file = "treatment_plans_report.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Treatment Plans Report - {datetime.datetime.now()}\n")
    f.write("=" * 80 + "\n\n")
    for i, case in enumerate(test_cases, start=1):
        assistant = TreatmentPlanAssistant()
        assistant.symptoms = case["symptoms"]
        assistant.patient_condition = case["condition"]
        assistant.geographic_location = {
            "Country": "United States",
            "State": case["location"]["State"],
            "City": case["location"]["City"],
            "Preferred Mode of Care": case["location"]["Preferred Mode of Care"]
        }
        assistant.patient_coords = assistant.get_city_coordinates(case["location"]["City"], case["location"]["State"])
        assistant.add_hospital_distances()
        plan = assistant.generate_plan()

        f.write(f"Test Case {i}\n")
        f.write(f"Symptoms: {case['symptoms']}\n")
        f.write(f"Location: {case['location']['City']}, {case['location']['State']}\n\n")
        f.write(plan.strip())
        f.write("\n" + "-" * 80 + "\n\n")

print(f"Report written to {output_file}")
