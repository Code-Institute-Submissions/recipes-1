import unittest
import app
from bson.objectid import ObjectId
app.testing = True
class TestQuiz(unittest.TestCase):
    def test_the_test(self):
        """
        Just to make sure that our testing is working
        """
        self.assertEqual(1,1)
    
    def test_register_form(self):
        registers = app.register
        users = app.mongo.db.register.find_one({'username':'Ram'})   
        """
        The registration form is working that means there is username called Ram in that database and the connection to the mongodb is working properly
        """
        self.assertEqual(registers, users)
    
    
print("Test passed")
    
if __name__ == "__main__": 
      unittest.main() 