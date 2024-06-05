import random
import json
import os
from threading import Thread
def numgen(limiteSuperior, qtdCombinacoes, id):
    combinacoesAtuais = []
    with open(f'combinacoes-{id}.txt', 'w') as f:
        while len(combinacoesAtuais) != limiteSuperior:    
            combinacao = set()
            while len(combinacao) != qtdCombinacoes:
                combinacao.add(random.randint(1, 26))
            if combinacao not in combinacoesAtuais:
                combinacoesAtuais.append(combinacao)
        print(combinacoesAtuais)
        f.write(str(combinacoesAtuais))

if __name__ == '__main__':
    a = Thread(target=numgen, args=(1000, 15, 1))
    b = Thread(target=numgen, args=(1000, 14, 2))
    c = Thread(target=numgen, args=(1000, 13, 3))
    d = Thread(target=numgen, args=(1000, 12, 4))
    e = Thread(target=numgen, args=(1000, 11, 5))

    for x in [a,b,c,d,e]:
        x.start()
    
    for x in [a,b,c,d,e]:
        x.join()