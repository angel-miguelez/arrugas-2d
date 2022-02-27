from __future__ import annotations
from typing import List

class Subject:
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    __observers: List[Observer] = [] #List of observers

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        self.__observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """

        self.__observers.remove(observer)

    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        for observer in self.__observers:
            observer.update(self)

class Observer:
    """
    The Observer interface declares the update method, used by subjects.
    """

    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass
