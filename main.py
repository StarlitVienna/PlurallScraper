import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


#ID --> #
#Class --> .

def login(DRIVER):
    try:
        enable_cookies_button = DRIVER.find_element(By.CSS_SELECTOR, 'button[class="css-14echvp exvnh5m0"]')
        enable_cookies_button.click()
    except Exception as E:
        print(E)

    #Get the email input field
    #email_input_field = DRIVER.find_element(By.CSS_SELECTOR, 'input[class="css-11qryxn"]')
    email_input_field = DRIVER.find_element(By.CSS_SELECTOR, 'input.css-13hzf48[type="text"][placeholder="Nome de usuário, e-mail ou celular"]')
    email_input_field.send_keys("")

    #Get the password input field
    password_input_field = DRIVER.find_element(By.CSS_SELECTOR, 'input.css-11qryxn[type="password"][placeholder="Digite sua senha"]')
    password_input_field.send_keys("")

    
    #Get the submit button
    login_button = DRIVER.find_element(By.CSS_SELECTOR, 'button[class="css-3x3axm exvnh5m0"]')
    login_button.click()

    try:
        fechar_informe_email_popup = DRIVER.find_element(By.CSS_SELECTOR, 'button[class="css-1h90763 exvnh5m0"]')
        fechar_informe_email_popup.click()
    except Exception as E:
        print(E)


    #Dump the cookies
    #pickle.dump(DRIVER.get_cookies(), open("./plurallCookies.pkl", "wb"))



def abrir_maestro(DRIVER):
    DRIVER.get("https://maestro.plurall.net/?utm_source=home&utm_medium=card-activities&utm_campaign=default")
    
    #Abrir aba disciplinas
    disciplinas = DRIVER.find_element(By.CSS_SELECTOR, '.tab-subjects')
    disciplinas.click()


def filtrar_todas(DRIVER):
    filtro_button = DRIVER.find_element(By.CSS_SELECTOR, '.activity-status')
    filtro_button.click()

    opcao_todas = DRIVER.find_element(By.CSS_SELECTOR, '#select_option_4')
    opcao_todas.click()


def criar_pastas_materias(DRIVER):
    subject_list = DRIVER.find_element(By.CSS_SELECTOR, "div.adp-list-container")
    subjects = subject_list.find_elements(By.CSS_SELECTOR, 'span[class="adp-subject-name adp-text ng-binding ng-scope"]')
    for subject in subjects:
        print(subject.text)
    pass

def abrir_geografia(DRIVER):
    geo_button = DRIVER.find_element(By.CSS_SELECTOR, 'div.adp-list-item:nth-child(2)')
    geo_button.click()    

    #DRIVER.execute_script("document.body.style.transform = 'scale(0.08)'")
    #DRIVER.execute_script('document.body.style.MozTransform = "scale(0.50)";')
    #DRIVER.execute_script("document.body.style.zoom='150%'")

    #nome = DRIVER.find_element(By.CSS_SELECTOR, 'input[id="input_141"]')
    #nome.send_keys(Keys.PAGE_DOWN);


    #Open every item and go back
    items = DRIVER.find_elements(By.CSS_SELECTOR, 'div[class="list-title layout-column flex-auto"]')
    #titulos = items.find_elements(By.CSS_SELECTOR, 'div[class="ng-binding"]')
    titulos = []
    for item in range(len(items)):
        #items[item].text
        titulos.append(items[item].find_element(By.CSS_SELECTOR, 'div[class="ng-binding"]'))

    for titulo in range(len(titulos)):
        print(titulos[titulo].text)

    filtrar_todas(DRIVER)



def main_func():
    URL = "https://login.plurall.net/"
    FP = webdriver.FirefoxProfile("./plurallScraper/profiles")
    FP.set_preference("layout.css.devPixelsPerPx", "0.3")

    ffOptions = Options()
    ffOptions.add_argument("-profile")
    ffOptions.add_argument(r'C:\Users\Tyler\AppData\Roaming\Mozilla\Firefox\Profiles\0753x1pz.default')

    DRIVER = webdriver.Firefox(firefox_profile=FP)
    #DRIVER.
    DRIVER.get(URL)
    
    DRIVER.implicitly_wait(10)

    login(DRIVER)
    abrir_maestro(DRIVER)
    criar_pastas_materias(DRIVER)

    #abrir_geografia(DRIVER)
    


if __name__ == "__main__":
    main_func()