from subject import Subject

class Observer():
    """
    The Observer interface declares the update method, used by subjects.
    """

    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass
