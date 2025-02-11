from clinic.patient import Patient
import json

class PatientEncoder(json.JSONEncoder):
    def default(self, obj):

        #checking if the type of object (instance) is of type patient
        if isinstance(obj, Patient):

            #returning in json format
            return {
                'phn': obj.phn,
                'name': obj.name,
                'birth_date': obj.birth_date,
                'phone': obj.phone,
                'email': obj.email,
                'address': obj.address
            }
        return super().default(obj)