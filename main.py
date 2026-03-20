import threading
import random
import time

# Controle de chegada
posicoes = []
lock = threading.Lock()

def barra_progresso(distancia, tamanho=20):
    progresso = int((distancia / 100) * tamanho)
    return "█" * progresso + "-" * (tamanho - progresso)

def corredor(nome):
    distancia = 0
    tropeços = 0

    while distancia < 100:
        passo = random.randint(1, 10)

        # 🌦️ Evento global (clima)
        clima = random.choice(["normal", "chuva"])
        if clima == "chuva":
            print(f"🌧️ Pista molhada! {nome} reduz velocidade.")
            passo = max(1, passo - 3)

        # 🎯 Evento individual
        evento = random.choice(["normal", "tropecou", "boost"])

        if evento == "tropecou":
            tropeços += 1
            print(f"⚠️ {nome} tropeçou! (x{tropeços})")
            time.sleep(1)
            passo = 0

        elif evento == "boost":
            print(f"🚀 {nome} disparou!")
            passo += random.randint(5, 10)

        # 💀 Eliminado se tropeçar muito
        if tropeços >= 3:
            print(f"💀 {nome} foi eliminado!")
            return

        distancia += passo
        distancia = min(distancia, 100)

        barra = barra_progresso(distancia)
        print(f"{nome:12} |{barra}| {distancia:3d}m")

        time.sleep(random.uniform(0.3, 0.7))

    # 🏁 Registro de chegada (thread-safe)
    with lock:
        posicoes.append(nome)

    print(f"🏁 {nome} terminou!")

# Lista de corredores
nomes = ["A", "B", "C", "D"]

threads = []

print("🏁 CORRIDA INICIADA!\n")

for nome in nomes:
    t = threading.Thread(target=corredor, args=(f"Corredor {nome}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 🥇 Ranking final
print("\n🏆 RESULTADO FINAL:\n")

for i, nome in enumerate(posicoes):
    medalha = ["🥇", "🥈", "🥉"]
    simbolo = medalha[i] if i < 3 else f"{i+1}º"
    print(f"{simbolo} {nome}")

print("\n🏁 Corrida finalizada!")