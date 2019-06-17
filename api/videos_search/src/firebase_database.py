from firebase_admin import firestore

def method(method_func):
    def wrapper(database, id = None, *args, **kwargs):
        if id and not isinstance(id, str):
            id = str(id)
        
        return method_func(database, id, *args, **kwargs)
    
    return wrapper

class Database():
    def __init__(self, table_title):
        self.table_title = table_title
        self._db = firestore.client()
        self._ref = self._db.collection(table_title)
        self.get_object_by_id = lambda id: self._ref.document(id)

    @method
    def update(self, id, dict):
        obj = self.get_object_by_id(id)
        obj.update(dict)

    @method
    def insert(self, id, dict):
        obj = self.get_object_by_id(id)
        obj.set(dict)

    @method
    def delete(self, id):
        obj = self.get_object_by_id(id)
        obj.delete()

    @method
    def read(self, id = None):
        if not id:
            get_all_objects = lambda : [self.get_object_by_id(obj.id).get().to_dict() for obj in self._ref.get()]
            return  get_all_objects()
        else:
            return self._ref.document(id).get().to_dict()
