from db import get_db

class UserSelections:
    
    # def __init__(self, **kwargs):
    #     self.id = kwargs.get('id')
    #     self.ModuleItemID = kwargs.get('ModuleItemID')

    @staticmethod
    def create(id, ModuleItemID):
        db = get_db()
        db.execute(
            "INSERT INTO UserSelections (id, ModuleItemID) VALUES (?, ?)",
            (id, ModuleItemID,)
        )
        db.commit()

    @staticmethod
    def delete(id):
        db = get_db()
        db.execute("DELETE FROM UserSelections WHERE id = ?", (id,))
        db.commit()
    
    @staticmethod
    def getAll(id):
        db = get_db()
        return db.execute(
            "SELECT ModuleItemID FROM UserSelections WHERE id = ?", (id,)
        ).fetchall()
    