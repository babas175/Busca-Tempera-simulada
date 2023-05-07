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
        self.solucao = self.gerar_solucao_inicial_aleatoria() if solucao is None else solucao
    
    def buscar_solucao(self) -> list[Solucao]:
        solucao_list = [self.solucao] # Adiciona a solução atual à lista de soluções
        iteracao = self.solucao.iteracao + 1 # Incrementa a iteração
        melhor_qualidade = self.solucao.qualidade # Salva a melhor qualidade atual
        caminho_atual = self.solucao.ciclo[:] # Salva o caminho atual
        i_inicial, j_inicial = 0, 1  # Define os índices iniciais para a busca na vizinhança
        temperatura = self.solucao.custo * self.parametro_mandato  # Define a temperatura inicial
        alpha = 0.95 # Define o parâmetro de resfriamento

        
        while time.time() < self.tempo_limite:  # Enquanto o tempo limite não for atingido
            vizinho = self.vizinhanca.proximo_vizinho(self.solucao, i_inicial, j_inicial)  # Obtém o próximo vizinho a ser avaliado
            iteracao += 1  # Incrementa a iteração
            delta = vizinho.custo - self.solucao.custo  # Calcula a diferença de custo entre a solução atual e o vizinho

            if delta < 0:  # Se o vizinho for melhor que a solução atual
                self.solucao = vizinho  # Define o vizinho como a nova solução
                caminho_atual = self.solucao.ciclo[:]  # Atualiza o caminho atual
                if self.solucao.custo < melhor_qualidade:  # Se a nova solução for melhor que a melhor qualidade atual
                    melhor_qualidade = self.solucao.custo  # Atualiza a melhor qualidade atual
                solucao_list.append(self.solucao)  # Adiciona a nova solução à lista de soluções

            else:  # Se o vizinho não for melhor que a solução atual
                if temperatura == 0:  # Se a temperatura atingir o valor mínimo
                    return [self.solucao]  # Retorna a solução atual como a melhor solução encontrada
                
                p_aceitacao = math.exp(-delta/temperatura) # Calcula a probabilidade de aceitação do vizinho com base na temperatura e na variação da qualidade
                if random.random() < p_aceitacao:
                    self.solucao = vizinho # Aceita o vizinho como a nova solução atual
                    caminho_atual = self.solucao.ciclo[:]
                    solucao_list.append(self.solucao) # Adiciona a solução atual à lista de soluções

            i_inicial = (i_inicial + 1) % (len(caminho_atual) - 1)  # Atualiza os índices iniciais para a busca na vizinhança
            if i_inicial == 0:
                j_inicial += 1  # Incrementa o índice de coluna para a busca na vizinhança
                
                if j_inicial == len(caminho_atual): # Se o índice de coluna chegar ao final do caminho atual
                    j_inicial = 1  # Reinicia o índice de coluna para o começo do caminho atual


            temperatura = temperatura * alpha # Atualiza a temperatura

        return solucao_list # retorna a lista de 
