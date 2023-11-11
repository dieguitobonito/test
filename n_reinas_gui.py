import tkinter as tk
from tkinter import messagebox
import random
import time

class SolucionadorNQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de N-Reinas")

        self.configurar_gui()

    def configurar_gui(self):
        # Entry para que el usuario ingrese la cantidad de reinas
        self.label = tk.Label(self.root, text="Ingrese la cantidad de reinas (N):")
        self.label.pack()

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_var)
        self.entry.pack()

        # Menú desplegable para seleccionar el algoritmo de solución
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Fuerza Bruta")  # Algoritmo predeterminado
        self.algorithm_label = tk.Label(self.root, text="Seleccione el algoritmo de solución:")
        self.algorithm_label.pack()

        algoritmos = ["Fuerza Bruta", "Algoritmo Genético"]
        self.algorithm_dropdown = tk.OptionMenu(self.root, self.algorithm_var, *algoritmos)
        self.algorithm_dropdown.pack()

        # Botón para comenzar a resolver
        self.solve_button = tk.Button(self.root, text="Resolver", command=self.resolver_n_reinas)
        self.solve_button.pack()

        # Lienzo del tablero de ajedrez
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

    def es_seguro(self, tablero, fila, col, n):
        for i in range(col):
            if tablero[i] == fila or \
               tablero[i] - i == fila - col or \
               tablero[i] + i == fila + col:
                return False
        return True

    # Algoritmos a utilizar
    def resolver_n_reinas_fuerza_bruta(self, n):
        def colocar_reina(tablero, col):
            if col == n:
                self.mostrar_solucion(tablero)
                return

            for fila in range(n):
                if self.es_seguro(tablero, fila, col, n):
                    tablero[col] = fila
                    colocar_reina(tablero, col + 1)

        tablero = [-1] * n
        colocar_reina(tablero, 0)

    def resolver_n_reinas_algoritmo_genetico(self, n):
        def aptitud(tablero):
            ataques = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if tablero[i] == tablero[j] or abs(i - j) == abs(tablero[i] - tablero[j]):
                        ataques += 1
            return ataques

        def cruzar(padre1, padre2):
            punto_division = random.randint(1, n - 1)
            hijo = padre1[:punto_division] + padre2[punto_division:]
            return hijo

        def mutar(hijo):
            punto_mutacion = random.randint(0, n - 1)
            hijo[punto_mutacion] = random.randint(0, n - 1)
            return hijo

        tamano_poblacion = 100
        max_generaciones = 1000

        poblacion = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(tamano_poblacion)]

        for generacion in range(max_generaciones):
            poblacion.sort(key=lambda tablero: aptitud(tablero))
            if aptitud(poblacion[0]) == 0:
                self.mostrar_solucion(poblacion[0])
                return

            nueva_poblacion = [poblacion[0]]

            for _ in range(tamano_poblacion - 1):
                padre1 = random.choice(poblacion[:50])
                padre2 = random.choice(poblacion[:50])
                hijo = cruzar(padre1, padre2)
                if random.random() < 0.1:
                    hijo = mutar(hijo)
                nueva_poblacion.append(hijo)

            poblacion = nueva_poblacion

        messagebox.showinfo("Algoritmo Genético", "No se encontró solución en las generaciones dadas.")

    def resolver_n_reinas(self):
        try:
            n = int(self.entry_var.get())
            if n <= 0:
                raise ValueError("Por favor, ingrese un entero positivo para N.")

            algoritmo = self.algorithm_var.get()

            self.limpiar_canvas()

            if algoritmo == "Fuerza Bruta":
                tiempo_inicio = time.time()
                self.resolver_n_reinas_fuerza_bruta(n)
                tiempo_fin = time.time()
            elif algoritmo == "Algoritmo Genético":
                tiempo_inicio = time.time()
                self.resolver_n_reinas_algoritmo_genetico(n)
                tiempo_fin = time.time()

            tiempo_transcurrido = tiempo_fin - tiempo_inicio
            messagebox.showinfo("Métricas de Desempeño", f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def mostrar_solucion(self, tablero):
        self.limpiar_canvas()

        tamano_celda = 400 // len(tablero)

        for fila in range(len(tablero)):
            for col in range(len(tablero)):
                x1, y1 = col * tamano_celda, fila * tamano_celda
                x2, y2 = (col + 1) * tamano_celda, (fila + 1) * tamano_celda
                color = "blue" if tablero[col] == fila else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        self.root.update()
        time.sleep(0.5)  # Pausa para la visualización

    def limpiar_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = SolucionadorNQueensGUI(root)
    root.mainloop()

