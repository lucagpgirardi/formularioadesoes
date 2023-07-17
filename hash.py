import bcrypt

def gerar_hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

senha = ''
hash_senha = gerar_hash_senha(senha)
print(hash_senha)
