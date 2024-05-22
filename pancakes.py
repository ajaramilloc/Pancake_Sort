import random
import time


def getPoblacionInicial(
    tamanoRepresentacion: int, n: int, tamanoPoblacion: int
) -> list[list]:
    solInicial = []

    for _ in range(tamanoPoblacion):
        elemRecorridos = 0
        cromosomaX = []
        while elemRecorridos < tamanoRepresentacion:
            numAleatorio = random.randint(0, n - 2)  # Aqui cambie el n-1 por n-2
            cromosomaX.append(numAleatorio)  # Se añade a cromosomaX el numero aleatorio
            elemRecorridos += 1
        solInicial.append(cromosomaX)
    return solInicial


def getFitness(poblacion: list[list], representacion: list, pancakesOrdenado: list) -> list[tuple[int, list]]:

    # print(pancakesOrdenado)

    poblacionFitness = []
    # pancakesOrdenado = representacion.copy()
    # pancakesOrdenado.sort(reverse=True)
    for cromosoma in poblacion:
        fitnessCromosoma = 0
        pancakes = representacion.copy()
        for posicionFlip in cromosoma:
            listaInicio = pancakes[:posicionFlip]
            listaFinal = pancakes[posicionFlip:]
            listaFinal.reverse()
            pancakes = listaInicio + listaFinal
        for posicionPancake in range(len(pancakes)):
            if pancakesOrdenado[posicionPancake] == pancakes[posicionPancake]:
                fitnessCromosoma += 1
        # print(pancakesOrdenado , " ,    " , pancakes , " ,     " , fitnessCromosoma)
        if fitnessCromosoma == len(pancakes):
            return [(-1, cromosoma)]
        poblacionFitness.append((fitnessCromosoma, cromosoma))
    return poblacionFitness

def roulette_selection(poblacionFitness: tuple[int, list]) -> tuple:
    total_fitness = sum(individual[0] for individual in poblacionFitness)
    valor_aleatorio = random.uniform(0, total_fitness)
    fitness_acumulado = 0
    for individual in poblacionFitness:
        fitness_acumulado += individual[0]
        if fitness_acumulado >= valor_aleatorio:
            return individual

def getCrossover(poblacion: tuple[int, list]) -> list:
    newPoblacion = []
    iterador = 0
    while iterador <= len(poblacion):
        cromosoma1 = roulette_selection(poblacion)
        cromosoma2 = roulette_selection(poblacion)
        puntoDeCorte = random.randint(0, len(cromosoma1[1]))
        newCromosoma1 = cromosoma1[1][:puntoDeCorte] + cromosoma2[1][puntoDeCorte:]
        newCromosoma2 = cromosoma2[1][:puntoDeCorte] + cromosoma1[1][puntoDeCorte:]
        newPoblacion.append(newCromosoma1)
        if iterador + 2 <= len(poblacion):
            newPoblacion.append(newCromosoma2)
        iterador += 2
    return newPoblacion

def getMutaciones(poblacion: list[list], probMutacion: float) -> list[list]:
    for cromosoma in poblacion:
        probMutacionCromosoma = random.uniform(0, 1)
        posicion = random.randint(0, len(cromosoma) - 1)
        if probMutacionCromosoma <= probMutacion:
            cromosoma[posicion] = random.randint(0, len(cromosoma) - 1)
    return poblacion


def eliminar_dobles_consecutivos(lista):
    if not lista:
        return []
    nueva_lista = []
    i = 0
    while i < len(lista):
        if i < len(lista) - 1 and lista[i] == lista[i + 1]:
            i += 2
        else:
            nueva_lista.append(lista[i])
            i += 1
    return nueva_lista


def generarCasos(n: int) -> list:
    casos = []
    for _ in range(n):
        caso = []
        for _ in range(n):
            caso.append(random.randint(1, n+1))
        casos.append(caso)
    # print("Ya estan los casos generados")
    return casos



def main():
    tInicio = time.time()
    # representacion = [5, 2, 3, 4, 1]
    representacion = [1,4,3,2,5]
    # representacion = [1, 4, 3, 2, 5,6,7,8,9]

    representacion = generarCasos(10)


    pancakesOrdenado = representacion.copy()
    pancakesOrdenado.sort(reverse=True)

    n = len(representacion)
    maximoRepeticiones = 1000
    tamanoPoblacion = 1000
    probaMutacion = 0.4
    maximoTamano = ((5 * n) + 5) // 3
    poblacionInicial = getPoblacionInicial(maximoTamano, n, tamanoPoblacion)
    for _ in range(maximoRepeticiones):
        poblacionFitness = getFitness(poblacionInicial, representacion, pancakesOrdenado)
        if poblacionFitness[0][0] == -1:
            print("Logrado")
            # print(poblacionFitness[0][1])
            poblacionFitness = eliminar_dobles_consecutivos(poblacionFitness[0][1])
            tfin = time.time()
            print("Tiempo de ejecucion: ", tfin - tInicio)
            return poblacionFitness
        nuevaPoblacion = getCrossover(poblacionFitness)
        nuevaPoblacion = getMutaciones(nuevaPoblacion, probaMutacion)
    nuevaPoblacion = eliminar_dobles_consecutivos(nuevaPoblacion[0])
    tfin = time.time()
    print("Tiempo de ejecucion: ", tfin - tInicio)
    return nuevaPoblacion

print(main())