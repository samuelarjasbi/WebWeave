class JSInjector:
    def __init__(self, selenium_session):
        """
        Initializes the JavaScript injector.

        :param selenium_session: An instance of SeleniumSession.
        """
        self.driver = selenium_session.driver  # Reuse the same driver

    def execute_script(self, script, *args):
        """
        Executes JavaScript in the browser and returns the result.

        :param script: The JavaScript code as a string.
        :param args: Any additional arguments to pass to the JS script.
        :return: The result of the script execution.
        """
        return self.driver.execute_script(script, *args)

    def execute_async_script(self, script, *args):
        """
        Executes an asynchronous JavaScript script and returns the result.

        :param script: The JavaScript code as a string.
        :param args: Any additional arguments to pass to the JS script.
        :return: The result of the async script execution.
        """
        self.driver.set_script_timeout(600)
        return self.driver.execute_async_script(script, *args)
