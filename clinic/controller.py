from .patient import Patient
from .note import Note
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
import hashlib

from .dao.patient_dao_json import PatientDAOJSON

class Controller:
    #Initializes the Controller class
    def __init__(self, autosave=True) -> None:
        self.autosave = autosave
        self.logged = False
        self.current_patient = None
        self.users = self.load_users()
        self.patient_dao = PatientDAOJSON()

    #loads users from a file or hardcodes them based on autosave
    def load_users(self):
        if self.autosave:
            try:
                with open("clinic/users.txt", "r") as file:
                    users = {}
                    for line in file:
                        username, hashed_password = line.strip().split(",")
                        users[username] = hashed_password
                    return users
            except FileNotFoundError:
                raise FileNotFoundError("The users.txt file is missing.")
        else:
            # Hardcoded users for in-memory tests
            return {
                "user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
                "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
                "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e",
            }

    # Hashes a password using SHA-256
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()     

    #logs in a user
    def login(self, user: str, password: str) -> bool:
        if self.logged:
            raise DuplicateLoginException("Already logged in.")
        hashed_password = self.hash_password(password)
        if user not in self.users or self.users[user] != hashed_password:
            raise InvalidLoginException("Invalid username or password.")
        self.logged = True
        return True
    
    #logs out a patient
    def logout(self) -> bool:
        if self.logged:
            self.logged = False
            return True
        raise InvalidLogoutException()

    #creates a new patient with all necessary info
    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> 'Patient':
        if self.logged:
            for patient in self.patient_dao.patient_list:
                if phn == patient.phn:
                    raise IllegalOperationException("Patient with the same PHN already exists.")
            return self.patient_dao.create_patient(phn, name, birth_date, phone, email, address)
        raise IllegalAccessException("Login required to create a patient.")

    #search for a patient by PHN
    def search_patient(self, phn: int) -> 'Patient':
        if self.logged:
            return self.patient_dao.search_patient(phn)
        else:
            raise IllegalAccessException("Login required to search for a patient.")
        return None

    #retrieves patients based on a name search and returns a list of all search matches
    def retrieve_patients(self, search_name: str) -> "list[Patient]":
        if self.logged:
            return self.patient_dao.retrieve_patients(search_name)
        raise IllegalAccessException("Login required to retrieve patients.")

    #used for updating patient details by providing the PHN of the patient we want to update
    def update_patient(self, phn_given: int, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> 'Patient':

        if not self.logged:
            raise IllegalAccessException("Login required to update a patient.")
       
        #not allowed to update the current patient
        if self.current_patient and self.current_patient.phn == phn:
            raise IllegalOperationException("Cannot update the current patient.")

        for patient in self.patient_dao.patient_list:
            if phn != phn_given and phn == patient.phn:
                raise IllegalOperationException("New PHN already in use.")

        # Checks to see if phn_given exists
        if phn_given not in [patient.phn for patient in self.patient_dao.patient_list]:
            raise IllegalOperationException("Patient with the given PHN not found.")

        #updating patient fields
        return self.patient_dao.update_patient(phn_given, phn, name, birth_date, phone, email, address)
            
        

    #deletes a patient based on PHN from the list of patients
    def delete_patient(self, phn: int) -> bool:

        if not self.logged:
            raise IllegalAccessException("Login required to delete a patient.")
        
        #not allowed to delete the current patient
        if self.current_patient and self.current_patient.phn == phn:
            raise IllegalOperationException("Cannot delete the current patient.")

        if phn not in [patient.phn for patient in self.patient_dao.patient_list]:
            raise IllegalOperationException("Patient with the given PHN not found.")

        return self.patient_dao.delete_patient(phn)
        

    #gives us a list of all patients
    def list_patients(self) -> "list[Patient]":
        if self.logged:
            return self.patient_dao.list_patients()
        raise IllegalAccessException("Login required to list patients.")

    #this functionn is used to set the current patient, by using this we can add notes to the set patient
    def set_current_patient(self, phn: int) -> Patient:
        
        if not self.logged:
            raise IllegalAccessException("Login required to set the current patient.")
        
        if self.logged:
            for patient in self.patient_dao.patient_list:
                if patient.phn == phn:
                    self.current_patient = patient
                    return patient
        raise IllegalOperationException("Patient with the given PHN not found.")
    
    #returns the current patient that is set
    def get_current_patient(self) -> Patient:
        if not self.logged:
            raise IllegalAccessException("Login required to get the current patient.")
        return self.current_patient
    
    #unsets the current patient by reassigning current_patient to None
    def unset_current_patient(self) -> None:
        if not self.logged:
            raise IllegalAccessException("Login required to unset the current patient.")
        self.current_patient = None
        

    #creates a note that is attached to the current patient
    def create_note(self, text: str):
        if not self.logged:
            raise IllegalAccessException("Login required to create a note.")
        
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        
        return self.current_patient.record.create_note(text)
    
    #allows us to search for a note in the record of the current patient by using the notes code
    def search_note(self, code: int):
        if not self.logged:
            raise IllegalAccessException("Login required to search for a note.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        return self.current_patient.record.search_note(code)
    
    #returns the notes associated to the current patient
    def retrieve_notes(self, text: str):
        if not self.logged:
            raise IllegalAccessException("Login required to retrieve notes.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        return self.current_patient.record.retrieve_notes(text)

    #allows us to update a note for the current patient based on the notes code and the new text we will be updating
    def update_note(self, code: int, text: str):
        if not self.logged:
            raise IllegalAccessException("Login required to update a note.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        return self.current_patient.record.update_note(code, text)
    
    #deletes a note based on code from the current patients record
    def delete_note(self, code: int):
        if not self.logged:
            raise IllegalAccessException("Login required to delete a note.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        return self.current_patient.record.delete_note(code)

    #lists all notes associated to the current patient
    def list_notes(self):
        if not self.logged:
            raise IllegalAccessException("Login required to list notes.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        return self.current_patient.record.list_notes()
