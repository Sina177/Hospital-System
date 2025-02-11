from .patient_dao import PatientDAO
from clinic.patient import Patient
from .patient_encoder import PatientEncoder
from .patient_decoder import PatientDecoder
import json


class PatientDAOJSON(PatientDAO):

    def __init__(self, autosave=True) -> None:
        self.patient_list = []
        self.autosave = autosave

        #loads the patients into patient list if autosave is on, otherwise the list is empty
        if self.autosave == True:
            try:
                with open("./clinic/patients.json", "r") as file:
                    self.patient_list = json.load(file, cls=PatientDecoder)

            except FileNotFoundError:
                self.patient_list = []

    #this is a helper method to make it easier to write the file data in the funtions bellow
    def write_to_file(self):
        if self.autosave:
            with open('./clinic/patients.json', 'w') as file:
                json.dump(self.patient_list, file, cls=PatientEncoder)
    
    #searches for a patient by phn then returns the patient
    def search_patient(self, phn: int) -> 'Patient':
        for patient in self.patient_list:
            if patient.phn == phn:
                return patient
    
    #creates a patient by the given fields and writes the new data into the json file
    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> 'Patient':
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        self.patient_list.append(new_patient)
        self.write_to_file()
        return new_patient

    #retreives a list of patients and returns all that contain the matching search name
    def retrieve_patients(self, search_name: str) -> "list[Patient]":
        list_of_patients = []
        for patient in self.patient_list:
            if search_name.lower() in patient.name.lower():
                list_of_patients.append(patient)
        return list_of_patients

    #updating the patient with the new inputed fields and then writing the new data to the json file
    def update_patient(self, phn_given: int, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> 'Patient':

            for patient in self.patient_list:
                if phn_given == patient.phn:
                    patient.phn = phn
                    patient.name = name
                    patient.birth_date = birth_date
                    patient.phone = phone
                    patient.email = email
                    patient.address = address
                    self.write_to_file()
                    return patient

    #deleteing the patient by phn and updating the json file
    def delete_patient(self, phn: int) -> bool:
        for patient in self.patient_list:
            if patient.phn == phn:
                self.patient_list.remove(patient)
                self.write_to_file()
                return True

    #returning a list of all patients
    def list_patients(self) -> "list[Patient]":
            return self.patient_list