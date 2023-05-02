from AlgoritmoBusca import AlgoritmoBusca
import time
from Vizinhanca import Vizinhanca
from Vizinhanca2opt import Vizinhanca2opt
from Solucao import Solucao


class BuscaLocalTemperaSimulada(AlgoritmoBusca):
    def __init__(self,vizinhanca2opt:Vizinhanca2opt, solucao_otima, parametro_mandato, solucao: Solucao = None):
        super().__init__("BTS"+vizinhanca2opt.nome, vizinhanca2opt.distancias, solucao_otima)
        self.parametro_mandato = parametro_mandato
        self.vizinhanca2opt = vizinhanca2opt.proximo_vizinho
        if solucao is None:
            self.solucao = self.gerar_solucao_inicial_aleatoria()
        else:
            self.solucao = solucao
    
    def buscar_solucao(self) -> list[Solucao]:
        solucao_list = [self.solucao]
        iteracao = self.solucao.iteracao + 1
        melhor_qualidade = self.solucao.qualidade
        initial_temp = 1
        alpha = 0.01


