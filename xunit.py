class TestResult:
    def __init__(self):
        self.runCount = 0
        self.failureCount = 0
    def testStarted(self):
        self.runCount += 1
    def testFailed(self):
        self.failureCount += 1
    def summary(self):
        return f'{self.runCount} run, {self.failureCount} failed'

class TestCase:
    def __init__(self, name):
        self.name = name
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def run(self):
        result = TestResult()
        result.testStarted()
        try:
            self.setUp()
            method = getattr(self, self.name)
            method()
        except:
            result.testFailed()
        self.tearDown()
        return result

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
    def testBrokenMethod(self):
        raise Exception

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
    def testResult(self):
        test = WasRun("testMethod")
        result = test.run()
        assert("1 run, 0 failed" == result.summary())
    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        result = test.run()
        assert ("1 run, 1 failed" == result.summary())
    def testFailedResultFormatting(self):
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert("1 run, 1 failed" == result.summary())

TestCaseTest("testRunning").run()
TestCaseTest("testSetUp").run()
TestCaseTest("testTemplateMethod").run()
TestCaseTest("testResult").run()
TestCaseTest("testFailedResult").run()
TestCaseTest("testFailedResultFormatting").run()

class SetUpExceptionTest(TestCase):
    def setUp(self):
        raise Exception
    def testFailedSetUp(self):
        test = WasRun("testMethod")
        result = test.run()
        assert("1 run, 1 failed" == result.summary())

SetUpExceptionTest("testFailedSetUp").run()