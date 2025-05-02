import React, { useState, useRef, useEffect } from "react";
import { X, MessageSquare, Send, Loader2, AlertTriangle } from "lucide-react";
import { GoogleGenerativeAI } from "@google/generative-ai";
 // use rinputs
const Chatbot = ({ onClose }) => {
  const API_KEY = import.meta.env.VITE_GEMINI_API_KEY;
  const [activeTab, setActiveTab] = useState("form");
  const [symptoms, setSymptoms] = useState("");
  const [age, setAge] = useState("");
  const [mobility, setMobility] = useState("");
  const [allergies, setAllergies] = useState("");
  const [conditions, setConditions] = useState("");
  const [surgeries, setSurgeries] = useState("");
  const [immunization, setImmunization] = useState("");
  const [otherNotes, setOtherNotes] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [modeOfCare, setModeOfCare] = useState("In person");

  const [responseText, setResponseText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const responseRef = useRef(null);

  // Auto-scroll to bottom when response changes
  useEffect(() => {
    if (responseText && responseRef.current) {
      responseRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [responseText]);

  const hospitalData = [
    { Name: "University of Cincinnati Medical Center", Latitude: 39.1412, Longitude: -84.5059 },
    { Name: "Cincinnati VA Medical Center", Latitude: 39.1398, Longitude: -84.5039 },
    { Name: "Christ Hospital", Latitude: 39.1231, Longitude: -84.507 },
    { Name: "Cleveland Clinic", Latitude: 41.5033, Longitude: -81.62 },
    { Name: "Mount Carmel East", Latitude: 39.9828, Longitude: -82.8291 },
  ];

  const generatePrompt = () => {
    const patientCondition = {
      Age: age,
      "Mobility Issues": mobility,
      "Known Allergies": allergies.split(",").map((a) => a.trim()).filter(Boolean),
      "Chronic Conditions": conditions.split(",").map((c) => c.trim()).filter(Boolean),
      "Recent Surgeries": surgeries,
      "Immunization Status": immunization,
      "Other Notes": otherNotes,
    };

    const geographicLocation = {
      Country: "United States",
      State: state,
      City: city,
      "Preferred Mode of Care": modeOfCare,
    };

    const symptomList = symptoms.split(",").map((s) => s.trim()).filter(Boolean);

    return `
You are a healthcare AI assistant tasked with generating a customized treatment plan for a patient. Given the following inputs:

1. Symptoms: ${JSON.stringify(symptomList)}
2. Physical Condition: ${JSON.stringify(patientCondition, null, 2)}
3. Location: ${JSON.stringify(geographicLocation, null, 2)}
4. Hospitals: ${JSON.stringify(hospitalData, null, 2)}

Generate a treatment plan that includes:

1. Medical Actions
2. Location-Specific Options
3. Justifications

Be concise, medically accurate, and context-aware. Avoid unnecessary medical jargon.
    `;
  };

  const handleGeneratePlan = async () => {
    if (!symptoms.trim()) {
      setResponseText("⚠️ Please enter at least one symptom to generate a treatment plan.");
      setActiveTab("response");
      return;
    }
    
    setIsLoading(true);
    setActiveTab("response");
    
    try {
      const genAI = new GoogleGenerativeAI(API_KEY);
      const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

      const result = await model.generateContent({
        contents: [{ parts: [{ text: generatePrompt() }] }],
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 1200,
        },
      });

      setResponseText(result.response.text());
    } catch (err) {
      console.error("Gemini Error:", err);
      setResponseText("⚠️ Error generating treatment plan. Please check your inputs and try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const formFields = [
    { label: "Symptoms", value: symptoms, onChange: setSymptoms, placeholder: "Fever, cough, headache", required: true },
    { label: "Age", value: age, onChange: setAge, placeholder: "25", width: "half" },
    { label: "Mobility Issues", value: mobility, onChange: setMobility, placeholder: "None, wheelchair, limited walking", width: "half" },
    { label: "Allergies", value: allergies, onChange: setAllergies, placeholder: "Penicillin, peanuts, latex", width: "half" },
    { label: "Chronic Conditions", value: conditions, onChange: setConditions, placeholder: "Asthma, diabetes, hypertension", width: "half" },
    { label: "Recent Surgeries", value: surgeries, onChange: setSurgeries, placeholder: "Appendectomy (2 months ago)" },
    { label: "Immunization Status", value: immunization, onChange: setImmunization, placeholder: "Up to date, missing flu shot" },
    { label: "Other Notes", value: otherNotes, onChange: setOtherNotes, placeholder: "Currently pregnant, taking medication" },
    { label: "City", value: city, onChange: setCity, placeholder: "Cincinnati", width: "half" },
    { label: "State", value: state, onChange: setState, placeholder: "Ohio", width: "half" }
  ];

  return (
    <div className="fixed bottom-20 left-4 bg-white w-96 md:w-[32rem] h-[38rem] shadow-xl rounded-xl border border-gray-200 flex flex-col z-20 overflow-hidden">
      {/* Header */}
      <div className="flex justify-between items-center bg-blue-600 text-white p-3 rounded-t-xl">
        <div className="flex items-center space-x-2">
          <MessageSquare size={20} />
          <span className="text-lg font-semibold">RE-ASSIST Chatbot</span>
        </div>
        <button 
          onClick={onClose} 
          className="text-white hover:text-red-200 transition-colors p-1 rounded-full hover:bg-blue-700"
          aria-label="Close"
        >
          <X size={20} />
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        <button
          className={`flex-1 py-2 font-medium text-sm ${
            activeTab === "form" ? "text-blue-600 border-b-2 border-blue-600" : "text-gray-500 hover:text-blue-500"
          }`}
          onClick={() => setActiveTab("form")}
        >
          Patient Information
        </button>
        <button
          className={`flex-1 py-2 font-medium text-sm ${
            activeTab === "response" ? "text-blue-600 border-b-2 border-blue-600" : "text-gray-500 hover:text-blue-500"
          }`}
          onClick={() => setActiveTab("response")}
          disabled={!responseText && !isLoading}
        >
          Treatment Plan
        </button>
      </div>

      {/* Content */}
      <div className="flex-grow overflow-y-auto p-4 bg-gray-50">
        {activeTab === "form" ? (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              {formFields.map((field) => (
                <div key={field.label} className={field.width === "half" ? "col-span-1" : "col-span-2"}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label} {field.required && <span className="text-red-500">*</span>}
                  </label>
                  <input
                    value={field.value}
                    onChange={(e) => field.onChange(e.target.value)}
                    placeholder={field.placeholder}
                    className="w-full border border-gray-300 p-2 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  />
                </div>
              ))}
              
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Preferred Care</label>
                <select
                  value={modeOfCare}
                  onChange={(e) => setModeOfCare(e.target.value)}
                  className="w-full border border-gray-300 p-2 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white"
                >
                  <option>In person</option>
                  <option>Telehealth</option>
                  <option>Either</option>
                </select>
              </div>
            </div>

            <button
              onClick={handleGeneratePlan}
              className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 flex items-center justify-center transition-colors font-medium shadow-sm disabled:bg-blue-300"
              disabled={isLoading || !symptoms.trim()}
            >
              {isLoading ? (
                <>
                  <Loader2 size={18} className="animate-spin mr-2" />
                  Generating...
                </>
              ) : (
                <>
                  <Send size={18} className="mr-2" />
                  Generate Treatment Plan
                </>
              )}
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm p-4 h-full">
            {isLoading ? (
              <div className="flex flex-col items-center justify-center h-full text-gray-500">
                <Loader2 size={32} className="animate-spin mb-4 text-blue-600" />
                <p>Generating your personalized treatment plan...</p>
                <p className="text-sm text-gray-400 mt-2">This may take a few moments</p>
              </div>
            ) : responseText ? (
              <div className="prose prose-sm max-w-none">
                <div className="whitespace-pre-wrap">{responseText}</div>
                <div ref={responseRef} />
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-gray-500">
                <AlertTriangle size={32} className="mb-4 text-amber-500" />
                <p>No treatment plan generated yet</p>
                <p className="text-sm text-gray-400 mt-2">Fill out the patient information first</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-gray-100 py-2 px-4 text-xs text-gray-500 text-center border-t border-gray-200">
        This is for test only, Awlays contact doctor :Gaurab
      </div>
    </div>
  );
};

export default Chatbot;