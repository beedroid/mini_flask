from ..dao.test_dao import TestDao

class Controller():
    def getDataByID(id):
        testData = TestDao.get_test_by_id(id)
        return testData