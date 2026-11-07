"""
Transcripción de hechos y reglas de la actividad de adquisición de conocimiento.
Dominio: identificación y clasificación de animales.
Animal documentado: ornitorrinco1.
"""

# Hechos conocidos del animal, transcritos de la actividad.
# Cada predicado se almacena como una cadena dentro del conjunto del individuo.
HECHOS = {
    "ornitorrinco1": {
        "tiene_pelo",
        "da_leche",
        "pone_huevos",
        "pico_aplanado",
        "patas_palmeadas",
        "detecta_senales_electricas",
        "nada",
        "vive_agua_dulce",
    }
}

# Vínculos semánticos entre individuos y conceptos.
# Cada tupla tiene la forma: (sujeto, relación, objeto).
RELACIONES = {
    ("ornitorrinco1", "es_un", "animal"),
    ("ornitorrinco1", "tiene_caracteristica", "pico_aplanado"),
    ("ornitorrinco1", "tiene_caracteristica", "patas_palmeadas"),
    ("ornitorrinco1", "tiene_caracteristica", "pelaje"),
    ("ornitorrinco1", "tiene_habitat", "agua_dulce"),
    ("ornitorrinco1", "presenta_capacidad", "electrorrecepcion"),
}

# Reglas expresadas como:
# cabeza: [[condiciones alternativas], ...]
# Cada lista interna representa condiciones que deben cumplirse juntas (AND).
# Las listas externas representan alternativas (OR).
REGLAS = {
    # Reglas generales del texto de la bióloga.
    "mamifero": [
        ["tiene_pelo"],
        ["da_leche"],
    ],
    "ave": [
        ["tiene_plumas"],
        ["vuela", "pone_huevos"],
    ],
    "carnivoro": [
        ["mamifero", "come_carne"],
    ],
    "ungulado": [
        ["mamifero", "tiene_pezuñas"],
    ],
    "guepardo": [
        ["carnivoro", "color_leonado", "manchas_oscuras"],
    ],
    "tigre": [
        ["carnivoro", "rayas_negras"],
    ],
    "jirafa": [
        ["ungulado", "cuello_largo", "manchas_oscuras"],
    ],
    "cebra": [
        ["ungulado", "rayas_negras"],
    ],
    "pinguino": [
        ["ave", "nada", "blanco_y_negro"],
    ],
    "albatros": [
        ["ave", "vuela_muy_bien"],
    ],

    # Reglas añadidas a partir de la entrevista sobre el ornitorrinco.
    "ornitorrinco": [
        ["mamifero", "pone_huevos", "pico_aplanado", "patas_palmeadas"],
    ],
    "electrorreceptor": [
        ["ornitorrinco", "detecta_senales_electricas"],
    ],
    "monotrema": [
        ["mamifero", "pone_huevos"],
    ],
    # Formalización de la regla 15: permite distinguirlo por estos rasgos.
    "diferenciable_de_nutria_y_castor": [
        ["mamifero", "pico_aplanado", "pone_huevos"],
    ],
}


def inferir(individuo):
    """Devuelve los hechos iniciales y los predicados que se pueden deducir."""
    conocidos = set(HECHOS.get(individuo, set()))

    # Encadenamiento hacia adelante: se aplican reglas hasta que no haya
    # nuevos predicados que agregar.
    cambio = True
    while cambio:
        cambio = False
        for conclusion, alternativas in REGLAS.items():
            if conclusion in conocidos:
                continue

            for condiciones in alternativas:
                if all(condicion in conocidos for condicion in condiciones):
                    conocidos.add(conclusion)
                    cambio = True
                    break

    return conocidos


def mostrar_resultados(individuo):
    """Muestra hechos, inferencias y consultas de interés."""
    iniciales = HECHOS.get(individuo, set())
    resultados = inferir(individuo)

    print("=" * 62)
    print("SISTEMA DE IDENTIFICACIÓN DE ANIMALES")
    print("=" * 62)
    print(f"Individuo analizado: {individuo}")

    print("\nHECHOS REGISTRADOS:")
    for hecho in sorted(iniciales):
        print(f"  - {hecho}({individuo})")

    print("\nCONCLUSIONES INFERIDAS:")
    inferidos = sorted(resultados - iniciales)
    for conclusion in inferidos:
        print(f"  - {conclusion}({individuo})")

    print("\nCONSULTAS:")
    consultas = [
        "mamifero",
        "ave",
        "ornitorrinco",
        "monotrema",
        "electrorreceptor",
        "diferenciable_de_nutria_y_castor",
    ]
    for consulta in consultas:
        respuesta = consulta in resultados
        print(f"  ?- {consulta}({individuo}).  ->  {respuesta}")

    print("\nINTERPRETACIÓN:")
    if "mamifero" in resultados and "ave" not in resultados:
        print("  El individuo se clasifica como mamífero, no como ave.")
        print("  Poner huevos no basta para clasificarlo como ave:")
        print("  la regla original también exige que vuele, o que tenga plumas.")
    if "ornitorrinco" in resultados:
        print("  Las características registradas permiten identificarlo como ornitorrinco.")
    print("=" * 62)


if __name__ == "__main__":
    mostrar_resultados("ornitorrinco1")
