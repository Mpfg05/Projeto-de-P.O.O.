#tudo rs

# Importação das bibliotecas necessárias para manipulação do banco de dados
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Configuração do banco de dados SQLite e criação de uma sessão para interagir com o banco
engine = create_engine('sqlite:///biblioteca.db')  # Criação do motor de banco de dados
Session = sessionmaker(bind=engine)  # Criação da classe de sessão
session = Session()  # Instância da sessão para interagir com o banco de dados

# Base para as classes de modelo
Base = declarative_base()  # Cria uma classe base para os modelos

# Modelo para Aluno
class Aluno(Base):
    __tablename__ = 'alunos'  # Nome da tabela no banco de dados

    # Definição das colunas da tabela
    ra = Column(String, primary_key=True)  # RA do aluno, serve como identificador único
    nome = Column(String)  # Nome do aluno
    idade = Column(Integer)  # Idade do aluno
    turmas = relationship('Turma', secondary='aluno_turma')  # Relacionamento de muitos-para-muitos com turmas

    # Representação do objeto Aluno
    def __repr__(self):
        return f'<Aluno(ra={self.ra}, nome={self.nome}, idade={self.idade})>'  # Formato de impressão do aluno

# Modelo para Turma
class Turma(Base):
    __tablename__ = 'turmas'  # Nome da tabela no banco de dados

    # Definição das colunas da tabela
    rt = Column(String, primary_key=True)  # RT da turma, serve como identificador único
    ano = Column(String)  # Ano da turma (exemplo: '7')
    classe = Column(String)  # Classe da turma (exemplo: 'A')
    alunos = relationship('Aluno', secondary='aluno_turma')  # Relacionamento com alunos
    professores = relationship('Professor', secondary='professor_turma')  # Relacionamento com professores

    # Representação do objeto Turma
    def __repr__(self):
        return f'<Turma(rt={self.rt}, ano={self.ano}, classe={self.classe})>'  # Formato de impressão da turma

# Tabela de associação entre Aluno e Turma
class AlunoTurma(Base):
    __tablename__ = 'aluno_turma'  # Nome da tabela de associação
    aluno_ra = Column(String, ForeignKey('alunos.ra'), primary_key=True)  # Chave estrangeira para a tabela alunos
    turma_rt = Column(String, ForeignKey('turmas.rt'), primary_key=True)  # Chave estrangeira para a tabela turmas

# Modelo para Professor
class Professor(Base):
    __tablename__ = 'professores'  # Nome da tabela no banco de dados

    # Definição das colunas da tabela
    rp = Column(Integer, primary_key=True)  # RP do professor, identificador único
    nome = Column(String)  # Nome do professor

    # Representação do objeto Professor
    def __repr__(self):
        return f'<Professor(nome={self.nome}, rp={self.rp})>'  # Formato de impressão do professor

# Tabela de associação entre Professor e Turma
class ProfessorTurma(Base):
    __tablename__ = 'professor_turma'  # Nome da tabela de associação
    professor_rp = Column(Integer, ForeignKey('professores.rp'), primary_key=True)  # Chave estrangeira para a tabela professores
    turma_rt = Column(String, ForeignKey('turmas.rt'), primary_key=True)  # Chave estrangeira para a tabela turmas

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)  # Cria todas as tabelas definidas na base de dados

# Função para adicionar um aluno ao banco de dados
def adicionar_aluno(ra, nome, idade):
    aluno_existente = session.query(Aluno).filter_by(ra=ra).first()  # Verifica se o aluno já existe
    if not aluno_existente:  # Se não existir, cria um novo aluno
        novo_aluno = Aluno(ra=ra, nome=nome, idade=idade)  # Cria um objeto Aluno
        session.add(novo_aluno)  # Adiciona o aluno à sessão
        session.commit()  # Confirma a transação no banco de dados
        print(f'Aluno {nome} (RA: {ra}, idade: {idade}) adicionado com sucesso!')  # Mensagem de sucesso
    else:
        print("Aluno com RA já existe!")  # Mensagem de erro se o aluno já estiver registrado

# Função para listar todos os alunos cadastrados
def consultar_alunos():
    alunos = session.query(Aluno).all()  # Recupera todos os alunos da tabela
    for aluno in alunos:
        print(f'RA: {aluno.ra}, Nome: {aluno.nome}, Idade: {aluno.idade}')  # Imprime os dados de cada aluno

# Função para adicionar uma turma ao banco de dados
def adicionar_turma(rt, ano, classe):
    turma_existente = session.query(Turma).filter_by(rt=rt).first()  # Verifica se a turma já existe
    if not turma_existente:  # Se não existir, cria uma nova turma
        nova_turma = Turma(rt=rt, ano=ano, classe=classe)  # Cria um objeto Turma
        session.add(nova_turma)  # Adiciona a turma à sessão
        session.commit()  # Confirma a transação no banco de dados
        print(f'Turma {rt} (ano: {ano}, classe: {classe}) adicionada com sucesso!')  # Mensagem de sucesso
    else:
        print("Turma com RT já existe!")  # Mensagem de erro se a turma já estiver registrada

# Função para listar todas as turmas cadastradas
def consultar_turmas():
    turmas = session.query(Turma).all()  # Recupera todas as turmas da tabela
    for turma in turmas:
        print(f'RT: {turma.rt}, Ano: {turma.ano}, Classe: {turma.classe}')  # Imprime os dados de cada turma

# Função para associar um aluno a uma turma
def adicionar_aluno_a_turma(aluno_ra, turma_rt):
    aluno = session.query(Aluno).filter_by(ra=aluno_ra).first()  # Busca o aluno pelo RA
    turma = session.query(Turma).filter_by(rt=turma_rt).first()  # Busca a turma pelo RT
    if aluno and turma:  # Se ambos forem encontrados
        turma.alunos.append(aluno)  # Adiciona o aluno à turma
        session.commit()  # Confirma a transação no banco de dados
        print(f'Aluno {aluno.nome} (RA: {aluno.ra}) adicionado à turma {turma.rt}.')  # Mensagem de sucesso
    else:
        print("Aluno ou Turma não encontrados.")  # Mensagem de erro se não encontrar aluno ou turma

# Função para listar os alunos de uma turma específica
def consultar_alunos_por_turma(turma_rt):
    turma = session.query(Turma).filter_by(rt=turma_rt).first()  # Busca a turma pelo RT
    if turma:  # Se a turma for encontrada
        print(f'Alunos na turma {turma.rt} ({turma.ano} {turma.classe}):')  # Cabeçalho da lista
        for aluno in turma.alunos:  # Itera sobre os alunos da turma
            print(f' - {aluno.nome} (RA: {aluno.ra})')  # Imprime os dados de cada aluno
    else:
        print("Turma não encontrada.")  # Mensagem de erro se a turma não for encontrada

# Função para adicionar um professor ao banco de dados
def adicionar_professor(rp, nome):
    professor_existente = session.query(Professor).filter_by(rp=rp).first()  # Verifica se o professor já existe
    if not professor_existente:  # Se não existir, cria um novo professor
        professor = Professor(rp=rp, nome=nome)  # Cria um objeto Professor
        session.add(professor)  # Adiciona o professor à sessão
        session.commit()  # Confirma a transação no banco de dados
        print(f'Professor {nome} (RP: {rp}) adicionado com sucesso!')  # Mensagem de sucesso
    else:
        print("Professor já existe no sistema.")  # Mensagem de erro se o professor já estiver registrado

# Função para listar todos os professores cadastrados
def consultar_professores():
    professores = session.query(Professor).all()  # Recupera todos os professores da tabela
    if professores:  # Se houver professores cadastrados
        for professor in professores:
            print(f'Nome: {professor.nome}, RP: {professor.rp}')  # Imprime os dados de cada professor
    else:
        print("Ainda não há professores registrados no sistema.")  # Mensagem se não houver professores

# Função para associar um professor a uma turma
def adicionar_professor_a_turma(professor_rp, turma_rt):
    professor = session.query(Professor).filter_by(rp=professor_rp).first()  # Busca o professor pelo RP
    turma = session.query(Turma).filter_by(rt=turma_rt).first()  # Busca a turma pelo RT
    if professor and turma:  # Se ambos forem encontrados
        turma.professores.append(professor)  # Adiciona o professor à turma
        session.commit()  # Confirma a transação no banco de dados
        print(f'Professor {professor.nome} (RP: {professor.rp}) adicionado à turma {turma.rt}.')  # Mensagem de sucesso
    else:
        print("Professor ou Turma não encontrados.")  # Mensagem de erro se não encontrar professor ou turma

# Função para listar os professores de uma turma específica
def consultar_professor_por_turma(turma_rt):
    turma = session.query(Turma).filter_by(rt=turma_rt).first()  # Busca a turma pelo RT
    if turma:  # Se a turma for encontrada
        print(f'Professores da turma {turma.rt} ({turma.ano} {turma.classe}):')  # Cabeçalho da lista
        for professor in turma.professores:  # Itera sobre os professores da turma
            print(f' - {professor.nome} (RP: {professor.rp})')  # Imprime os dados de cada professor
    else:
        print("Turma não encontrada.")  # Mensagem de erro se a turma não for encontrada

# Função principal e menu de interação com o usuário
def main():
    while True:  # Loop para manter o menu ativo
        print('\nEscolha uma opção:')  # Exibe as opções disponíveis
        print("-----------------------------")
        print('1. Adicionar Aluno')  # Opção para adicionar aluno
        print('2. Adicionar Turma')  # Opção para adicionar turma
        print('3. Adicionar Professor')  # Opção para adicionar professor
        print("-----------------------------")
        print('4. Consultar Aluno')  # Opção para consultar alunos
        print('5. Consultar Turmas')  # Opção para consultar turmas
        print('6. Consultar Professor')  # Opção para consultar professores
        print("-----------------------------")
        print('7. Adicionar aluno a turma')  # Opção para adicionar aluno a uma turma
        print('8. Adicionar professor a turma')  # Opção para adicionar professor a uma turma
        print("-----------------------------")
        print('9. Consultar lista de alunos da turma')  # Opção para listar alunos de uma turma
        print('10. Consultar Professor por Turma')  # Opção para listar professores de uma turma
        print("-----------------------------")
        print('20. Sair')  # Opção para sair do programa

        opcao = input('Opção: ')  # Captura a opção escolhida pelo usuário

        # Processa a opção escolhida pelo usuário
        if opcao == '1' or opcao == 'Adicionar Aluno' or opcao == 'adicionar aluno' or opcao == 'Adicionar aluno':
            print("RA é o código identificador do Aluno")  
            ra = input('RA do Aluno: ')  # Captura o RA do aluno
            nome = input('Nome do Aluno: ')  # Captura o nome do aluno
            idade = int(input('Idade do Aluno: '))  # Captura a idade do aluno
            adicionar_aluno(ra, nome, idade)  # Chama a função para adicionar aluno

        elif opcao == '2' or opcao == 'Adicionar Turma' or opcao == 'Adicionar turma' or opcao == 'adicionar turma':
            print("RT é o código identificador da turma")
            rt = input('RT da Turma: ')  # Captura o RT da turma
            ano = input('Ano da Turma: ')  # Captura o ano da turma
            classe = input('Classe da Turma: ')  # Captura a classe da turma
            adicionar_turma(rt, ano, classe)  # Chama a função para adicionar turma

        elif opcao == '3' or opcao == 'Adicionar Professor' or opcao == 'Adicionar professor' or opcao == 'adicionar professor':
            print("RP é o código identificador do Professor")
            rp = input('RP do Professor: ')  # Captura o RP do professor
            nome = input('Nome do Professor: ')  # Captura o nome do professor
            adicionar_professor(rp, nome)  # Chama a função para adicionar professor

        elif opcao == '4' or opcao == 'Consultar Aluno' or opcao == 'Consultar aluno' or opcao == 'consultar aluno':
            print("Lista de Alunos:")
            consultar_alunos()  # Chama a função para consultar alunos

        elif opcao == '5' or opcao == 'Consultar Turma' or opcao == 'Consultar turma' or opcao == 'consultar turma':
            print("Lista de Turmas:")
            consultar_turmas()  # Chama a função para consultar turmas

        elif opcao == '6' or opcao == 'Consultar Professor' or opcao == 'Consultar professor' or opcao == 'consultar professor':
            print("Lista de Professores:")
            consultar_professores()  # Chama a função para consultar professores

        elif opcao == '7' or opcao == 'Adicionar Aluno a Turma' or opcao == 'Adicionar Aluno a turma' or opcao == 'Adicionar aluno a turma' or opcao == 'adicionar aluno a turma':
            aluno_ra = input('RA do Aluno: ')  # Captura o RA do aluno
            turma_rt = input('RT da Turma: ')  # Captura o RT da turma
            adicionar_aluno_a_turma(aluno_ra, turma_rt)  # Chama a função para adicionar aluno à turma

        elif opcao == '8' or opcao == 'Adicionar Professor a Turma' or opcao == 'Adicionar Professor a turma' or opcao == 'Adicionar professor a turma' or opcao == 'adicionar professor a turma':
            professor_rp = int(input('RP do Professor: '))  # Captura o RP do professor
            turma_rt = input('RT da Turma: ')  # Captura o RT da turma
            adicionar_professor_a_turma(professor_rp, turma_rt)  # Chama a função para adicionar professor à turma

        elif opcao == '9' or opcao == 'Consultar Lista de Alunos da Turma' or opcao == 'Consultar Lista de Alunos da turma' or opcao == 'Consultar Lista de alunos da turma' or opcao == 'consultar lista de alunos da turma':
            turma_rt = input('RT da Turma: ')  # Captura o RT da turma
            consultar_alunos_por_turma(turma_rt)  # Chama a função para listar alunos da turma

        elif opcao == '10' or opcao == 'Consultar Professor por Turma' or opcao == 'Consultar Professor por turma' or opcao == 'Consultar professor por Turma' or opcao == 'consultar professor por turma':
            turma_rt = input('RT da Turma: ')  # Captura o RT da turma
            consultar_professor_por_turma(turma_rt)  # Chama a função para listar professores da turma

        elif opcao == '20' or opcao == 'Sair' or opcao == 'sair':
            break  # Encerra o loop e o programa

        else:
            print("Opção inválida. Tente novamente.")  # Mensagem para opção inválida

# Executa a função principal ao iniciar o programa
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar a interação com o usuário
