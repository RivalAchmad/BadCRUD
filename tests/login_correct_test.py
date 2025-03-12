import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginCorrectCredentialsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')  
        cls.browser = webdriver.Firefox(options=option)
        cls.browser.implicitly_wait(10) 

    def test_1_login_correct_credentials(self):
        login_url = 'http://localhost/login.php'
        self.browser.get(login_url)

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'inputUsername')))

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()

        WebDriverWait(self.browser, 10).until(EC.url_contains('index.php'))

    def test_2_index_page(self):
        expected_text = "Halo, "

        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/h2"))
        )
        actual_text = element.text

        self.assertIn(expected_text, actual_text)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
