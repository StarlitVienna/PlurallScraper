from plurallScraper import PlurallScraper
from creds import email, password
import time
# Use argparse later on
# With argparse also let the user setup how many seconds wait between scrolls

# EITHER MAKE YOUR OWN CREDS.PY OR JUST WRITE YOUR CREDENTIALS AS A STRING IN THE CLASS PlurallScraper

# Make the user make sure the firefox default zoom is set to 30% so it can take full screenshots


def main_func():
    mainScraper = PlurallScraper(email=email, password=password)
    mainScraper.setup()
    mainScraper.login()
    mainScraper.abrir_maestro()
    mainScraper.criar_pastas_materias()
    mainScraper.criar_pastas_conteudos_materias(max_number_of_pages=3)
    #mainScraper.salvar_conteudo(max_number_of_pages=3)

    mainScraper.close()



if __name__ == "__main__":
    main_func()
