from Observer import Observer

class Subject():
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass
