
import unittest


if __name__ =="__main__":
    runner=unittest.TextTestRunner(verbosity=2)
    suite= unittest.TestSuite()
    
    runner.run(suite())
    unittest.main()