from abc import ABC, abstractmethod

class Notificacion(ABC):
    
    @abstractmethod
    def send(self , mensaje):
        pass  