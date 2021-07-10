from dataclasses import dataclass


@dataclass
class Feedback:
    feedback_text: str

    @staticmethod
    def fromTuple(tuple: tuple):
        # get rid of id
        return Feedback(*tuple[1:])
