import threading
import random
import time
import os

ranking = []
estado = []

# barra de progresso
def barra(dist, tamanho=20):
    progresso = int((dist / 100) * tamanho)
    return "█" * progresso + "-" * (tamanho - progresso)

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def corredor(id, nome):
    distancia = 0

    while distancia < 100:
        passo = random.randint(1, 10)

        # eventos aleatórios
        evento = random.random()
        msg = ""

        if evento < 0.2:
            msg = "⚠️ Tropeçou "
            passo = 0
        elif evento < 0.35:
            msg = "🚀 Bônus de aceleração"
            passo *= 2

        distancia += passo
        distancia = min(distancia, 100)

        # ATUALIZA ESTADO (modo painel)
        estado[id] = (nome, distancia, msg)

        # THREADS EXECUTANDO COM PARALELISMO (VISUALIZAÇÃO MAIS CAÓTICA)
        #Para usar o painel de ranking, comentar essa linha
        #print(f"{nome:12} -> {distancia}m {msg}")

        time.sleep(random.uniform(0.4, 0.9))

    ranking.append(nome)

# painel (uma linha por corredor)
def painel(nomes):
    while len(ranking) < len(nomes):
        limpar()
        print("🏁 CORRIDA DE THREADS\n")

        for nome, dist, msg in estado:
            print(f"{nome:12} |{barra(dist)}| {dist:3d}m {msg}")

        time.sleep(0.2)

# entrada do usuário
qtd = int(input("Quantos corredores deseja? "))

threads = []
nomes = [f"Corredor {i+1}" for i in range(qtd)]

# estado inicial
estado = [(nome, 0, "") for nome in nomes]

print("\n🏁 Corrida iniciada!\n")

# cria e inicia threads
for i, nome in enumerate(nomes):
    t = threading.Thread(target=corredor, args=(i, nome))
    threads.append(t)
    t.start()

#Descomentar para o painel funcionar
painel_thread = threading.Thread(target=painel, args=(nomes,))
painel_thread.start()

# espera threads terminarem
for t in threads:
    t.join()

#Descomentar para o painel funcionar
painel_thread.join()

# resultado final
print("\n🏆 RESULTADO FINAL:\n")
for i, nome in enumerate(ranking):
    medalhas = ["🥇", "🥈", "🥉"]
    pos = medalhas[i] if i < 3 else f"{i+1}º"
    print(f"{pos} {nome}")

print("\n🏁 Corrida finalizada!")
