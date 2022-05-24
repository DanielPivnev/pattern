from abc import ABC, abstractmethod


class ViewObserver(ABC):

    @abstractmethod
    def update(self, state, u_id):
        pass
