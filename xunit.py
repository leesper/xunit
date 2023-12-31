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
    def run(self, result):
        result.testStarted()
        try:
            self.setUp()
            method = getattr(self, self.name)
            method()
        except:
            result.testFailed()
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
    def testBrokenMethod(self):
        raise Exception

class TestSuite:
    def __init__(self):
        self.tests = []
    def add(self, test):
        self.tests.append(test)
    def run(self, result):
        for test in self.tests:
            test.run(result)

class TestCaseTest(TestCase):
    def setUp(self):
        self.result = TestResult()
    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert("setUp testMethod tearDown " == test.log)
    def testResult(self):
        test = WasRun("testMethod")
        result = test.run(self.result)
        assert("1 run, 0 failed" == result.summary())
    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        result = test.run(self.result)
        assert ("1 run, 1 failed" == result.summary())
    def testFailedResultFormatting(self):
        self.result.testStarted()
        self.result.testFailed()
        assert("1 run, 1 failed" == result.summary())
    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(self.result)
        assert("2 run, 1 failed" == result.summary())

class SetUpExceptionTest(TestCase):
    def setUp(self):
        raise Exception
    def testFailedSetUp(self):
        test = WasRun("testMethod")
        result = test.run()
        assert("1 run, 1 failed" == result.summary())

suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResultFormatting"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testSuite"))
suite.add(TestCaseTest("testRunning"))
suite.add(TestCaseTest("testSetUp"))
suite.add(SetUpExceptionTest("testFailedSetUp"))
result = TestResult()
suite.run(result)
print(result.summary())