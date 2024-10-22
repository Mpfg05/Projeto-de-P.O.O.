#classe alunos
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

# Criação da tabela
Base.metadata.create_all(engine)

def adicionar_aluno(nome, idade):
    novo_aluno = Aluno(nome=nome, idade=idade)  # Corrigido para receber nome
    session.add(novo_aluno)
    session.commit()
    print(f'Aluno {nome} (idade: {idade}) adicionado com sucesso!')

def consultar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f'Nome: {aluno.nome}, Idade: {aluno.idade}')  # Impressão formatada

def main():
    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar Aluno')
        print('2. Consultar Alunos')
        print('3. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            nome = input('Nome do Aluno: ')
            idade = int(input('Idade do Aluno: '))  # Solicita a idade do aluno
            adicionar_aluno(nome, idade)  # Passa o nome e a idade
        elif opcao == '2':
            print("Lista de Alunos:")
            consultar_alunos()
        elif opcao == '3':
           break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

