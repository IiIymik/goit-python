import pickle
import json
from abc import abstractmethod, ABC

class SerializationInterface(ABC):

    @abstractmethod
    def serialize_file(self):
        pass
            
        
class SaveToJson(SerializationInterface):

    def serialize_file(self):
        filename = "data.json"    
        with open(filename, "wb") as file: 
            json.dump(self, file)      


class SaveToBin(SerializationInterface):
    
    def serialize_file(self):
        filename = "data.pic"    
        with open(filename, "wb") as file: 
            pickle.dump(self, file)



class Meta(type):
    children_number = 0

    def __new__(*args, **kwargs):
        return type.__new__(*args)

    def __init__(*args, **kwargs):
        Meta.children_number += 1

 

class Cls1(metaclass=Meta):

    class_number = Meta.children_number

    def __init__(self, data):
        self.data = data

 
class Cls2(metaclass=Meta):

    class_number = Meta.children_number

    def __init__(self, data):
        self.data = data

 

assert (Cls1.class_number, Cls2.class_number) == (0, 1)
# print((Cls1.class_number, Cls2.class_number) == (0, 1))
a, b = Cls1(''), Cls2('')

assert (a.class_number, b.class_number) == (0, 1)
# print((a.class_number, b.class_number) == (0, 1))

