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

    def test_1_login_correct_credentials(self):
        login_url = 'http://localhost/login.php'
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()
        
        # Tunggu redirect dan pastikan berada di halaman index.php
        WebDriverWait(self.browser, 10).until(EC.url_contains("index.php"))
        self.assertIn("index.php", self.browser.current_url)
    
    def test_2_index_page(self):
        try:
            expected_result = "Halo, "
            
            # Tunggu hingga elemen h2 muncul di halaman
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h2"))
            )
            actual_result = element.text
            self.assertIn(expected_result, actual_result)
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
