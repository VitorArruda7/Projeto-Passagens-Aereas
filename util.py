from validate_docbr import CPF
cpf = CPF()

def verifica_cpf(login1):
    if cpf.validate(login1) is True:
        print("CPF Válido")
    else:
        raise ValueError("O CPF inserido é inválido")