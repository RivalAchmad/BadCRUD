import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestContactManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')  # Gunakan headless untuk CI/CD
        cls.browser = webdriver.Firefox(options=option)
        cls.url = os.environ.get('URL', 'http://docker-apache')  # Gunakan hostname container, bukan localhost

    def login(self):
        self.browser.get(f"{self.url}/login.php")
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "inputUsername"))).send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_1_add_new_contact(self):
        self.login()
        self.browser.get(f"{self.url}/create.php")
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "name"))).send_keys("John Doe")
        self.browser.find_element(By.ID, 'email').send_keys("john.doe@example.com")
        self.browser.find_element(By.ID, 'phone').send_keys("123456789")
        self.browser.find_element(By.ID, 'title').send_keys("Developer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_2_delete_contact(self):
        self.login()
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")))
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
        delete_button.click()
        WebDriverWait(self.browser, 5).until(EC.alert_is_present()).accept()
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_3_change_profile_picture(self):
        self.login()
        self.browser.get(f"{self.url}/profil.php")
        file_path = os.path.join(os.getcwd(), 'tests', 'image_test.jpg')
        self.browser.find_element(By.ID, 'formFile').send_keys(file_path)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertEqual(self.browser.current_url, f"{self.url}/profil.php")

    def test_4_update_contact(self):
        self.login()
        actions_section = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]"))
        )
        update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
        update_button.click()
        self.browser.find_element(By.ID, 'name').clear()
        self.browser.find_element(By.ID, 'name').send_keys("Jane Doe")
        self.browser.find_element(By.ID, 'email').clear()
        self.browser.find_element(By.ID, 'email').send_keys("jane.doe@example.com")
        self.browser.find_element(By.ID, 'phone').clear()
        self.browser.find_element(By.ID, 'phone').send_keys("987654321")
        self.browser.find_element(By.ID, 'title').clear()
        self.browser.find_element(By.ID, 'title').send_keys("Designer")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_5_test_xss_security(self):
        self.login()
        self.browser.get(f"{self.url}/xss.php")
        self.browser.find_element(By.NAME, 'thing').send_keys("<script>alert(1)</script>")
        self.browser.find_element(By.NAME, 'submit').click()

        try:
            WebDriverWait(self.browser, 5).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            alert.accept()
            self.fail("XSS vulnerability detected!")
        except NoAlertPresentException:
            pass  # XSS tidak terjadi, berarti aman

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
