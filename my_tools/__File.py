""" 
Funções para manipulação de arquivos

    isFile - verifica se arquivo existe
    getFile - retorna conteúdo de um arquivo como lista
    toFile - armazena os dados em um arquivo
    required - verifica arquivos necessários

    Json - manipulação de arquivos json
        Json.getJson - mesmo que getFile
        Json.setJson - mesmo que toFile

    # getDadosBase - extrai dados da base Gestão (base_gestao.csv)

"""
import json, os
from os.path import exists

class File:
    def __init__(self):
        self._path = os.path.abspath('')


    def isFile(self, fileName, default_dir=False) -> bool:
        """Verifica se arquivo existe. 
        \ndefault_dir utilizado caso __class__.path esteja definido
        """
        if default_dir:
            fileName = f'{self._path}\\{fileName}'

        return exists(fileName)


    def getFile(self, fileName: str, default_dir=False) -> list | None:
        """ lendo arquivos e retornando lista com dados """
        file_type = fileName.split('.')[-1]
        if default_dir: fileName = f'{self._path}\\{fileName}'

        if not self.isFile(fileName):
            return None
        
        if file_type == 'json':
            with open(fileName, 'r', encoding='utf8') as f:
                return json.load(f)
        
        elif file_type in ('txt','csv'):
            with open(fileName, 'r') as arquivo:
                try:
                    linhas, result = arquivo.readlines(), []
                    for i in linhas:
                        i = i.strip('\n')
                        if ';' in i:
                            i = i.split(';')

                        result.append(i)
                    return result

                except UnicodeDecodeError:
                    pass
        return None # em caso de exceção UnicodeDecodeError ou tipo de arquivo não ser compatível


    def toFile(self, fileName: str, dados: list | dict | tuple, default_dir=False) -> None:
        """ 
        gera arquivo com dados informados, substitui o arquivo caso já exista.

        fileName: .csv | .txt | .json
        dados : list | dict | tuple
        """
        file_type = fileName.split('.')[-1]
        
        if default_dir: fileName = f'{self._path}\\{fileName}'

        if file_type == 'json':
            with open(fileName, 'w', encoding='utf8') as f:
                json.dump(dados, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))

        elif file_type in ('txt', 'csv'):
            with open(fileName, 'w') as arquivo:
                if type(dados) == dict:
                    for chave in dados:
                        conteudo = dados[chave]
                        arquivo.write(str(chave) + ';')
                    
                        if type(conteudo) == list:
                            for i in conteudo:
                                arquivo.write(i + ';')
                        else:
                                arquivo.write(str(conteudo) + ';')

                        arquivo.write('\n')
                            
                elif type(dados) in (list, tuple):
                    for conteudo in dados:
                        arquivo.write(str(conteudo) + '\n')
                else:
                    arquivo.write(str(dados) + '\n')


    def delFile(self, fileName: str, default_dir=False) -> bool:
        """ remove arquivo/pasta especificada """
        if default_dir: fileName = f'{self._path}\\{fileName}'
        
        if not self.isFile(fileName):
            return None

        return not bool(os.system('rmdir /s /q ' + fileName))


    def appendFile(self, fileName: str, dados: str | list | tuple, default_dir=False) -> bool:
        if type(dados) not in (str, list, tuple):
            return False

        if default_dir: fileName = f'{self._path}\\{fileName}'

        with open(fileName, 'a') as f:
            if type(dados) == str:
                f.write(dados + '\n')
            
            elif type(dados) in (list, tuple):
                for i in dados:
                    f.write(i + ';')
                f.write('\n')
            
            return True
    
    
    @property
    def path(self):
        """ local path """
        return self._path
