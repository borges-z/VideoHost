import secrets
import string

def gerar_string_aleatoria():
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(100))

