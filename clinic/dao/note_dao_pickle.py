from .note_dao import NoteDAO
from clinic.note import Note

from pickle import load, dump

class NoteDAOPickle(NoteDAO):
    def __init__(self, phn: int, autosave=True):
        self.autosave = autosave
        self.autocounter = 0
        self.phn = phn
        self.notes = []

        # If autosave is on the patient's notes are loaded into the notes list, if auto save is off or file is not found notes remains empty
        if self.autosave:
            try:
                with open(f"./clinic/records/{self.phn}.dat", 'rb') as file:
                    self.notes = load(file)
                if self.notes:
                    self.autocounter = self.notes[-1].code
            except (FileNotFoundError):
                self.notes = []

    # Helper method which writes notes list into the .dat file
    def write_to_file(self):
        if self.autosave:
            with open(f"./clinic/records/{self.phn}.dat", 'wb') as file:
                dump(self.notes, file)

    # Creates a new note and returns the note
    def create_note(self, text: str):
        self.autocounter += 1  # Auto-incremented code for each new note
        note = Note(self.autocounter, text)
        self.notes.append(note)
        self.write_to_file()
        return note

    # Searches for a note by it's code and if the note is found returns it, if note code doesn't exist returns None
    def search_note(self, code: int):
        for note in self.notes:
            if note.code == code:
                return note
        return None

    # Retrieves a note by it's text and returns the note if it is found, if the note is not found an empty list is returned
    def retrieve_notes(self, text: str):
        result = []
        for note in self.notes:
            if text in note.text:
                result.append(note)
        return result

    # Updates a note given it's code and the new text; returns True if successfully updated and False if the note was not found
    def update_note(self, code: int, text: str):
        if code in [note.code for note in self.notes]: # Checks to see if the code exists in the current notes
            for note in self.notes: # searches through the notes to find the note with the matching code
                if code == note.code:
                    note.text = text
                    self.write_to_file()
                    return True
        return False

    # Deletes a note by it's code, returns True if the note was successfully deleted, and returns None if the note was not found
    def delete_note(self, code: int): 
        for note in self.notes: # Looking through all notes to see if code exists
            if note.code == code:
                self.notes.remove(note)
                self.write_to_file()
                return True
        return None

    def list_notes(self): # Returns a list which contains every note in the notes array
        return [note for note in self.notes[::-1]]