from setuptools import setup, find_packages

VERSION = '1.0.2' 
DESCRIPTION = 'Conjunto de ferramentas Python'
LONG_DESCRIPTION = 'Conjunto personalizado de ferramentas para manipulações de arquivos .txt, .json, .csv, manipulação de registros Windows e mais.'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="my_tools", 
        version=VERSION,
        author="Iago Carvalho",
        author_email="<iagoo.felipe123@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)