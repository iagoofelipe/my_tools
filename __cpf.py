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