class TestCase:
    def __init__(self, name):
        self.name = name
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def run(self):
        self.setUp()
        method = getattr(self, self.name)
        method()
        self.tearDown()

class WasRun(TestCase):
    def __init__(self, name):
        super().__init__(name)
    def testMethod(self):
        self.wasRun = 1
        self.log += "testMethod "
    def setUp(self):
        self.wasRun = None
        self.log = "setUp "
    def tearDown(self):
        self.log += "tearDown "

class TestCaseTest(TestCase):
    def setUp(self):
        self.test = WasRun("testMethod")
    def testRunning(self):
        self.test.run()
        assert(self.test.wasRun)
    def testSetUp(self):
        self.test.run()
        assert("setUp testMethod tearDown " == self.test.log)
    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run()
        assert("setUp testMethod tearDown " == test.log)

TestCaseTest("testRunning").run()
TestCaseTest("testSetUp").run()
TestCaseTest("testTemplateMethod").run()