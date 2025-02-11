from datetime import datetime

class Note:
    # Initializes the notes class which contains the code to uniquely identify each note, the note text, and the timestamp
    def __init__(self, code: int, text: str):
        self.code = code
        self.text = text
        self.timestamp = datetime.now()

    # Checks to see if two notes are equal to one another while disregarding the timestamp
    def __eq__(self, other):
        return (
            self.code == other.code and
            self.text == other.text 
            # self.timestamp == other.timestamp doesnt want to compare time
        )

    # Defines the implementation of the str representation of notes (This is what is typically shown to users)
    def __str__(self):
        return f'The code is: {self.code}, and the text is: {self.text}'