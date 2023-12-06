import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


#ID --> #
#Class --> .

class PlurallScraper():
    def __init__(self, email: str, password:str):
        self.DRIVER = None
        self.email = email
        self.password = password
        self.URL = "https://login.plurall.net/"


    def setup(self):
        #FP = webdriver.FirefoxProfile("./plurallScraper/profiles")
        #FP.set_preference("layout.css.devPixelsPerPx", "0.3")

        
        #ffOptions = Options()
        #ffOptions.add_argument("-profile")
        #ffOptions.add_argument(r'C:\Users\Tyler\AppData\Roaming\Mozilla\Firefox\Profiles\0753x1pz.default')
        

        #DRIVER = webdriver.Firefox(firefox_profile=FP)
        self.DRIVER = webdriver.Firefox()
        #DRIVER.
        self.DRIVER.get(self.URL)
        
        self.DRIVER.implicitly_wait(10)
        


    def login(self):
        try:
            enable_cookies_button = self.DRIVER.find_element(By.CSS_SELECTOR, 'button[class="css-14echvp exvnh5m0"]')
            enable_cookies_button.click()
        except Exception as E:
            print(E)

        #Get the email input field
        #email_input_field = DRIVER.find_element(By.CSS_SELECTOR, 'input[class="css-11qryxn"]')
        email_input_field = self.DRIVER.find_element(By.CSS_SELECTOR, 'input.css-13hzf48[type="text"][placeholder="Nome de usuário, e-mail ou celular"]')
        email_input_field.send_keys(self.email)
        value = self.DRIVER.execute_script("return getComputedStyle(arguments[0], null).getPropertyValue('CSS SELECTOR');", email_input_field)
        print(f"AAAAAAAAA --> {value}")

        #Get the password input field
        password_input_field = self.DRIVER.find_element(By.CSS_SELECTOR, 'input.css-11qryxn[type="password"][placeholder="Digite sua senha"]')
        password_input_field.send_keys(self.password)

        
        #Get the submit button
        login_button = self.DRIVER.find_element(By.CSS_SELECTOR, 'button[class="css-3x3axm exvnh5m0"]')
        login_button.click()

        try:
            fechar_informe_email_popup = self.DRIVER.find_element(By.CSS_SELECTOR, 'button[class="css-1h90763 exvnh5m0"]')
            fechar_informe_email_popup.click()
        except Exception as E:
            print(E)


        #Dump the cookies
        #pickle.dump(DRIVER.get_cookies(), open("./plurallCookies.pkl", "wb"))


    def abrir_maestro(self):
        self.DRIVER.get("https://maestro.plurall.net/?utm_source=home&utm_medium=card-activities&utm_campaign=default")
        
        #Abrir aba disciplinas
        disciplinas = self.DRIVER.find_element(By.CSS_SELECTOR, '.tab-subjects')
        disciplinas.click()


    def criar_pastas_materias(self):
        document = self.DRIVER.find_element(By.CSS_SELECTOR, "html")
        subjects_list = self.DRIVER.find_element(By.CSS_SELECTOR, "div.adp-list-container")
        
        #Make subjects list for appending stuff later
        subjects = []
        subjects_elements = []

        #subjects = subject_list.find_elements(By.CSS_SELECTOR, 'span[class="adp-subject-name adp-text ng-binding ng-scope"]')
        #DRIVER.execute_script("window.scrollTo(0, 5000);");
        for i in range(3):
            scroll_items = subjects_list.find_elements(By.CSS_SELECTOR, 'span[class="adp-subject-name adp-text ng-binding ng-scope"]')
            for scroll_item in scroll_items:
                #print(scroll_item.text)
                if (scroll_item.text not in subjects):
                    subjects.append(scroll_item.text)

                #if (scroll_item not in subjects_elements):
                    #subjects_elements.append(scroll_item)

                #print(scroll_item.value_of_css_property("class"))
                
                #subjects_elements.append(self.DRIVER.execute_script("return getComputedStyle(arguments[0], null).getPropertyValue('selector');", scroll_item))
                            
                    
            document.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            # Try tweaking the sleep number if things don't go as planned

        # Remove empty strings from end result
        subjects = [s for s in subjects if s != '']
        #print(subjects)
        print(subjects_elements)

        
        #Prompt the user to check if all the folders got registered

        if not os.path.exists("./plurallSubjects"):
            os.mkdir("./plurallSubjects")

        for subject in subjects:
            if not os.path.exists(f"./plurallSubjects/{subject}"):
                os.mkdir(f"./plurallSubjects/{subject}")

        # Go back up
        document.send_keys(Keys.PAGE_UP)
        document.send_keys(Keys.PAGE_UP)
        document.send_keys(Keys.PAGE_UP)
        document.send_keys(Keys.PAGE_UP)
        document.send_keys(Keys.PAGE_UP)


    def abrir_cada_materia(self):
        #materias
        pass




    def filtrar_todas(self):
        filtro_button = self.DRIVER.find_element(By.CSS_SELECTOR, '.activity-status')
        filtro_button.click()

        opcao_todas = self.DRIVER.find_element(By.CSS_SELECTOR, '#select_option_4')
        opcao_todas.click()



    def abrir_geografia(self):
        geo_button = self.DRIVER.find_element(By.CSS_SELECTOR, 'div.adp-list-item:nth-child(2)')
        geo_button.click()    

        #DRIVER.execute_script("document.body.style.transform = 'scale(0.08)'")
        #DRIVER.execute_script('document.body.style.MozTransform = "scale(0.50)";')
        #DRIVER.execute_script("document.body.style.zoom='150%'")

        #nome = DRIVER.find_element(By.CSS_SELECTOR, 'input[id="input_141"]')
        #nome.send_keys(Keys.PAGE_DOWN);


        #Open every item and go back
        items = self.DRIVER.find_elements(By.CSS_SELECTOR, 'div[class="list-title layout-column flex-auto"]')
        #titulos = items.find_elements(By.CSS_SELECTOR, 'div[class="ng-binding"]')
        titulos = []
        for item in range(len(items)):
            #items[item].text
            titulos.append(items[item].find_element(By.CSS_SELECTOR, 'div[class="ng-binding"]'))

        for titulo in range(len(titulos)):
            print(titulos[titulo].text)

        filtrar_todas()



    def close(self):
        self.DRIVER.close()



if __name__ == "__main__":
    pass