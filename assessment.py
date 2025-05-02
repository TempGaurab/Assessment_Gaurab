import os
import json
from dotenv import load_dotenv
from google import genai
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class TreatmentPlanAssistant:
    def __init__(self): #All of this is intializing stuff
        load_dotenv()
        self.api_key = os.getenv('Gemini_Api_Key')
        self.client = genai.Client(api_key=self.api_key)
        self.symptoms = []
        self.patient_condition = {}
        self.geographic_location = {}
        self.patient_coords = ()  # Will be auto-populated
        self.hospital_data = [
            {
                "Name": "University of Cincinnati Medical Center",
                "Latitude": 39.1412,
                "Longitude": -84.5059,
                "Services Offered": "Either"
            },
            {
                "Name": "Cincinnati VA Medical Center",
                "Latitude": 39.1398,
                "Longitude": -84.5039,
                "Services Offered": "In person"
            },
            {
                "Name": "Christ Hospital",
                "Latitude": 39.1231,
                "Longitude": -84.507,
                "Services Offered": "Telehealth"
            },
            {
                "Name": "Cleveland Clinic",
                "Latitude": 41.5033,
                "Longitude": -81.62,
                "Services Offered": "Either"
            },
            {
                "Name": "Mount Carmel East",
                "Latitude": 39.9828,
                "Longitude": -82.8291,
                "Services Offered": "In person"
            },
        ]

    def get_city_coordinates(self, city, state): #this is the library that helps use get latitude and longitude of the user input
        geolocator = Nominatim(user_agent="treatment-plan-assistant")
        location = geolocator.geocode(f"{city}, {state}, United States")
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError("Could not find coordinates for the provided location.")

    def collect_inputs(self): # this collect input is collecting all details of the user
        self.symptoms = [s.strip() for s in input("Enter patient symptoms (comma separated): ").split(",") if s.strip()]
        age = input("Enter patient age: ")
        mobility = input("Describe mobility issues: ")
        allergies = [a.strip() for a in input("List known allergies (comma separated): ").split(",") if a.strip()]
        conditions = [c.strip() for c in input("List chronic conditions (comma separated): ").split(",") if c.strip()]
        surgeries = input("Recent surgeries (if any): ")
        immunization = input("Immunization status: ")
        other_notes = input("Any other notes: ")
        city = input("City: ")
        state = input("State: ")
        mode_of_care = input("Preferred mode of care (In person / Telehealth / Either): ")

        self.patient_coords = self.get_city_coordinates(city, state)

        self.patient_condition = {
            "Age": age,
            "Mobility Issues": mobility,
            "Known Allergies": allergies,
            "Chronic Conditions": conditions,
            "Recent Surgeries": surgeries,
            "Immunization Status": immunization,
            "Other Notes": other_notes
        }

        self.geographic_location = {
            "Country": "United States",
            "State": state,
            "City": city,
            "Preferred Mode of Care": mode_of_care
        }

        self.add_hospital_distances()

    def add_hospital_distances(self): #this code is adding the distance of the hopitals with the hopsital data
        for hospital in self.hospital_data:
            hosp_coords = (hospital["Latitude"], hospital["Longitude"])
            distance = geodesic(self.patient_coords, hosp_coords).miles
            hospital["Distance (miles)"] = round(distance, 2)

    def generate_prompt(self): #prompt
        return f"""
            You are a healthcare AI assistant tasked with generating a customized treatment plan for a patient. Given the following inputs:

            1. Symptoms: {json.dumps(self.symptoms)}
            2. Physical Condition: {json.dumps(self.patient_condition, indent=2)}
            3. Location: {json.dumps(self.geographic_location, indent=2)}
            4. Hospitals: {json.dumps(self.hospital_data, indent=2)}

            Generate a treatment plan that includes:

            1. Medical Actions
            2. Location-Specific Options
            3. Justifications

            Be concise, medically accurate, and context-aware. Avoid unnecessary medical jargon. Just provide the plan.
            """

    def generate_plan(self): #main funciton that calls the bot
        prompt = self.generate_prompt()
        print("Generating plan.......")
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text

    def display_plan(self, text): #displays the output of the code
        print("\n===== Customized Treatment Plan =====\n")
        sections = text.strip().split('\n\n')
        for section in sections:
            if section.strip():
                print(section)
                print("-" * 60)

if __name__ == "__main__": #call the program in our code
    print("Starting program")
    assistant = TreatmentPlanAssistant()
    assistant.collect_inputs()
    plan = assistant.generate_plan()
    assistant.display_plan(plan)
