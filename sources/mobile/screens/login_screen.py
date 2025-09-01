
class LoginScreen:
    def __init__(self, driver):
        self.driver = driver

    def login(self, email, password):
        self.driver.find_element("accessibility id", "Email").send_keys(email)
        self.driver.find_element("accessibility id", "Password").send_keys(password)
        self.driver.find_element("accessibility id", "Sign in").click()