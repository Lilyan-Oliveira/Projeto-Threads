import threading
import random
import time

#Criando um corredor
def corredor(nome):
    distancia = 0

    while distancia < 100:
        #Distância aleatória para o corredor avançar
        passo = random.randint(1, 10)
        distancia += passo

        # evita passar de 100
        distancia = min(distancia, 100)

        #Mostrando o progresso
        print(f"{nome}:  ({distancia}m)")

        #Descanso do corredor (talvez o tempo de recuperação)
        time.sleep(random.uniform(0.5, 1.0))

    #Thread finalizou a corrida
    print(f"🏁 {nome} terminou!")

#Lista de corredores (Precisa ser algo escalável)
nomes = ["A", "B", "C"]

threads = []

print("🏁 Corrida iniciada!\n")

#Cria corredores e inicia as Threads
for nome in nomes:
    t = threading.Thread(target=corredor, args=(f"Corredor {nome}",))
    threads.append(t)
    t.start()

#Espera todas acabarem de correr
for t in threads:
    t.join()

print("\n🏁 Corrida finalizada!")