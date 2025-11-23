import random #Importa random, Tuple, Optional, Tabuleiro, e Jogador
from typing import Tuple, Optional
from tabuleiro import Tabuleiro
from jogador import Jogador

class Jogo(): #Define a classe "Jogo" que comanda o estado principal do jogo
    tab: 'Tabuleiro' #Atributo para Tabuleiro e jogadores, inicialmente como None
    jogador1: Optional['Jogador'] = None
    jogador2: Optional['Jogador'] = None
    quemJoga: Optional['Jogador'] = None

    def __init__(self) -> None: #Define o método construtor 
        self.tab = Tabuleiro() #Inicializa o tabuleiro
    
    def menu_jogo(self) -> None: #Define o método para o menu do jogo e definição dos jogadores
        print("Bem-vindo ao Connect Four (Quatro em Linha)!")
        
        while True:
            try: #Inicia o try para lidar com erros do input do usuário
                modo = int(input("Escolha o modo de jogo (1: Humano x Humano, 2: Humano x Computador): ")) #Input do usuário
                modos_aceitos = {
                    1: ('Humano X', 'humano', 'Humano O', 'humano'),
                    2: ('Humano X', 'humano', 'Computador O', 'computador')}
                if modo not in modos_aceitos: #Localiza o erro e o define
                    raise ValueError('Opção inválida')
                print(f'Iniciando partida {modos_aceitos[modo]}')
                setup = modos_aceitos[modo]
                self.jogador1 = Jogador(setup[0], 'X', setup[1]) #Cria o jogador1
                self.jogador2 = Jogador(setup[2], 'O', setup[3]) #Cria o jogador2
                print(f"\nPartida iniciada: {self.jogador1.nome} ('X') vs {self.jogador2.nome} ('O')")
                break
            except ValueError as e:
                print(f'Erro {e}. Tente Novamente')
    
    def obter_jogada(self) -> Tuple[int,int]: #Método que retorna as coordenadas da jogada
        jogador = self.quemJoga #Obtém o jogador da vez
        if jogador is None: #Identifica erro na lógica do jogo
            raise ValueError("Erro de lógica: jogador atual não pode ser None no turno.")
        
        if jogador.tipo == 'humano': #Caso adversário seja humano
            while True:
                try: #Bloco para identificar invalidez no input do usuário
                    coluna =  int(input(f'Vez de {jogador.nome}. Escolha uma coluna livre'))
                    if not (0 <= coluna < self.tab.NUM_COLUNAS): #Identifica erro caso a coluna escolhida esteja fora do intervalo
                        print("Erro: Coluna fora do intervalo (0 a 6). Tente novamente.")
                        continue
                    linha_livre = self.tab.obter_linha_livre(coluna) #Chama método do Tabuleiro para achar a primeira linha livre da coluna escolhida
                    if linha_livre == -1: #Determina se a coluna está cheia
                        print('Essa coluna está preenchida. Digite outra coluna')
                        continue

                    return linha_livre,coluna
                except ValueError:
                    print('Entrada inválida, por favor digite um número de 0 a 6')
        elif jogador.tipo == 'computador': #Caso adversário seja computador
            while True:
                coluna = random.randrange(0, self.tab.NUM_COLUNAS) #Escolhe uma coluna aleatória dentro do intervalo
                linha_livre = self.tab.obter_linha_livre(coluna) #Verifica a linha livre da coluna escolhida
                if linha_livre != -1:
                    break
            print(f'A Máquina escolheu {linha_livre}, {coluna}')
            return linha_livre, coluna
        return -1, -1 #Linha de segurança caso o tipo de jogador seja desconhecido
    
    def iniciar_partida(self) -> None: #Método que inicia o loop principal do jogo
        self.quemJoga = self.jogador1 #jogador1 joga primeiro 
        while True:
            jogador_atual = self.quemJoga
            if jogador_atual is None: #Identifica erro de lógica do jogo (caso não haja jogador)
                print(f'Não é possível jogar sem jogador, saindo do programa...')
                break
            self.tab.mostrar_tabuleiro() #Mostra o estado atual do tabuleiro
            print(f"\n--- Turno de {jogador_atual.nome} ({jogador_atual.peca}) ---")
            linha_livre, coluna = self.obter_jogada() #Chama o método para obter as coordenadas da jogada
            self.tab.fazer_jogada(linha_livre, coluna, jogador_atual.peca) #Chama o método Tabuleiro para colocar a peça na poisção desejada
            if self.tab.verificar_vitoria(linha_livre, coluna, jogador_atual.peca): #Verifica se a jogada resultou em vitória
                self.tab.mostrar_tabuleiro() #Mostra o tabuleiro final
                print(f'Vitória de {jogador_atual}, parabéns!')
                break
            if self.tab.tabuleiro_cheio(): #Identifica empate do jogo
                print(f'O jogo empatou, parabéns ao dois... Ou não!')
                break

            self.quemJoga = self.jogador2 if jogador_atual == self.jogador1 else self.jogador1 #Troca a vez do jogador
            

                    
                    

if __name__ == "__main__": #Bloco padrão de Python que garante que o código dentro dele só será executado quando o arquivo for rodado diretamente
    try:
        jogo = Jogo() 
        jogo.menu_jogo()
        jogo.iniciar_partida()
    except KeyboardInterrupt:
        print("\n\nJogo encerrado. Até mais!")

