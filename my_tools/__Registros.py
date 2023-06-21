from my_tools.__adm import adm
import subprocess, os

# KEYNAME =  r'HKEY_LOCAL_MACHINE\SOFTWARE\CentralSuporte'
class Registros:
    """ Dados armazenados no Editor de Registro do Windows """
    def get(KEYNAME, nome='all') -> dict | str:
        """ lendo dados de registro """
        output = subprocess.check_output(rf'reg query {KEYNAME}').decode(errors='ignore').replace(f'\r\n{KEYNAME}\r\n    ', '').split('\r\n')
        historico_de_registros = {}

        for linha in output[2:]:
            linha = linha.strip().split('    REG_SZ    ') # removendo espaço no início e separando chave de dados
            
            if linha == ['']:
                pass
            else:
                historico_de_registros[linha[0]] = linha[1]
        
        return historico_de_registros if nome == 'all' else historico_de_registros[nome]


    def set(KEYNAME, **kwargs) -> None:
        adm_exe = True
        if 'dict' in kwargs:
            kwargs = kwargs['dict']

        for nome, dados in kwargs.items():
            os.system(f'reg add {KEYNAME} /v {str(nome)} /d "{str(dados)}" /f')
            
            if adm_exe:
                adm()
                adm_exe = False