from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base     
from sqlalchemy.exc import OperationalError      

engine = create_engine('sqlite:///biblioteca.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Diciplina(Base):
    __tablename__ = "diciplinas"

    id = Column(Integer, primary_key=True)
    nome = Column(String)

    def __repr__(self):
        return f'<Diciplina(nome={self.nome}, ID={self.id})>'
    
    
    def adicionar_diciplina(nome):
        Diciplina = session.query(Diciplina).filter_by(nome=nome).first()
        if not Diciplina:
            Diciplina = Diciplina(nome=nome)
            session.add(Diciplina)
            session.commit()

    
    def consultar_diciplina():
        try:
            diciplinas = session.query(Diciplina).all()
            if diciplinas:
                for Diciplina in diciplinas:
                    print(Diciplina.nome)
            else:
                print("Ainda não possuí professor registrado no sistema.")
        except OperationalError:
            print("Tabela de professores não existe ainda. Por favor, adicione um professor primeiro.")
        
def main():
    # Garante que as tabelas sejam criadas antes de iniciar as operações
    Base.metadata.create_all(engine)

    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar Diciplina')
        print('2. Consultar Diciplina')
        print('3. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            nome = input('Nome do Diciplina: ')
            Diciplina.adicionar_diciplina(nome)
        elif opcao == '2':
            Diciplina.consultar_diciplina()
        elif opcao == '3':
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()
