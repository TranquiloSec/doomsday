import os

def verificar_resources(pasta='resources'):
    verifica_pasta_existe(nome_pasta=pasta)
    verifica_arquivos_existem(nome_pasta=pasta)


def verifica_pasta_existe(nome_pasta='resources'):
    caminho_pasta = os.path.join(os.getcwd(), nome_pasta)
    if os.path.isdir(caminho_pasta):
        print(f" Pasta '{nome_pasta}' - OK.")
        return True
    else:
        print(f" Pasta '{nome_pasta}' - Não Encontrada.")
        os.mkdir(nome_pasta)
        print(f" Pasta {nome_pasta} - OK")
        return False


def verifica_arquivos_existem(nome_pasta):
    if os.path.exists(f".\\{nome_pasta}\\ua.txt"):
        print(' ua.txt - OK')
    else:
        with open('.\\resources\\ua.txt', 'w') as f:
            pass
            print(" ua.txt  - Criado")
            
            
    if os.path.exists(f".\\{nome_pasta}\\proxy.txt"):
        print(' proxy.txt - Ok')
    else:
            print(" proxy.txt - Não Encontrado")
            
            
    if os.path.exists(f".\\{nome_pasta}\\headers.txt"):
        print(' headers.txt - Ok')
    else:
        with open(f'.\\{nome_pasta}\\headers.txt', 'w') as f:
            pass
            print(" headers.txt - Criado")