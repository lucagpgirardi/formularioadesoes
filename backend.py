import os
import csv
from flask import Flask, render_template, request, redirect, session, url_for
from flask_dropzone import Dropzone
from functools import wraps
import bcrypt

app = Flask(__name__, template_folder='.')

app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 16
app.config['DROPZONE_MAX_FILES'] = 10
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_PARALLEL_UPLOADS'] = 3
app.config['DROPZONE_TIMEOUT'] = 5 * 60 * 1000  # 5 minutes
app.config['DROPZONE_UPLOAD_ON_CLICK'] = True
app.config['DROPZONE_UPLOAD_ACTION'] = 'upload'  # URL do endpoint para processar o upload

dropzone = Dropzone(app)

# Configuração para a sessão
app.secret_key = 'sua_chave_secreta_aqui'

# Dicionário para armazenar os usuários e senhas (substitua com seus próprios usuários)
usuarios = {
    'luca': '$2b$12$UaN32w9XLCDT5.YCAVDuMeDRH7xMA3VUHMA7JA93K3WArZcEE074m',
    'sueli': '$2b$12$x2r3Tz.QTDj392O54nHVvO2xPpcePECSO2aweIxCFa6L4gHO1XI/G'
}

def verificar_autenticacao(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrapper

# Rota para a página inicial
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and bcrypt.checkpw(password.encode(), usuarios[username].encode()):
            session['usuario'] = username
            return redirect('/formulario')
        else:
            return render_template('login.html', error='Credenciais inválidas.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/login')

@app.route('/formulario')
@verificar_autenticacao
def formulario():
    return render_template('formulario.html')

@app.route('/processar_formulario', methods=['POST'])
@verificar_autenticacao
def processar_formulario():
    print("Iniciando processamento do formulário...")

    oficial = request.form['oficial']
    rua = request.form['rua']
    numero = request.form['numero']
    complemento = request.form['complemento']
    regiao = request.form['regiao']
    rgi = request.form['rgi']
    hidrometro = request.form['hidrometro']
    inspecao = request.form['inspecao']
    ligacao = request.form['ligacao']
    cliente = request.form['cliente']
    relacionamento = request.form['relacionamento']
    profissao = request.form['profissao']
    nacionalidade = request.form['nacionalidade']
    estado_civil = request.form['estado_civil']
    telefone = request.form['telefone']
    rg = request.form['rg']
    cpf = request.form['cpf']
    data_nascimento = request.form['data_nascimento']
    hd = request.form['hd']
    leitura_hd = request.form['leitura_hd']
    abastecimento = request.form['abastecimento']
    ligacao_esgoto = request.form['ligacao_esgoto']

    print("Oficial:", oficial)
    print("Rua:", rua)
    print("Número:", numero)
    print("Complemento:", complemento)
    print("Região:", regiao)

    # Criação das pastas com base nos dados do formulário
    destino = os.path.join(regiao, rua, numero, complemento)
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Verifica se o formulário possui arquivos de imagem
    if 'file' in request.files:
        imagens = request.files.getlist('file')
        print("Número de imagens:", len(imagens))

        for i, imagem in enumerate(imagens):
            nome_arquivo = imagem.filename
            print(f"Imagem {i + 1} - Nome do arquivo:", nome_arquivo)
            caminho_final = os.path.join(destino, nome_arquivo)
            print(f"Imagem {i + 1} - Caminho final:", caminho_final)
            imagem.save(caminho_final)

    # Salva os dados em um arquivo CSV
    dados = [oficial, rua, numero, complemento, regiao, rgi, hidrometro, inspecao, cliente, relacionamento,
             profissao, nacionalidade, estado_civil, telefone, rg, cpf, data_nascimento, hd, leitura_hd,
             abastecimento, ligacao_esgoto]
    salvar_dados_csv(dados)

    return render_template('formulario.html', success=True)

@app.route('/novo_formulario')
@verificar_autenticacao
def novo_formulario():
    return redirect(url_for('formulario'))

def salvar_dados_csv(dados):
    nome_arquivo_csv = 'dados_formulario.csv'

    # Verifica se o arquivo CSV já existe
    arquivo_existe = os.path.isfile(nome_arquivo_csv)

    with open(nome_arquivo_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Escreve o cabeçalho do arquivo CSV, caso ele não exista
        if not arquivo_existe:
            writer.writerow(['Oficial', 'Rua', 'Número', 'Complemento', 'Região', 'RGI', 'Número do Hidrômetro',
                             'Relatório da Inspeção', 'Nome do Cliente', 'Relacionamento com Imóvel', 'Profissão',
                             'Nacionalidade', 'Estado Civil', 'Telefone Celular', 'RG', 'CPF', 'Data de Nascimento',
                             'Existe HD no local?', 'Leitura do HD', 'Abastecimento normal?', 'Ligação de Esgoto'])

        writer.writerow(dados)


if __name__ == '__main__':
    app.run(debug=True)
