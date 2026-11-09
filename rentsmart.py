import csv

class Imovel:
    """Representa um imóvel e calcula o aluguel com adicionais e desconto."""
    def __init__(self, tipo, quartos=1, vaga_garagem=False, vagas_estudio=2,
                 sem_criancas=False):
        self.tipo = tipo
        self.quartos = quartos
        self.vaga_garagem = vaga_garagem
        self.vagas_estudio = vagas_estudio
        self.sem_criancas = sem_criancas

    def calcular_aluguel(self):
        if self.tipo == "apartamento":
            valor = 700
            if self.quartos == 2:
                valor += 200
            if self.vaga_garagem:
                valor += 300
            if self.sem_criancas:
                valor *= 0.95
        elif self.tipo == "casa":
            valor = 900
            if self.quartos == 2:
                valor += 250
            if self.vaga_garagem:
                valor += 300
        elif self.tipo == "estudio":
            valor = 1200
            # O pacote inicial de duas vagas custa R$ 250.
            valor += 250
            if self.vagas_estudio > 2:
                valor += (self.vagas_estudio - 2) * 60
        else:
            raise ValueError("Tipo de imóvel inválido.")
        return round(valor, 2)


class Orcamento:
    """Reúne os valores do aluguel e da taxa contratual."""
    TAXA_CONTRATUAL = 2000

    def __init__(self, imovel, parcelas):
        if not 1 <= parcelas <= 5:
            raise ValueError("A taxa contratual pode ser dividida em 1 a 5 parcelas.")
        self.imovel = imovel
        self.parcelas = parcelas

    def taxa_por_parcela(self):
        return round(self.TAXA_CONTRATUAL / self.parcelas, 2)

    def exibir_resumo(self):
        aluguel = self.imovel.calcular_aluguel()
        print("\\n===== RENTSMART | ORÇAMENTO =====")
        print(f"Tipo de imóvel: {self.imovel.tipo.title()}")
        print(f"Aluguel mensal: R$ {aluguel:.2f}")
        print(f"Taxa contratual: R$ {self.TAXA_CONTRATUAL:.2f}")
        print(f"Parcelamento: {self.parcelas}x de R$ {self.taxa_por_parcela():.2f}")
        print("Total no primeiro mês: R$ {:.2f}".format(aluguel + self.taxa_por_parcela()))
        print("=================================")

    def gerar_csv(self, nome_arquivo="projecao_12_meses.csv"):
        aluguel = self.imovel.calcular_aluguel()
        taxa_parcela = self.taxa_por_parcela()
        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mês", "Aluguel (R$)", "Taxa contratual (R$)", "Total previsto (R$)"])
            for mes in range(1, 13):
                taxa = taxa_parcela if mes <= self.parcelas else 0
                escritor.writerow([mes, f"{aluguel:.2f}", f"{taxa:.2f}", f"{aluguel + taxa:.2f}"])
        print(f"Arquivo '{nome_arquivo}' gerado com sucesso.")


def pedir_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def main():
    print("RentSmart - Sistema de Orçamento de Locação")
    print("1 - Apartamento\\n2 - Casa\\n3 - Estúdio")
    opcao = pedir_inteiro("Escolha o tipo de imóvel: ", 1, 3)
    tipo = {1: "apartamento", 2: "casa", 3: "estudio"}[opcao]

    quartos = 1
    vaga = False
    vagas_estudio = 2
    sem_criancas = False

    if tipo in ("apartamento", "casa"):
        quartos = pedir_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        vaga = input("Deseja vaga de garagem? (s/n): ").strip().lower() == "s"
    else:
        vagas_estudio = pedir_inteiro("Quantidade de vagas no estúdio (mínimo 2): ", 2, 20)

    if tipo == "apartamento":
        sem_criancas = input("Não possui crianças? (s/n): ").strip().lower() == "s"

    parcelas = pedir_inteiro("Em quantas parcelas pagar a taxa (1 a 5)? ", 1, 5)

    imovel = Imovel(tipo, quartos, vaga, vagas_estudio, sem_criancas)
    orcamento = Orcamento(imovel, parcelas)
    orcamento.exibir_resumo()
    orcamento.gerar_csv()


if __name__ == "__main__":
    main()
