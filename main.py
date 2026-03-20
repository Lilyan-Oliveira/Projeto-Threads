import threading
import random
import time
import os

estado = {}
posicoes = []
lock = threading.Lock()

def barra(dist, tamanho=20):
    prog = int((dist / 100) * tamanho)
    return "█" * prog + "-" * (tamanho - prog)

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def corredor(nome):
    dist = 0

    while dist < 100:
        passo = random.randint(1, 10)

        evento = random.choice(["normal", "tropecou", "boost"])

        if evento == "tropecou":
            msg = "⚠️ Tropeçou"
            passo = 0

        elif evento == "boost":
            msg = "🚀 Boost"
            passo = random.randint(1, 5)

        else:
            msg = ""

        dist += passo
        dist = min(dist, 100)

        with lock:
            estado[nome] = (msg, dist)

        time.sleep(random.uniform(0.8, 1.5))

    with lock:
        estado[nome] = ("🏁 Finalizou", dist)
        posicoes.append(nome)

def painel(nomes):
    while True:
        limpar()
        print("🏁 CORRIDA EM TEMPO REAL\n")

        with lock:
            for nome in nomes:
                status, dist = estado.get(nome, ("...", 0))
                print(f"{nome:12} |{barra(dist)}| {dist:3d}m  {status}")

            finalizados = len(posicoes)

        if finalizados == len(nomes):
            break

        time.sleep(0.2)

# Corredores
nomes = [f"Corredor {c}" for c in ["A", "B", "C", "D"]]

threads = []

for nome in nomes:
    estado[nome] = ("Largando...", 0)
    t = threading.Thread(target=corredor, args=(nome,))
    threads.append(t)
    t.start()

# Painel
painel_thread = threading.Thread(target=painel, args=(nomes,))
painel_thread.start()

for t in threads:
    t.join()

painel_thread.join()

# Resultado final
print("\n🏆 RESULTADO FINAL:\n")
for i, nome in enumerate(posicoes):
    medalhas = ["🥇", "🥈", "🥉"]
    pos = medalhas[i] if i < 3 else f"{i+1}º"
    print(f"{pos} {nome}")

print("\n🏁 Corrida finalizada!")