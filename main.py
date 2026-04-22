import threading
import random
import time
import os

ranking = []
estado = []
tempos_execucao = {}

lock_hidratacao = threading.Lock()
fila_hidratacao = []
fila_lock = threading.Lock()

PONTO_HIDRATACAO = 50

# escolha do algoritmo
while True:
    print("Escolha o algoritmo de hidratação:")
    print("1 - FCFS (ordem de chegada)")
    print("2 - SJF (menor tempo primeiro)")

    opcao = input("Digite 1 ou 2: ")

    if opcao == "1":
        ALGORITMO = "FCFS"
        break
    elif opcao == "2":
        ALGORITMO = "SJF"
        break
    else:
        print("Opção inválida!\n")

# barra com ponto de hidratação
def barra(dist, tamanho=20):
    progresso = int((dist / 100) * tamanho)
    pos_hidratacao = int((PONTO_HIDRATACAO / 100) * tamanho)

    barra_str = ""

    for i in range(tamanho):
        if i == pos_hidratacao:
            barra_str += "|"
        elif i < progresso:
            barra_str += "█"
        else:
            barra_str += "-"

    return barra_str

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def corredor(id, nome):
    inicio = time.time()

    distancia = 0
    hidratou = False
    tempo_hidratacao = random.randint(2, 5)

    while distancia < 100:
        passo = random.randint(1, 10)

        evento = random.random()
        msg = ""

        if evento < 0.2:
            msg = "⚠️ Tropeçou"
            passo = 0
        elif evento < 0.35:
            msg = "🚀 Acelerou"
            passo *= 2

        distancia += passo
        distancia = min(distancia, 100)

        # 💧 ponto de hidratação
        if distancia >= PONTO_HIDRATACAO and not hidratou:
            msg = "💧 Chegou no ponto de hidratação"

            with fila_lock:
                fila_hidratacao.append((nome, tempo_hidratacao))

                if ALGORITMO == "SJF":
                    fila_hidratacao.sort(key=lambda x: x[1])

            # esperando na fila
            while True:
                with fila_lock:
                    if fila_hidratacao[0][0] == nome:
                        break
                estado[id] = (nome, distancia, "⏳ Esperando para hidratar")
                time.sleep(0.2)

            # região crítica
            with lock_hidratacao:
                for i in range(tempo_hidratacao, 0, -1):
                    estado[id] = (nome, distancia, f"💧 Hidratando ({i}s) - PARADO")
                    time.sleep(1)

            with fila_lock:
                fila_hidratacao.pop(0)

            hidratou = True

        estado[id] = (nome, distancia, msg)

        # THREADS EXECUTANDO COM PARALELISMO (VISUALIZAÇÃO MAIS CAÓTICA)
        # Para usar esse modo, descomente a linha abaixo e comente o painel
        # print(f"{nome:12} -> {distancia}m {msg}")

        time.sleep(random.uniform(0.4, 0.9))
        time.sleep(0.4)

    fim = time.time()
    tempos_execucao[nome] = fim - inicio

    ranking.append(nome)

# painel
def painel(nomes):
    while len(ranking) < len(nomes):
        limpar()
        print(f"🏁 CORRIDA COM HIDRATAÇÃO ({ALGORITMO})")
        print(f"📍 Ponto de hidratação: {PONTO_HIDRATACAO}m\n")

        for nome, dist, msg in estado:
            print(f"{nome:12} |{barra(dist)}| {dist:3d}m {msg}")

        print("\nFila hidratação:", [n for n, _ in fila_hidratacao])

        time.sleep(0.2)

# entrada
qtd = int(input("\nQuantos corredores deseja? "))

threads = []
nomes = [f"Corredor {i+1}" for i in range(qtd)]

estado = [(nome, 0, "") for nome in nomes]

print("\n🏁 Corrida iniciada!\n")

# ⏱️ INÍCIO DO TEMPO
inicio = time.time()

# ⏱️ INÍCIO DO TEMPO
inicio = time.time()

for i, nome in enumerate(nomes):
    t = threading.Thread(target=corredor, args=(i, nome))
    threads.append(t)
    t.start()

# iniciar painel
painel_thread = threading.Thread(target=painel, args=(nomes,))
painel_thread.start()

for t in threads:
    t.join()

painel_thread.join()

# ⏱️ FIM DO TEMPO
fim = time.time()
tempo_total = fim - inicio

# ⏱️ FIM DO TEMPO
fim = time.time()
tempo_total = fim - inicio

# resultado
print("\n🏆 RESULTADO FINAL (ORDEM DE CHEGADA):\n")
for i, nome in enumerate(ranking):
    medalhas = ["🥇", "🥈", "🥉"]
    pos = medalhas[i] if i < 3 else f"{i+1}º"
    tempo = tempos_execucao[nome]
    print(f"{pos} {nome} - Tempo total: {tempo:.2f}s")

print("\n⚡ RANKING POR DESEMPENHO (MENOR TEMPO):\n")

ranking_tempo = sorted(tempos_execucao.items(), key=lambda x: x[1])

for i, (nome, tempo) in enumerate(ranking_tempo):
    medalhas = ["🥇", "🥈", "🥉"]
    pos = medalhas[i] if i < 3 else f"{i+1}º"
    print(f"{pos} {nome} - Tempo: {tempo:.2f}s")

print("\n🏁 Corrida finalizada!")

# ⏱️ EXIBIÇÃO DO TEMPO
print(f"\n⏱️ Tempo total de execução: {tempo_total:.2f} segundos")
