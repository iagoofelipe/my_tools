# módulos python
import sys, os, subprocess, json
import win32com.shell.shell as shell

__version__ = '1.0.1'
__path__ = os.path.abspath('')
__all__ = ('File', 'encode', 'Cpf', 'adm', 'Registros', 'resource_path')

""" 
Conjunto personalizado de ferramentas para manipulações de arquivos .txt, .json, .csv, manipulação de registros Windows e mais.

    - resource_path
    - encode
    - adm
    - Cpf
    - Registros
        get - pega valor em chave de registro
        set - define valor em chave registro
    - File    
        isFile - verifica se arquivo existe
        getFile - retorna conteúdo de um arquivo como lista
        toFile - armazena os dados em um arquivo
        required - verifica arquivos necessários


"""
#-----------------------------------RESOURCE-PATH-----------------------------------------------------
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#------------------------------------------------------------------------------------------------------
#----------------------------------------ENCODE--------------------------------------------------------
def encode(name, upper=False) -> str:
    from unicodedata import normalize

    ascii_name = normalize("NFKD", name).encode("ascii", errors="ignore").decode("ascii")        
    return ascii_name.upper() if upper else ascii_name
#------------------------------------------------------------------------------------------------------
#------------------------------------------ADM---------------------------------------------------------
def adm():
    """ solicitando acesso de administrador """
    ASADMIN = 'asadmin'
    
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
#------------------------------------------------------------------------------------------------------
#------------------------------------------CPF---------------------------------------------------------
""" 
    Manipulação de cpf

    formatar - formatação do cpf para padrão com pontos
    validadar - validação do cpf
"""
class Cpf:
    def formatar(cpf: str | int) -> str:
        """ retorna string do cpf no padrão 000.000.000-00 """
        cpf = str(cpf)
        
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


    def validar(cpf: str) -> bool:
        # Verifica a formatação do CPF
        if len(cpf) > 15 or len(cpf) < 11:
            return False

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True
#------------------------------------------------------------------------------------------------------
#--------------------------------------Registro--------------------------------------------------------
KEYNAME =  r'HKEY_LOCAL_MACHINE\SOFTWARE\CentralSuporte'

class Registros:
    """ Dados armazenados no Editor de Registro do Windows """
    def get(KEYNAME=KEYNAME, nome='all') -> dict | str:
        """ lendo dados de registro """
        output = subprocess.check_output(rf'reg query {KEYNAME}').decode(errors='ignore').split('\r\n')
        historico_de_registros = {}

        for linha in output[2:]:
            linha = linha.strip().split('    REG_SZ    ') # removendo espaço no início e separando chave de dados
            
            if linha == ['']:
                pass
            else:
                historico_de_registros[linha[0]] = linha[1]
        
        return historico_de_registros if nome == 'all' else historico_de_registros[nome]


    def set(KEYNAME=KEYNAME, **kwargs) -> None:
        adm_exe = True
        if 'dict' in kwargs:
            kwargs = kwargs['dict']

        for nome, dados in kwargs.items():
            os.system(f'reg add {KEYNAME} /v {str(nome)} /d "{str(dados)} " /f')
            
            if adm_exe:
                adm()
                adm_exe = False
#------------------------------------------------------------------------------------------------------
#---------------------------------------File-----------------------------------------------------------
class File:
    @staticmethod
    def isFile(fileName, default_dir=False) -> bool:
        """Verifica se arquivo existe. 
        \ndefault_dir utilizado caso __class__.path esteja definido
        """
        if default_dir:
            fileName = f'{__path__}\\{fileName}'

        return os.path.exists(fileName)

    @staticmethod
    def getFile(fileName: str, default_dir=False) -> list | None:
        """ lendo arquivos e retornando lista com dados """
        file_type = fileName.split('.')[-1]
        if default_dir: fileName = f'{__path__}\\{fileName}'

        if not __class__.isFile(fileName):
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


    @staticmethod
    def toFile(fileName: str, dados: list | dict | tuple, default_dir=False) -> None:
        """ 
        gera arquivo com dados informados, substitui o arquivo caso já exista.

        fileName: .csv | .txt | .json
        dados : list | dict | tuple
        """
        file_type = fileName.split('.')[-1]
        
        if default_dir: fileName = f'{__path__}\\{fileName}'

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


    @staticmethod
    def delFile(fileName: str, default_dir=False) -> bool:
        """ remove arquivo/pasta especificada """
        if default_dir: fileName = f'{__path__}\\{fileName}'
        
        if not __class__.isFile(fileName):
            return None

        return not bool(os.system('rmdir /s /q ' + fileName))


    @staticmethod
    def appendFile(fileName: str, dados: str | list | tuple, default_dir=False) -> bool:
        if type(dados) not in (str, list, tuple):
            return False

        if default_dir: fileName = f'{__path__}\\{fileName}'

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
#------------------------------------------------------------------------------------------------------
