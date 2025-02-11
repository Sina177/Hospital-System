from .note import Note
from .dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
    #Initializes the PatientRecord class which records all of the notes for a patient
    def __init__(self, phn: int):
        self.note_dao = NoteDAOPickle(phn)

    #Adds a new note for a patient and returns the note
    def create_note(self, text: str):
        return self.note_dao.create_note(text)
    
    #Searches for a note by its code and returns it if found
    def search_note(self, code: int):
        return self.note_dao.search_note(code)

    #Searches for notes that contain a certain text and returns all notes that contain the text within a list
    def retrieve_notes(self, text: str):
        return self.note_dao.retrieve_notes(text)
    
    #Updates a note by searching for its code and changing its text. Returns true if this is done successfully and False if unsuccessful
    def update_note(self, code: int, text: str):
        return self.note_dao.update_note(code, text)
    
    # Deletes a note by its give code and returns True if code exists and False if code did not exist
    def delete_note(self, code: int): 
        return self.note_dao.delete_note(code)

    # Returns all notes for a patient
    def list_notes(self): 
        return self.note_dao.list_notes() # Goes through every note from the most recent to oldest and adds them to a list which is returned at the end of iteration