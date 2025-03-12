import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginCorrectCredentialsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=option)

    def test_1_login_correct_credentials(self):
        login_url = 'http://localhost/login.php'
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()
        
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
