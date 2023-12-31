import re
import os
import time
import shutil
import pickle
import pathlib
import requests
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions

#ID --> #
#Class --> .

class PlurallScraper():
    def __init__(self, email: str, password:str):
        self.DRIVER = None
        self.email = email
        self.password = password
        self.URL = "https://login.plurall.net/"

        self.subjects_names = []
        self.subjects_num = 0
        self.subjects_css_selector = []

        self.contents_css_selectors = []

        self.subjects_dict = {}

        self.current_page_content_names = []

        self.file_path = os.path.realpath(__file__)
        self.folder_path = pathlib.Path(__file__).parent.resolve()




    def setup(self):
        #FP = webdriver.FirefoxProfile("./plurallScraper/profiles")
        #FP.set_preference("layout.css.devPixelsPerPx", "0.3")

        
        #ffOptions = Options()
        #ffOptions.add_argument("-profile")
        #ffOptions.add_argument(r'C:\Users\Tyler\AppData\Roaming\Mozilla\Firefox\Profiles\0753x1pz.default')
        

        #DRIVER = webdriver.Firefox(firefox_profile=FP)

        # Make downloads folder for additional files
        if not os.path.exists("./downloads"):
            os.mkdir("./downloads")

        options = FirefoxOptions()
        options.log.level = "trace"

        # Make sure firefox won't open the pdf's in preview mode
        #options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", "C:\\Users\\stardust\\Downloads\\PlurallScraper-dev-branch\\second\\downloads")
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("pdfjs.disabled", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        #options.add_argument("--window-size=1920x1080")
        #options.add_argument("-devtools")
        self.DRIVER = webdriver.Firefox(options=options)

        #DRIVER.
        self.DRIVER.get(self.URL)
        
        self.DRIVER.implicitly_wait(10)

            

    def zoom_out(self, times):
        # A WORKING WAY TO ZOOM OUT WITH SELENIUM :D
        self.DRIVER.set_context("chrome")
        win = self.DRIVER.find_element(By.CSS_SELECTOR, "html")
        for i in range(times):
            win.send_keys(Keys.CONTROL + "-")
        self.DRIVER.set_context("content")
    
    def zoom_in(self, times):
        # A WORKING WAY TO ZOOM OUT WITH SELENIUM :D
        self.DRIVER.set_context("chrome")
        win = self.DRIVER.find_element(By.CSS_SELECTOR, "html")
        for i in range(times):
            win.send_keys(Keys.CONTROL + "+")
        self.DRIVER.set_context("content")

    def zoom_default(self):
        self.DRIVER.set_context("chrome")
        win = self.DRIVER.find_element(By.CSS_SELECTOR, "html")
        win.send_keys(Keys.CONTROL + "0")
        self.DRIVER.set_context("content")

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
        self.DRIVER.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.F12)
        actions = ActionChains(self.DRIVER)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys("k").key_up(Keys.CONTROL).key_up(Keys.SHIFT).perform()
        time.sleep(5)


    def abrir_maestro(self):
        self.DRIVER.get("https://maestro.plurall.net/?utm_source=home&utm_medium=card-activities&utm_campaign=default")
        
        #Abrir aba disciplinas
        disciplinas = self.DRIVER.find_element(By.CSS_SELECTOR, '.tab-subjects')
        disciplinas.click()



    def name_sanitizer(self, name):
        # Django slugify function
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
        name = re.sub(r'[^\w\s-]', '', name.lower())
        return re.sub(r'[-\s]+', '-', name).strip('-_')

    def criar_pastas_materias(self, cut_subjects):
        html_element = self.DRIVER.find_element(By.CSS_SELECTOR, "html")
        subjects_list = self.DRIVER.find_element(By.CSS_SELECTOR, "div.adp-list-container")
        
        #Make subjects list for appending stuff later
        subjects = []
        subjects_elements = []

        #subjects = subject_list.find_elements(By.CSS_SELECTOR, 'span[class="adp-subject-name adp-text ng-binding ng-scope"]')
        #DRIVER.execute_script("window.scrollTo(0, 5000);");



        ##############################################################################################################################
        #Get all subjects name
        for i in range(3):
            #Saving the names of each subject so the folders can be created
            scroll_items = subjects_list.find_elements(By.CSS_SELECTOR, 'span[class="adp-subject-name adp-text ng-binding ng-scope"]')
            for scroll_item in scroll_items:
                if (scroll_item.text not in subjects):
                    subjects.append(scroll_item.text)


            """
            #Saving the subjects elements for later use :)
            scroll_elements = subjects_list.find_elements(By.CSS_SELECTOR, "div.adp-list-item")
            for scroll_element in scroll_elements:
                if scroll_element not in subjects_elements:
                    subjects_elements.append(scroll_element)
            """

                            
            #SCROLL DOWN        
            html_element.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            # Try tweaking the sleep number if things don't go as planned

        # Remove empty strings from end result
        subjects = [s for s in subjects if s != '']

        if cut_subjects > 0:
            #For some reason it does not work properly without the -1
            for i in range(cut_subjects-1):
                del(subjects[0])

        #SANITIZE subjects name
        #subjects = [s for self.name_normalizer(s) in subjects]
        for i in range(len(subjects)):
            subjects[i] = self.name_sanitizer(subjects[i])


        #Save those names and elements to an object of the class for later use
        self.subjects_names = subjects;
        self.subjects_num = len(subjects)
        for subject_i in range(len(subjects)):
            #self.subjects_dict[str(subjects[subject_i])] = subjects_elements
            if cut_subjects > 0:
                self.subjects_css_selector.append(f"div.adp-list-item:nth-child({cut_subjects+subject_i+2})")
            else:
                self.subjects_css_selector.append(f"div.adp-list-item:nth-child({subject_i+2})")
        
        ##############################################################################################################################


        #Some testing to make sure there is a proper number of elements
        #print(f"Expected number of subjects -->  {len(subjects)}")
        #print(f"Actual number of subject elements --> {len(subjects_elements)}")

        #print(subjects)
        #print(subjects_elements)

        
        #Prompt the user to check if all the folders got registered

        if not os.path.exists("./plurallSubjects"):
            os.mkdir("./plurallSubjects")

        for subject in subjects:
            if not os.path.exists(f"./plurallSubjects/{subject}"):
                os.mkdir(f"./plurallSubjects/{subject}")

        # Go back up
        html_element.send_keys(Keys.PAGE_UP)
        html_element.send_keys(Keys.PAGE_UP)
        html_element.send_keys(Keys.PAGE_UP)
        html_element.send_keys(Keys.PAGE_UP)
        html_element.send_keys(Keys.PAGE_UP)

    

    def scroll_e_carregar(self, html_element, detect_load_button: bool):
        html_element.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        
        if detect_load_button:
            # Try to find and press load more button
            try:
                load_more_button = self.DRIVER.find_element(By.CSS_SELECTOR, "div.layout-align-end-center:nth-child(1) > button:nth-child(1)")
                load_more_button.click()
                # In case it works, wait a bit
                time.sleep(1)
            except Exception as E:
                print(E)
                print("No load button")

    def download_mp4(self, URL: str, videoname: str, path):
        FILE_TO_SAVE_AS = f"{path}\\{videoname}.mp4" # the name you want to save file as

        resp = requests.get(URL) # making requests to server

        with open(FILE_TO_SAVE_AS, "wb") as f: # opening a file handler to create new file 
            f.write(resp.content)

    def esperar_download(self):
        seconds = 0
        timeout = 20
        dl_wait = True
        while dl_wait and seconds < timeout:
            time.sleep(1)
            dl_wait = False
            for fname in os.listdir("./downloads/"):
                if fname.endswith('.crdownload') or fname.endswith('.part'):
                    dl_wait = True
            seconds += 1
        return seconds

    def criar_pastas_conteudos_materias(self, max_number_of_pages):

        self.current_page_content_names = []

        #print(self.subjects_elements)
        #for i in self.subjects_dict:
            #print(i)
        #self.subjects_dict[self.subjects_names[0]].click()
        #time.sleep(10)


        for i in range(self.subjects_num):

            #Find content name
            #self.subjects_elements[0].click()
            #subject.click()

            self.current_page_content_names = []
            current_subject = self.DRIVER.find_element(By.CSS_SELECTOR, self.subjects_css_selector[i])
            # It does not need to scroll to be able to click it but to get the name it does need to scroll thus the need to actually get the names from a list
            #current_subject_name = self.name_sanitizer(current_subject.find_element(By.CSS_SELECTOR, 'span[class="adp-subject-name adp-text ng-binding ng-scope"]').text)
            current_subject_name = self.subjects_names[i]
            current_subject.click()



            #When saving a subject detect if there's an arrow button, if there is then it's an exercise list so the program will need to either delete that folder or save the list somehow

            contents_num = 0

            content_names = []
            html_element = self.DRIVER.find_element(By.CSS_SELECTOR, 'html')
            for i in range(max_number_of_pages):
                contents_titles_divs = self.DRIVER.find_elements(By.CSS_SELECTOR, 'div[class="list-title layout-column flex-auto"]')
                for content_title in contents_titles_divs:
                    content_name = content_title.find_element(By.CSS_SELECTOR, 'div[class="ng-binding"]').text
                    
                    # Normalize content name
                    content_name = self.name_sanitizer(content_name)
                    if content_name not in self.current_page_content_names:
                        self.current_page_content_names.append(content_name)
                
                self.scroll_e_carregar(html_element=html_element, detect_load_button=True)
            
            # Remove any empty strings
            self.current_page_content_names = [name for name in self.current_page_content_names if name != '']
            contents_num = len(self.current_page_content_names)

            for content_name in self.current_page_content_names:
                #if not os.path.exists("./plurallSubjects/{current_subject}")
                if not os.path.exists(f"./plurallSubjects/{current_subject_name}/{content_name}"):
                    os.mkdir(f"./plurallSubjects/{current_subject_name}/{content_name}")

            # Before going back, go into each of the contents
            contents_css_selector = []
            for i in range(contents_num):
                contents_css_selector.append(f'.adp-list-container > div:nth-child({i+3})')

            for content_i in range(contents_num):
                current_content_selector = contents_css_selector[content_i]
                current_content_name = self.current_page_content_names[content_i]

                content_button = self.DRIVER.find_element(By.CSS_SELECTOR, current_content_selector)
                content_button.click()
                
                
                # Make folders for each subcontent

                sub_contents_names = []

                for page in range(max_number_of_pages):
                    html_element = self.DRIVER.find_element(By.CSS_SELECTOR, 'html')

                    sub_contents = self.DRIVER.find_elements(By.CSS_SELECTOR, 'div.cm-box-activity-student')
                    for s_c in sub_contents:
                        sub_contents_name = s_c.find_element(By.CSS_SELECTOR, 'div[class="cm-activity-title ng-binding"]').text
                        if self.name_sanitizer(sub_contents_name) not in sub_contents_names:
                            sub_contents_names.append(self.name_sanitizer(sub_contents_name))

                    self.scroll_e_carregar(html_element=html_element, detect_load_button=False) 
                    

                #Remove sub-contents_names empty strings
                sub_contents_names = [s_c for s_c in sub_contents_names if s_c != '']
                sub_contents_num = len(sub_contents_names)
                
                #SANITIZE the names
                for s_c_i in range(sub_contents_num):
                    sub_contents_names[s_c_i] = self.name_sanitizer(sub_contents_names[s_c_i])


                for s_c in sub_contents_names:
                    if not os.path.exists(f"./plurallSubjects/{current_subject_name}/{current_content_name}/{s_c}"):
                        os.mkdir(f"./plurallSubjects/{current_subject_name}/{current_content_name}/{s_c}")


                # Make folders for each subcontent

                # Open each sub-content

                sub_contents_selector = []
                for i in range(sub_contents_num):
                    sub_contents_selector.append(f'div.cm-box-activity-student:nth-child({i+2})')

                
                for i in range(sub_contents_num):
                    self.DRIVER.find_element(By.CSS_SELECTOR, sub_contents_selector[i]).click()
                    current_subcontent_name = sub_contents_names[i]
                    time.sleep(2)
                    self.DRIVER.refresh()
                    time.sleep(5)
                    print(f"clicked on --> {current_subcontent_name}")
                    
                    """
                    self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + '-')
                    self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + '-')
                    self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + '-')
                    self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + '-')
                    self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + '-')
                    """

                    
                    #self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + Keys.SHIFT + 'k')
                    #console = self.DRIVER.find_element(By.ID, "tabbrowser-tabs")
                    #console.send_keys(":screenshot --dpr 3 --fullpage")

                    #self.DRIVER.execute_script(':screenshot --dpr 3 --fullpage')

                    #self.DRIVER.set_window_size(15360, 8640)
                    print(f"Going to take screenshot")
                    if not os.path.exists(f"./plurallSubjects/{current_subject_name}/{current_content_name}/{current_subcontent_name}/{self.name_sanitizer(current_content_name)}.png"):
                        self.zoom_out(4)
                        time.sleep(1)
                        self.DRIVER.save_full_page_screenshot(f"./plurallSubjects/{current_subject_name}/{current_content_name}/{current_subcontent_name}/{self.name_sanitizer(current_content_name)}.png")
                        print(f"TOOK SCREENSHOT OF {self.name_sanitizer(current_subcontent_name)}")
                        #self.DRIVER.save_screenshot()
                        self.zoom_default()
                        time.sleep(1)
                        #self.DRIVER.execute("FULL_PAGE_SCREENSHOT")
                        #self.DRIVER.exe
                        #driver.find_element("body").send_keys(Keys.F12)
                    else:
                        print("DID NOT TAKE SCREENSHOT")

                    self.zoom_default()




                    #FOR THIS PART TO WORK, YOU NEED TO EITHER HAVE A REALLY BIG RESOLUTION THAT CAN VIEW ALL THE FILES OR CHANGE THE FRICKING CODE
                    # REMEMBER TO MAKE IT A TRY
                    # Get any downloadable files from page
                    subcontent_files = []
                    try:
                        #Switch to the iframe
                        self.DRIVER.switch_to.frame(self.DRIVER.find_element(By.CSS_SELECTOR, '#activityTemplate'))
                        #subcontent_files = self.DRIVER.find_elements(By.CSS_SELECTOR, 'div[class="content-file ng-scope"]')
                        self.zoom_out(6)
                        subcontent_files = self.DRIVER.find_elements(By.CSS_SELECTOR, 'a[class="text_link ng-binding"]')
                        true_file_names = []
                        #print(f"FOI --> {self.DRIVER.find_element(By.CSS_SELECTOR, 'div.person-name').text}")
                        #print(subcontent_files)
                        for file in subcontent_files:
                            # Download each file
                            #true_file_names.append(file.value_of_css_property("download"))
                            
                            # MAKE SURE THE LINK IS A DOWNLOADABLE FILE, OTHERWISE DON'T CLICK IT
                            if file.get_attribute('download') != '':
                                if file.get_attribute('download').endswith("mp4"):
                                    self.download_mp4(URL=file.get_attribute('href'), videoname=self.name_sanitizer(file.text), path=f"C:\\Users\\stardust\\Downloads\\PlurallScraper-dev-branch\\second\\plurallSubjects\\{current_subject_name}\\{current_content_name}\\{current_subcontent_name}\\")
                                else:
                                    # APPEN AND CLICK
                                    true_file_names.append(file.get_attribute('download'))
                                    # CLICK THE LINK
                                    file.click()
                            #print(file.find_element(By.CSS_SELECTOR, 'class="text_link ng-binding"'))
                        
                        # wait for the download to complete before moving the files
                        #time.sleep(3)
                        self.esperar_download()
                        for file_i in range(len(subcontent_files)):
                            filename, file_extension = os.path.splitext(str(true_file_names[file_i]))
                            #actual_file = os.path.join(self.folder_path, f"/downloads/{true_file_names[file_i]}")
                            #actual_dst = os.path.join(self.folder_path, f"/plurallSubjects/{current_subject_name}/{current_content_name}/{current_subcontent_name}/{self.name_sanitizer(subcontent_files[file_i].text)}{file_extension}")
                            actual_file = f"C:\\Users\\stardust\\Downloads\\PlurallScraper-dev-branch\\second\\downloads\\{filename}{file_extension}"
                            actual_dst = f"C:\\Users\\stardust\\Downloads\\PlurallScraper-dev-branch\\second\\plurallSubjects\\{current_subject_name}\\{current_content_name}\\{current_subcontent_name}\\{self.name_sanitizer(subcontent_files[file_i].text)}{file_extension}"
                            print(f"FILE --> {actual_file}")
                            print(f"DST --> {actual_dst}")

                            if not os.path.exists(actual_dst):
                                shutil.copy(actual_file, actual_dst)
                        
                        self.zoom_default()

                        
                        # Leave the iframe :D
                        self.DRIVER.switch_to.default_content()

                        # MAKE SURE TO CLOSE ANY TABS IT OPENED TO DOWNLOAD STUFF
                        try:
                            time.sleep(1)
                            for i in range(5):
                                self.DRIVER.switch_to.window(self.DRIVER.window_handles[1])
                                self.DRIVER.close()
                            self.DRIVER.switch_to.window(self.DRIVER.window_handles[0])
                        except Exception as E:
                            print(E)

                    except Exception as E:
                        self.DRIVER.switch_to.default_content()
                        self.zoom_default()
                        print(E)


                    go_back_button = self.DRIVER.find_element(By.CSS_SELECTOR, '.md-icon-button')
                    go_back_button.click()
                    time.sleep(1)



                time.sleep(1)
                go_back_button = self.DRIVER.find_element(By.CSS_SELECTOR, '.md-icon-button')
                go_back_button.click()
                time.sleep(1)

            # Before going back, go into each of the contents








            # Then go to each of the sub-contents



            # Then go to each of the sub-contents

            go_back_button = self.DRIVER.find_element(By.CSS_SELECTOR, '.md-icon-button')
            go_back_button.click()
            time.sleep(1)
            


    def filtrar_todas(self):
        filtro_button = self.DRIVER.find_element(By.CSS_SELECTOR, '.activity-status')
        filtro_button.click()

        opcao_todas = self.DRIVER.find_element(By.CSS_SELECTOR, '#select_option_4')
        opcao_todas.click()


    def salvar_conteudo(self, max_number_of_pages):
        #Abrir geografia
        self.DRIVER.find_element(By.CSS_SELECTOR, 'div.adp-list-item:nth-child(2)').click()

        for subject in range(1):
        
            contents = [] 

            for i in range(max_number_of_pages):
                current_contents = self.DRIVER.find_elements(By.CSS_SELECTOR, 'div[class="ng-scope"][data-ng-repeat="list in activitiesList"]')
                for cc in current_contents:
                    if cc not in contents:
                        contents.append(cc)


                # The html address will change as soon as I leave the page, so it's best to always get the new element address
                html_element = self.DRIVER.find_element(By.CSS_SELECTOR, 'html')
                """

                contents_titles_divs = self.DRIVER.find_elements(By.CSS_SELECTOR, 'div[class="list-title layout-column flex-auto"]')
                for content_title in contents_titles_divs:
                    content_name = content_title.find_element(By.CSS_SELECTOR, 'div[class="ng-binding"]').text
                    
                    # Normalize content name
                    content_name = self.name_sanitizer(content_name)
                    if content_name not in self.current_page_content_names:
                        self.current_page_content_names.append(content_name)

                """

                time.sleep(1)
                html_element.send_keys(Keys.PAGE_DOWN)
                # Try to find and press load more button
                try:
                    load_more_button = self.DRIVER.find_element(By.CSS_SELECTOR, "div.layout-align-end-center:nth-child(1) > button:nth-child(1)")
                    load_more_button.click()
                    # In case it works, wait a bit
                    time.sleep(1)
                except Exception as E:
                    print(E)

            for i in range(len(contents)):
                contents[i].click()
                go_back_button = self.DRIVER.find_element(By.CSS_SELECTOR, '.md-icon-button')
                go_back_button.click()
                time.sleep(1)


        
        print(contents)

        
        
        #contents_css_selectors = []
        #for i in range(10):
            #contents_css_selectors.append('.adp-list-container > div:nth-child(3)')





    def close(self):
        self.DRIVER.close()



if __name__ == "__main__":
    pass