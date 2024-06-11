from itertools import combinations
import random
import pandas
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
import os
from typing import List

os.environ["INVOICE_LANG"] = "pt_BR"

def generate_all_combinations(n:List[int], p:int) -> List[List[int]]:
    """
    Gera todas as combinações possíveis de um conjunto de números n com p elementos em cada combinação (PROGRAMA 1)

    Args:
    n: List[int]: Lista de números
    p: int: Número de elementos em cada combinação

    Returns:
    List[List[int]]: Lista de combinações
    """
    print(f"Generating all combinations of length {p}")
    return list(combinations(n, p))

def get_random_points(list_of_combos:List[int]) -> int:
    """
    Gera pontos aleatórios dentro da lista para a simulação de Monte Carlo

    Args:
    list_of_combos: List[int]: Lista de combinações

    Returns:
    int: Ponto aleatório
    """
    return random.randint(0, len(list_of_combos)-1)

def check_combo(list_of_combos_large:List[int], list_of_combos_small:List[int], max_sims:int) -> List[int]:
    """
    Função Monte Carlo para encontrar o subconjunto de S15 que contém todas as sequências de S14

    Args:
    list_of_combos_large: List[int]: Lista de combinações grandes
    list_of_combos_small: List[int]: Lista de combinações pequenas
    max_sims: int: Número máximo de simulações

    Returns:
    List[int]: Lista de subconjuntos
    """
    subset_list = []
    for number_of_sim in range(1,max_sims):
        subset_list = check_for_subset(list_of_combos_large, list_of_combos_small, number_of_sim, subset_list)
    return subset_list

def check_for_subset(list_large:List[int], list_small:List[int], number_of_sim:int, subset_list:List[int]) -> List[int]:
    """
    Verifica se a combinação pequena está contida na combinação grande

    Args:
    list_large: List[int]: Lista de combinações grandes
    list_small: List[int]: Lista de combinações pequenas
    number_of_sim: int: Número de simulações
    subset_list: List[int]: Lista de subconjuntos

    Returns:
    List[int]: Lista de subconjuntos
    """
    for _ in range(1,number_of_sim):
        checkpoint_bigger = get_random_points(list_large)
        checkpoint_smaller = get_random_points(list_small)
        is_subset = set(list_small[checkpoint_smaller]).issubset(set(list_large[checkpoint_bigger]))
        if is_subset:
            if list_large[checkpoint_bigger] not in subset_list:
                subset_list.append(list_large[checkpoint_bigger])
    return subset_list

if __name__ == '__main__':
    numbers = list(range(1, 26))
    lengths = [15, 14, 13, 12, 11]
    all_combinations = [generate_all_combinations(numbers, length) for length in lengths]

    subset_15_14 = check_combo(all_combinations[0], all_combinations[1], 50000)
    pandas.DataFrame(subset_15_14, columns=list(range(1,16))).to_excel("subset_15_14.xlsx", index=False)
    print(f"Subset found in attempts {len(subset_15_14)}")

    subset_15_13 = check_combo(all_combinations[0], all_combinations[2], 50000)
    pandas.DataFrame(subset_15_13, columns=list(range(1,16))).to_excel("subset_15_13.xlsx", index=False)
    print(f"Subset found: {len(subset_15_13)}")

    subset_15_12 = check_combo(all_combinations[0], all_combinations[3], 50000)
    pandas.DataFrame(subset_15_12, columns=list(range(1,16))).to_excel("subset_15_12.xlsx", index=False)
    print(f"Subset found: {len(subset_15_12)}")

    subset_15_11 = check_combo(all_combinations[0], all_combinations[4], 50000)
    pandas.DataFrame(subset_15_11, columns=list(range(1,16))).to_excel("subset_15_11.xlsx", index=False)
    print(f"Subset found: {len(subset_15_11)}")


    all_subsets = [(subset_15_14, 'S_15_14'), (subset_15_13, 'S_15_13'), (subset_15_12, 'S_15_12'), (subset_15_11, 'S_15_11')]
    for subset in all_subsets:
        pandas.DataFrame(subset[0]).to_excel(f"{subset[1]}.xlsx", index=False)

    empresa = Client('Loterias Scala', 'Rua Imaculada Conceição, 1155', 'Curitiba', 'PR', '80215-901', 'Brazil', '123456789', logo_filename='Loterias Caixa.png')
    fornecedor = Provider('Loterias Caixa', bank_account='260152-8', logo_filename='Loterias Caixa.png')
    criador = Creator('Loterias Scala', )
    invoice = Invoice(empresa, fornecedor, criador)

    invoice.currency = 'R$'
    invoice.add_item(Item(count=len(subset_15_14), price = 3.00, description='Jogo LotoFácil com 14 números', unit='x'))
    invoice.add_item(Item(count=len(subset_15_13), price = 3.00, description='Jogo LotoFácil com 13 números', unit='x'))
    invoice.add_item(Item(count=len(subset_15_12), price = 3.00, description='Jogo LotoFácil com 12 números', unit='x'))
    invoice.add_item(Item(count=len(subset_15_11), price = 3.00, description='Jogo LotoFácil com 11 números', unit='x'))
    pdf = SimpleInvoice(invoice)
    pdf.gen("invoice.pdf", generate_qr_code=True)








