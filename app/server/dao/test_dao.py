from app import db
from app.server.models import TestModel


class TestDao:
    @staticmethod
    def get_test_by_id(id=None):
        if not id:
            return None
        query = db.session.query(TestModel).filter(TestModel.id == id)
        if not query:
            return None
        return query.first()
