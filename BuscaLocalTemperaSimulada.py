from AlgoritmoBusca import AlgoritmoBusca
import time
from Vizinhanca import Vizinhanca
from Vizinhanca2opt import Vizinhanca2opt
from Solucao import Solucao
import random
import math

class BuscaLocalTemperaSimulada(AlgoritmoBusca):
    def __init__(self,vizinhanca:Vizinhanca, solucao_otima, parametro_mandato, solucao: Solucao = None):
        super().__init__("BTS"+vizinhanca.nome, vizinhanca.distancias, solucao_otima)
        self.parametro_mandato = parametro_mandato
        self.vizinhanca = vizinhanca
        if solucao is None:
            self.solucao = self.gerar_solucao_inicial_aleatoria()
        else:
            self.solucao = solucao
    
    def buscar_solucao(self) -> list[Solucao]:
        solucao_list = [self.solucao]
        iteracao = self.solucao.iteracao + 1  #A variável iteracao armazena o número de iterações realizadas durante a busca;
        melhor_qualidade = self.solucao.qualidade #A variável melhor_qualidade guarda a qualidade da melhor solução encontrada até o momento;
        caminho_atual = self.solucao.caminho[:] #A variável caminho_atual armazena a lista de cidades visitadas na ordem atual;
        i_inicial = 0 #As variáveis i_inicial e j_inicial são utilizadas para controlar a escolha da vizinhança;
        j_inicial = 1
        temperatura = self.solucao.custo * self.parametro_mandato #A variável temperatura é iniciada com o custo da solução inicial multiplicado por um parâmetro de mandato;
        alpha = 0.95  #A variável alpha é utilizado para controlar a diminuição da temperatura em cada iteração;

        while time.time() < self.tempo_limite: #O loop principal executa a busca até que o tempo limite seja atingido;
            vizinho = self.vizinhanca.proximo_vizinho(self.solucao, i_inicial, j_inicial)
            iteracao += 1 #A cada iteração, é gerada uma nova solução na vizinhança da solução atual;
            delta = vizinho.custo - self.solucao.custo #A variável delta_custo é a diferença entre o custo da solução atual e o custo da solução gerada pela vizinhança;

            if delta < 0: #Se delta_custo for negativo, a solução gerada pela vizinhança é melhor do que a solução atual e é aceita como a nova solução. 
                self.solucao = vizinho
                caminho_atual = self.solucao.caminho[:]
                if self.solucao.custo < melhor_qualidade:
                    melhor_qualidade = self.solucao.custo
                solucao_list.append(self.solucao)

            else: #Se delta_custo for positivo, a solução gerada pela vizinhança é aceita como a nova solução com uma certa probabilidade.
                p_aceitacao = math.exp(-delta/temperatura)
                if random.random() < p_aceitacao:
                    self.solucao = vizinho
                    caminho_atual = self.solucao.caminho[:]
                    solucao_list.append(self.solucao)

            i_inicial += 1
            if i_inicial == len(caminho_atual) - 1:
                i_inicial = 0
                j_inicial += 1
                if j_inicial == len(caminho_atual):
                    j_inicial = 1

            temperatura = temperatura * alpha #A temperatura é atualizada a cada iteração, multiplicando-a pelo fator alpha;

        return solucao_list #Ao final da busca, a lista de soluções encontradas é retornada.


#A variável iteracao armazena o número de iterações realizadas durante a busca;
#A variável melhor_qualidade guarda a qualidade da melhor solução encontrada até o momento;
#A variável caminho_atual armazena a lista de cidades visitadas na ordem atual;
#As variáveis i_inicial e j_inicial são utilizadas para controlar a escolha da vizinhança;
#A variável temperatura é iniciada com o custo da solução inicial multiplicado por um parâmetro de mandato;
#A variável alpha é utilizado para controlar a diminuição da temperatura em cada iteração;
#O loop principal executa a busca até que o tempo limite seja atingido;
#A cada iteração, é gerada uma nova solução na vizinhança da solução atual;
#A variável delta_custo é a diferença entre o custo da solução atual e o custo da solução gerada pela vizinhança;
#Se delta_custo for negativo, a solução gerada pela vizinhança é melhor do que a solução atual e é aceita como a nova solução. A solução atual é atualizada, o caminho atual é atualizado, e se a nova solução for melhor do que a melhor solução encontrada até o momento, a variável melhor_qualidade é atualizada. A nova solução é adicionada à lista de soluções encontradas;
#Se delta_custo for positivo, a solução gerada pela vizinhança é aceita como a nova solução com uma certa probabilidade. A probabilidade de aceitação é calculada com base na temperatura e no delta_custo. A nova solução é adicionada à lista de soluções encontradas apenas se for aceita;
#A temperatura é atualizada a cada iteração, multiplicando-a pelo fator alpha;
#Ao final da busca, a lista de soluções encontradas é retornada.