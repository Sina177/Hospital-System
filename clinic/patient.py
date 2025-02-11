from .patient_record import PatientRecord

#the patient class is used to manage all info regarding each individual patient
class Patient:
    def __init__(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str):
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.record = PatientRecord(self.phn)

    #this function is used to check if all fields in a patient match with the other patient to check if they are the same
    def __eq__(self, other):
        return (
            self.phn == other.phn and
            self.name == other.name and
            self.birth_date == other.birth_date and
            self.phone == other.phone and
            self.email == other.email and
            self.address == other.address
        )
    
    # Defines the str method for the patient class (Typically shown to users)
    def __str__(self):
        return f'phn is: {self.phn}, name is: {self.name}, date of birth is: {self.birth_date}, phone number is: {self.phone}, email is: {self.email}, address is: {self.address}'