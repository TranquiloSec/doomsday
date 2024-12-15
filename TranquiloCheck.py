import os

def verificar_resources(pasta='resources'):
    """
    Main function that ensures the existence of the folder and necessary files.
    Calls auxiliary functions to check folder and files.
    """
    verifica_pasta_existe(nome_pasta=pasta)
    verifica_arquivos_existem(nome_pasta=pasta)


def verifica_pasta_existe(nome_pasta='resources'):
    """
    Checks if the 'resources' folder (or another defined one) exists.
    If it does not exist, creates the folder.

    Parameters:
    nome_pasta (str): Name of the folder to check/create.

    Returns:
    bool: True if the folder already existed, False if it had to be created.
    """
    caminho_pasta = os.path.join(os.getcwd(), nome_pasta)
    if os.path.isdir(caminho_pasta):
        # The folder already exists
        print(f" Pasta '{nome_pasta}' - OK.")
        return True
    else:
        # Folder does not exist, create it
        print(f" Pasta '{nome_pasta}' - Não Encontrada.")
        os.mkdir(nome_pasta)
        print(f" Pasta {nome_pasta} - OK")
        return False


def verifica_arquivos_existem(nome_pasta):
    """
    Checks for the existence of ua.txt, proxy.txt, and headers.txt files inside the specified folder.
    Creates empty files for ua.txt and headers.txt if they do not exist.
    For proxy.txt, only informs if it is not found (does not create automatically).

    Parameters:
    nome_pasta (str): Folder where the files will be checked.
    """
    # Check if ua.txt exists, otherwise create an empty file.
    if os.path.exists(f".\\{nome_pasta}\\ua.txt"):
        print(' ua.txt - OK')
    else:
        with open(f'.\\{nome_pasta}\\ua.txt', 'w') as f:
            pass  # Cria um arquivo vazio
        print(" ua.txt  - Created")
            
    # Check if proxy.txt exists, otherwise just inform.
    if os.path.exists(f".\\{nome_pasta}\\proxy.txt"):
        print(' proxy.txt - OK')
    else:
        print(" proxy.txt - Not Found")
            
    # Check if headers.txt exists, otherwise create an empty file.
    if os.path.exists(f".\\{nome_pasta}\\headers.txt"):
        print(' headers.txt - Ok')
    else:
        with open(f'.\\{nome_pasta}\\headers.txt', 'w') as f:
            pass  # Create an empty file
        print(" headers.txt - Created")
