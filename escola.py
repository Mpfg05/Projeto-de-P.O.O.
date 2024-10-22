from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Criação do engine e da sessão
engine = create_engine('sqlite:///biblioteca.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)  # A coluna id
    nome = Column(String)                     # Nome do aluno
    idade = Column(Integer)                   # Idade do aluno

    def __repr__(self):
        return f'<Aluno(nome={self.nome}, idade={self.idade})>'


class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True)  # A coluna id
    ano = Column(String)                     # ano (ex: '7')
    classe = Column(String)                  # letra da turma (ex: 'A')

    def __repr__(self):
        return f'<Turma(ano={self.ano}, classe={self.classe})>'

# Criação das tabelas
Base.metadata.create_all(engine)

def adicionar_aluno(nome, idade):
    novo_aluno = Aluno(nome=nome, idade=idade)
    session.add(novo_aluno)
    session.commit()
    print(f'Aluno {nome} (idade: {idade}) adicionado com sucesso!')

def consultar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f'Nome: {aluno.nome}, Idade: {aluno.idade}')

def adicionar_turma(ano, classe):
    nova_turma = Turma(ano=ano, classe=classe)
    session.add(nova_turma)
    session.commit()
    print(f'Turma {ano} (classe: {classe}) adicionada com sucesso!')

def consultar_turmas():
    turmas = session.query(Turma).all()
    for turma in turmas:
        print(f'Ano: {turma.ano}, Classe: {turma.classe}')  # Correção aqui

def main():
    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar Aluno')
        print('2. Consultar Alunos')
        print('3. Adicionar Turma')
        print('4. Consultar Turmas')
        print('5. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            nome = input('Nome do Aluno: ')
            idade = int(input('Idade do Aluno: '))
            adicionar_aluno(nome, idade)
        elif opcao == '2':
            print("Lista de Alunos:")
            consultar_alunos()
        elif opcao == '3':
            ano = input('Ano da Turma: ')
            classe = input('Classe da Turma: ')
            adicionar_turma(ano, classe)
        elif opcao == '4':
            print("Lista de Turmas:")
            consultar_turmas()
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
]
