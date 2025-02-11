from clinic.patient import Patient
import json

class PatientDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    def object_hook(self, obj):
        if 'phn' in obj:  # Check if it's a Patient-like dictionary
            return Patient(obj['phn'], obj['name'], obj['birth_date'], obj['phone'], obj['email'], obj['address'])
        return obj