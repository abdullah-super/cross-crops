import os

sequence_uml = """
@startuml
actor User
participant "Web Browser" as Browser
participant "Flask Server" as Server
participant "Preprocessing Module" as Preproc
participant "Model Prediction" as Model

User -> Browser: Open Home Page (/)
Browser -> Server: GET /
Server --> Browser: Render UI

User -> Browser: Fill in Prediction Form (Country, Crop, Year, Temp, Rainfall, Pesticides)
Browser -> Server: POST /predict (JSON payload)
Server -> Preproc: preprocess_input(...)
note right of Preproc: Process input and do feature engineering
Preproc --> Server: Processed features
Server -> Model: model.predict(features)
Model --> Server: Prediction result
Server -> Server: Prepare response (interpretation, unit conversion)
Server --> Browser: JSON response with prediction details
Browser -> User: Display prediction result
@enduml
"""

# Write the UML to a file
uml_file = "sequence_diagram.uml"
with open(uml_file, "w") as f:
    f.write(sequence_uml)

# Generate the PNG diagram using PlantUML (ensure PlantUML is installed)
os.system(f"plantuml {uml_file}")

print("Sequence diagram UML file created and PNG diagram generated as 'sequence_diagram.png'")