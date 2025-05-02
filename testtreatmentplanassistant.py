# test_treatment_assistant.py
import unittest
from unittest.mock import patch, MagicMock
from assessment import TreatmentPlanAssistant

class TestTreatmentPlanAssistant(unittest.TestCase):
    
    def setup_mocks(self, inputs, coords=(39.1412, -84.5059)):
        # Stop existing patches if any
        for patch_name in ['input_patch', 'geo_patch', 'client_patch']:
            if hasattr(self, patch_name):
                getattr(self, patch_name).stop()
                
        # Input mocking
        self.input_patch = patch('builtins.input')
        self.mock_input = self.input_patch.start()
        self.mock_input.side_effect = inputs
        
        # Geolocation mocking
        self.geo_patch = patch.object(TreatmentPlanAssistant, 'get_city_coordinates')
        self.mock_geo = self.geo_patch.start()
        self.mock_geo.return_value = coords
        
        # AI client mocking
        self.client_patch = patch('assessment.genai.Client')
        self.mock_client = self.client_patch.start()
        mock_response = MagicMock()
        mock_response.text = self.generate_mock_response(inputs)
        self.mock_client.return_value.models.generate_content.return_value = mock_response

    def generate_mock_response(self, inputs):
        """Generate context-aware mock response"""
        age = inputs[1]
        conditions = inputs[4]
        mode = inputs[-1]
        
        response = [
            "Medical Actions:",
            "- Symptom management",
            "- Consider comorbidities" if conditions else "",
            "- Pediatric care" if age == '0' else "- Geriatric care" if age == '100' else "- Standard care",
            "",
            "Location-Specific Options:",
            f"- {mode} services available" if mode != 'Either' else "- Both service types available",
            "- Nearby hospitals sorted by distance",
            "",
            "Justifications:",
            "- Age-appropriate considerations" if age in ('0', '100') else "- General medical guidelines",
            f"- Chronic condition management" if conditions else ""
        ]
        return '\n'.join([line for line in response if line])

    def tearDown(self):
        for patch_name in ['input_patch', 'geo_patch', 'client_patch']:
            if hasattr(self, patch_name):
                getattr(self, patch_name).stop()

    # Test Case 1: Basic Functionality
    def test_typical_case(self):
        inputs = ["Fever, Cough", "35", "None", "Penicillin", "Asthma", "", 
                 "Up-to-date", "", "Cincinnati", "OH", "Either"]
        self.setup_mocks(inputs)
        
        assistant = TreatmentPlanAssistant()
        assistant.collect_inputs()
        plan = assistant.generate_plan()
        
        self.assertIn("Asthma", plan)
        self.assertIn("Chronic condition management", plan)

    # Test Case 2: Telehealth Preference
    def test_telehealth_preference(self):
        inputs = ["Rash, Itching", "28", "Temporary leg injury", "", "", 
                 "", "", "", "Cincinnati", "OH", "Telehealth"]
        self.setup_mocks(inputs)
        
        assistant = TreatmentPlanAssistant()
        assistant.collect_inputs()
        plan = assistant.generate_plan()
        
        self.assertIn("Telehealth services available", plan)
        self.assertIn("leg injury", ' '.join(inputs))  # Verify input handling

    # Test Case 3: Invalid Location Handling
    def test_invalid_location(self):
        with patch.object(TreatmentPlanAssistant, 'get_city_coordinates') as mock_geo:
            mock_geo.side_effect = ValueError("Coordinates not found")
            assistant = TreatmentPlanAssistant()
            with self.assertRaises(ValueError):
                assistant.get_city_coordinates("Narnia", "ZZ")

    # Test Case 4: Age Extremes
    def test_age_extremes(self):
        # Newborn
        inputs = ["Poor feeding", "0", "", "", "", "", "", "", "Columbus", "OH", "Either"]
        self.setup_mocks(inputs)
        plan = TreatmentPlanAssistant().generate_plan()
        self.assertIn("Pediatric care", plan)

        # Elderly
        inputs = ["Joint pain", "100", "Uses walker", "", "Arthritis", 
                 "", "", "", "Cleveland", "OH", "In person"]
        self.setup_mocks(inputs)
        plan = TreatmentPlanAssistant().generate_plan()
        self.assertIn("Geriatric care", plan)
        self.assertIn("Fall Prevention", plan)

    # Test Case 5: Empty Medical History
    def test_minimal_input(self):
        inputs = ["Headache", "30", "", "", "", "", "", "", "Columbus", "OH", "Either"]
        self.setup_mocks(inputs, coords=(39.9828, -82.8291))
        
        assistant = TreatmentPlanAssistant()
        assistant.collect_inputs()
        hospitals = sorted(assistant.hospital_data, 
                          key=lambda x: x['Distance (miles)'])
        self.assertEqual(hospitals[0]['Name'], "Mount Carmel East")

if __name__ == '__main__':
    unittest.main()