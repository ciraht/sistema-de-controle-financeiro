import os
import plotly.express as px
import fdb
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

host = 'localhost'

pasta_atual = os.path.dirname(__file__)
database = os.path.join(pasta_atual, 'banco.fdb')

user = 'SYSDBA'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)


class Users:
    def __init__(self, id_user, nome, cpf, nascimento, senha, email):
        self.id_user = id_user
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.senha = senha
        self.email = email


class Despesas:
    def __init__(self, id_despesa, motivo, valor, data_despesa, id_user):
        self.id_despesa = id_despesa
        self.motivo = motivo
        self.valor = valor
        self.data_despesas = data_despesa
        self.id_user = id_user


class Receitas:
    def __init__(self, id_receita, motivo, valor, data_receita, id_user):
        self.id_receita = id_receita
        self.motivo = motivo
        self.valor = valor
        self.data_receitas = data_receita
        self.id_user = id_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dicas1', methods=['GET'])
def dicas1():
    if session.get('id_user') == '':
        return redirect('/')
    users = [session.get('id_user'), session.get('nome')]
    perfis = session.get('perfis')
    return render_template('dicas1.html', users=users, perfis=perfis)


@app.route('/dicas2')
def dicas2():
    if session.get('id_user') == '':
        return redirect('/')
    users = [session.get('id_user'), session.get('nome')]
    perfis = session.get('perfis')
    return render_template('dicas2.html', users=users, perfis=perfis)


@app.route('/dicas3')
def dicas3():
    if session.get('id_user') == '':
        return redirect('/')
    users = [session.get('id_user'), session.get('nome')]
    perfis = session.get('perfis')
    return render_template('dicas3.html', users=users, perfis=perfis)


@app.route('/dicas4')
def dicas4():
    if session.get('id_user') == '':
        return redirect('/')
    users = [session.get('id_user'), session.get('nome')]
    perfis = session.get('perfis')
    return render_template('dicas4.html', users=users, perfis=perfis)


@app.route('/home', methods=['GET'])
def home():
    if session.get('id_user') == '':
        return redirect('/')
    id_user = session.get('id_user')
    users = [session.get('id_user'), session.get('nome')]
    perfis = session.get('perfis')

    cursor = con.cursor()

    cursor.execute('SELECT ID_RECEITA, MOTIVO, VALOR, DATA_RECEITA FROM RECEITAS WHERE id_user = ?', (id_user,))
    receitas = cursor.fetchall()
    cursor.execute('SELECT ID_DESPESA, MOTIVO, VALOR, DATA_DESPESA FROM DESPESAS WHERE id_user = ?', (id_user,))
    despesas = cursor.fetchall()
    cursor.execute('SELECT MOTIVO, VALOR, DATA_RECEITA FROM RECEITAS WHERE id_user = ?', (id_user,))
    grafico_receitas = cursor.fetchall()
    cursor.execute('SELECT MOTIVO, VALOR, DATA_DESPESA FROM DESPESAS WHERE id_user = ?', (id_user,))
    grafico_despesas = cursor.fetchall()
    cursor.close()

    saldo = 0
    for receita in receitas:
        saldo += receita[2]
    for despesa in despesas:
        saldo -= despesa[2]

    import pandas as pd
    receitas_df = pd.DataFrame(grafico_receitas, columns=["Motivo", "Valor", "Data"])
    receitas_df["Tipo"] = "Receita"
    despesas_df = pd.DataFrame(grafico_despesas, columns=["Motivo", "Valor", "Data"])
    despesas_df["Tipo"] = "Despesa"

    df = pd.concat([receitas_df, despesas_df])

    df["Data"] = pd.to_datetime(df["Data"])

    df["Mes"] = df["Data"].dt.to_period("M").astype(str)

    fig = px.bar(
        df,
        x="Mes",
        y="Valor",
        color="Tipo",
        title="Evolução Financeira Mensal",
        labels={"Valor": "R$", "Mes": "Mês"}
    )

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        barmode='group'
    )

    graph_html = fig.to_html(full_html=False)

    return render_template('home.html', users=users, receitas=receitas, despesas=despesas, total=saldo, perfis=perfis, graph_html=graph_html)


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    cpf = request.form['cpf'].replace(".", "").replace("-", "")
    nascimento = request.form['nascimento']
    email = request.form['email']
    senha = request.form['senha']
    senhaCorreta = request.form['senhaCorreta']

    if not validar_cpf(cpf):
        flash("Erro: CPF inválido. Insira um CPF válido.", "error")
        return redirect(url_for('cadastro'))

    cursor = con.cursor()

    try:
        cursor.execute("SELECT 1 FROM USERS WHERE cpf = ?", (cpf,))
        if cursor.fetchone():
            flash("Erro: CPF já cadastrado.", "error")
            return redirect(url_for('cadastro'))
        cursor.execute("SELECT 1 FROM USERS WHERE email = ?", (email,))
        if cursor.fetchone():
            flash("Erro: Email já cadastrado.", "error")
            return redirect(url_for('cadastro'))
        if senha != senhaCorreta:
            flash("Erro: Senha Incorreta.", "error")
            return redirect(url_for('cadastro'))

        cursor.execute("INSERT INTO users (nome, cpf, email, senha, nascimento) VALUES (?, ?, ?, ?, ?)",
                       (nome, cpf, email, senha, nascimento))
        con.commit()
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(f"Erro ao fechar o cursor: {e}")

    flash("Usuário cadastrado com sucesso!", "success")
    return redirect('/login')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logar', methods=['POST'])
def logar():
    email = request.form['email']
    senha = request.form['senha']

    cursor = con.cursor()

    try:
        cursor.execute("SELECT 1 FROM users WHERE email = ? AND senha = ?", (email, senha))
        if not cursor.fetchone():
            flash("Credenciais Inválidas", "error")
            cursor.close()
            return redirect(url_for('login'))
        else:
            session['email'] = email
            session['senha'] = senha
            cursor.execute("SELECT id_user, nome, cpf, nascimento, email, senha FROM users WHERE email = ? AND senha = ?",
                           (email, senha))
            usuario = cursor.fetchone()
            session['nome'] = usuario[1]
            session['cpf'] = usuario[2]
            session['nascimento'] = usuario[3]
            session['id_user'] = usuario[0]
            session['perfis'] = usuario

    except Exception as e:
        flash(f"Erro ao logar: {e}", "error")
        cursor.close()
        return redirect(url_for('login'))

    cursor.close()
    flash("Usuário entrou com sucesso!", "success")
    return redirect('/home')


@app.route('/editar_usuario', methods=['POST', 'GET'])
def editar_usuario():
    if session.get('id_user') == '':
        return redirect('/')
    email = session.get('email')
    senhaCorreta = session.get('senha')

    cursor = con.cursor()

    cursor.execute("select id_user, nome, cpf, nascimento, email, senha from users where email = ?", (email,))
    user = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        nascimento = request.form['nascimento']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = request.form['senha']
        senhaAntiga = request.form['senhaAntiga']

        if senhaAntiga == senhaCorreta:
            id_user = user[0]

            cursor.execute("UPDATE users SET nome = ?, cpf = ?, nascimento = ?, email = ?, senha = ? WHERE id_user = ?",
                           (nome, cpf, nascimento, email, senha, id_user))
            con.commit()

            session['email'] = email
            session['senha'] = senha

            cursor.close()
            flash("Usuário atualizado com sucesso!", "success")
            return redirect('/home')
        else:
            flash("Senha Incorreta", "error")
            if cursor:
                cursor.close()
            return redirect('/editar_usuario')

    cursor.close()

    return render_template('editar_usuario.html', user=user)


@app.route('/criar_receita', methods=['POST', 'GET'])
def criar_receita():
    if session.get('id_user') == '':
        return redirect('/')
    motivo = request.form['motivo_receita']
    valor = request.form['valor_receita']
    data_receita = request.form['data_receita']
    if data_receita < "1900-01-01" or data_receita > "2099-12-12":
        return redirect('/nova_receita')
    id_user = session.get('id_user')

    cursor = con.cursor()

    try:
        cursor.execute("INSERT INTO receitas (motivo, valor, data_receita, id_user) VALUES (?, ?, ?, ?)",
                       (motivo, valor, data_receita, id_user))
        con.commit()
    finally:
        cursor.close()

    flash("Receita cadastrada com sucesso!", "success")
    return redirect('/home')


@app.route('/criar_despesa', methods=['POST', 'GET'])
def criar_despesa():
    if session.get('id_user') == '':
        return redirect('/')
    motivo = request.form['motivo_despesa']
    valor = request.form['valor_despesa']
    data_despesa = request.form['data_despesa']
    if data_despesa < "1900-01-01" or data_despesa > "2099-12-12":
        return redirect('/nova_despesa')
    id_user = session.get('id_user')

    cursor = con.cursor()

    try:
        cursor.execute("INSERT INTO despesas (motivo, valor, data_despesa, id_user) VALUES (?, ?, ?, ?)",
                       (motivo, valor, data_despesa, id_user))
        con.commit()
    finally:
        cursor.close()

    flash("Despesa cadastrada com sucesso!", "success")
    return redirect('/home')


@app.route('/nova_receita', methods=['GET'])
def nova_receita():
    if session.get('id_user') == '':
        return redirect('/')
    id_user = session.get('id_user')
    cursor = con.cursor()
    cursor.execute("select id_receita, motivo, valor, data_receita from receitas where id_user = ?", (id_user,))
    receitas = cursor.fetchall()
    perfis = session.get('perfis')
    cursor.close()
    return render_template('nova_receita.html', receitas=receitas, perfis=perfis)


@app.route('/nova_despesa', methods=['GET'])
def nova_despesa():
    if session.get('id_user') == '':
        return redirect('/')
    id_user = session.get('id_user')
    cursor = con.cursor()
    cursor.execute("select id_despesa, motivo, valor, data_despesa from despesas where id_user = ?", (id_user,))
    despesas = cursor.fetchall()
    perfis = session.get('perfis')
    cursor.close()
    return render_template('nova_despesa.html', despesas=despesas, perfis=perfis)


@app.route('/atualizar_receita', methods=['GET'])
def atualizar_receita():
    if session.get('id_user') == '':
        return redirect('/')
    id_user = session.get('id_user')
    cursor = con.cursor()
    cursor.execute("select id_receita, motivo, valor, data_receita from receitas where id_user = ?", (id_user,))
    receitas = cursor.fetchall()
    perfis = session.get('perfis')
    cursor.close()
    return render_template('editar_receita.html', receitas=receitas, perfis=perfis)


@app.route('/atualizar_despesa')
def atualizar_despesa():
    if session.get('id_user') == '':
        return redirect('/')
    id_user = session.get('id_user')
    cursor = con.cursor()
    cursor.execute("select id_despesa, motivo, valor, data_despesa from despesas where id_user = ?", (id_user,))
    despesas = cursor.fetchall()
    perfis = session.get('perfis')
    cursor.close()
    return render_template('editar_despesa.html', despesas=despesas, perfis=perfis)


@app.route('/editar_receita/<int:id>', methods=['GET', 'POST'])
def editar_receita(id):
    if session.get('id_user') == '':
        return redirect('/')
    perfis = session.get('perfis')
    cursor = con.cursor()
    cursor.execute("SELECT ID_RECEITA, MOTIVO, VALOR, DATA_RECEITA FROM RECEITAS WHERE ID_RECEITA = ?", (id,))
    receita = cursor.fetchone()

    if not receita:
        cursor.close()
        flash("Receita não encontrada!", "error")
        return redirect('/nova_receita')

    if request.method == 'POST':
        motivo = request.form['motivo_receita']
        valor = request.form['valor_receita']
        data = request.form['data_receita']

        cursor.execute("UPDATE receitas SET motivo = ?, valor = ?, data_receita = ? WHERE id_receita = ?",
                       (motivo, valor, data, id))
        con.commit()
        cursor.close()
        flash("Receita atualizada com sucesso!", "success")
        return redirect('/nova_receita')

    cursor.close()

    return render_template('editar_receita.html', receita=receita, perfis=perfis)


@app.route('/editar_despesa/<int:id>', methods=['GET', 'POST'])
def editar_despesa(id):
    if session.get('id_user') == '':
        return redirect('/')
    perfis = session.get('perfis')
    id_user = session.get('id_user')
    cursor = con.cursor()
    cursor.execute("SELECT ID_DESPESA, MOTIVO, VALOR, DATA_DESPESA FROM DESPESAS WHERE ID_DESPESA = ? ", (id,))
    despesa = cursor.fetchone()

    if not despesa:
        cursor.close()
        flash("Despesa não encontrada!", "error")
        return redirect('/nova_despesa')

    if request.method == 'POST':
        motivo = request.form['motivo_despesa']
        valor = request.form['valor_despesa']
        data = request.form['data_despesa']

        cursor.execute("UPDATE despesas SET motivo = ?, valor = ?, data_despesa = ? WHERE id_despesa = ?",
                       (motivo, valor, data, id))
        con.commit()
        cursor.close()
        flash("Despesa atualizada com sucesso!", "success")
        return redirect('/nova_despesa')

    cursor.close()


    return render_template('editar_despesa.html', despesa=despesa, perfis=perfis)


@app.route('/deletar_receita/<int:id>', methods=('POST', 'GET'))
def deletar_receita(id):
    if session.get('id_user') == '':
        return redirect('/')
    cursor = con.cursor()

    try:
        cursor.execute('DELETE FROM receitas WHERE id_receita = ?', (id,))
        con.commit()
        flash('Receita excluída com sucesso!', 'success')
    except Exception as e:
        con.rollback()
        flash('Erro ao excluir a receita.', 'error')
    finally:
        cursor.close()

    return redirect('/nova_receita')


@app.route('/deletar_despesa/<int:id>', methods=('POST', 'GET'))
def deletar_despesa(id):
    if session.get('id_user') == '':
        return redirect('/')
    cursor = con.cursor()

    try:
        cursor.execute('DELETE FROM despesas WHERE id_despesa = ?', (id,))
        con.commit()
        flash('Despesa excluída com sucesso!', 'success')
    except Exception as e:
        con.rollback()
        flash('Erro ao excluir a despesa.', 'error')
    finally:
        cursor.close()

    return redirect('/nova_despesa')


@app.route('/sair')
def sair():
    session['id_user'] = ''
    session['cpf'] = ''
    session['nome'] = ''
    session['nascimento'] = ''
    session['email'] = ''
    session['senha'] = ''
    flash("Saida realizada com sucesso", "success")
    return redirect('/')


def validar_cpf(cpf: str) -> bool:
    cpf = cpf.replace(".", "").replace("-", "").replace(" ", "")

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    primeiro_digito = (soma * 10 % 11) % 10

    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    segundo_digito = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"


if __name__ == '__main__':
    app.run(debug=True)
