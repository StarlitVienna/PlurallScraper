from plurallScraper import PlurallScraper

# Use argparse later on

# EITHER MAKE YOUR OWN CREDS.PY OR JUST WRITE YOUR CREDENTIALS AS A STRING IN THE CLASS PlurallScraper

def main_func():
    mainScraper = PlurallScraper(
        email="",
        password="")
    mainScraper.setup()
    mainScraper.login()
    mainScraper.abrir_maestro()
    mainScraper.criar_pastas_materias()

    #mainScraper.close()

if __name__ == "__main__":
    main_func()
