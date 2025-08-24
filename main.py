#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa principal para el algoritmo DPLL
Implementa un menú interactivo para resolver fórmulas SAT
"""

import sys
import os
from typing import Dict, List, Any, Optional

# Importar módulos del proyecto
from dpll_solver import DPLLSolver
from brute_force_solver import BruteForceSolver
from cnf_formula import CNFFormula
from utils import (
    clear_screen, pause, format_formula, format_literal, format_clause,
    parse_cnf_formula, parse_clause, parse_literal,
    print_step, print_assignment, print_formula_state,
    measure_time, create_statistics, print_statistics,
    save_formula_to_file, load_formula_from_file, validate_cnf_formula
)

def mostrar_menu_principal():
    """
    Muestra el menú principal del programa
    """
    clear_screen()
    print("="*60)
    print("           SOLVER SAT - COMPARACIÓN DE ALGORITMOS")
    print("="*60)
    print("Seleccione el algoritmo a utilizar:")
    print()
    print("1. Algoritmo de Fuerza Bruta")
    print("   - Prueba todas las posibles asignaciones")
    print("   - Garantiza encontrar la solución")
    print("   - Complejidad: O(2^n × m)")
    print()
    print("2. Algoritmo DPLL")
    print("   - Propagación unitaria y literales puros")
    print("   - Complejidad: O(2^n)")
    print()
    print("0. Salir")
    print("="*60)

def obtener_ejemplos_predefinidos() -> Dict[str, Dict[str, Any]]:
    """
    Obtiene ejemplos predefinidos de fórmulas CNF
    
    Returns:
        Diccionario con ejemplos categorizados
    """
    return {
        "satisfacibles": {
            "simple": {
                "nombre": "Fórmula satisfacible simple",
                "formula": "(A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)",
                "cnf": [["A", "B"], ["-A", "C"], ["-B", "-C"]]
            },
            "propagacion": {
                "nombre": "Con propagación unitaria",
                "formula": "(A) ∧ (¬A ∨ B) ∧ (¬B ∨ C)",
                "cnf": [["A"], ["-A", "B"], ["-B", "C"]]
            }
        },
        "insatisfacibles": {
            "contradiccion": {
                "nombre": "Contradicción directa",
                "formula": "(A) ∧ (¬A)",
                "cnf": [["A"], ["-A"]]
            }
        }
    }

def ingresar_formula_manual() -> Optional[CNFFormula]:
    """
    Permite al usuario ingresar una fórmula CNF manualmente
    
    Returns:
        Objeto CNFFormula o None si hay error
    """
    print("\nIngreso de fórmula CNF")
    print("-" * 30)
    print("Formato: Cada cláusula en una línea, literales separados por espacios")
    print("Use '-' para negación (ej: -A para ¬A)")
    print("Ejemplo: A B -C")
    print("Escriba 'FIN' para terminar\n")
    
    clausulas = []
    num_clausula = 1
    
    while True:
        try:
            entrada = input(f"Cláusula {num_clausula}: ").strip()
            
            if entrada.upper() == "FIN":
                break
            
            if not entrada:
                continue
            
            clausula = parse_clause(entrada)
            if clausula is not None:
                clausulas.append(clausula)
                print(f"  ✓ Agregada: {format_clause(clausula)}")
                num_clausula += 1
            else:
                print("  ✗ Formato inválido. Intente nuevamente.")
                
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            return None
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    if not clausulas:
        print("No se ingresaron cláusulas válidas.")
        return None
    
    try:
        formula = CNFFormula(clausulas)
        print(f"\n✓ Fórmula creada: {format_formula(clausulas)}")
        return formula
    except Exception as e:
        print(f"✗ Error al crear la fórmula: {e}")
        return None

def mostrar_informacion_dpll():
    """
    Muestra información sobre el algoritmo DPLL
    """
    clear_screen()
    print("="*70)
    print("                    ALGORITMO DPLL")
    print("="*70)
    print()
    print("El algoritmo DPLL (Davis-Putnam-Logemann-Loveland) es un algoritmo")
    print("completo de backtracking para determinar la satisfacibilidad de")
    print("fórmulas proposicionales en forma normal conjuntiva (CNF).")
    print()
    print("CARACTERÍSTICAS PRINCIPALES:")
    print("• Algoritmo completo: siempre termina con la respuesta correcta")
    print("• Utiliza backtracking sistemático")
    print("• Incorpora técnicas de optimización")
    print()
    print("TÉCNICAS DE OPTIMIZACIÓN:")
    print("1. Propagación Unitaria:")
    print("   - Detecta cláusulas con un solo literal")
    print("   - Asigna automáticamente el valor necesario")
    print("   - Simplifica la fórmula")
    print()
    print("2. Eliminación de Literales Puros:")
    print("   - Identifica variables que aparecen solo positiva o negativamente")
    print("   - Las asigna para satisfacer todas sus cláusulas")
    print()
    print("3. Heurísticas de Ramificación:")
    print("   - Selección inteligente de variables para ramificar")
    print("   - Mejora el rendimiento del algoritmo")
    print()
    print("HEURÍSTICAS DISPONIBLES:")
    print("• First: Selecciona la primera variable disponible")
    print("• Most Frequent: Selecciona la variable más frecuente")
    print("• Jeroslow-Wang: Heurística basada en pesos de cláusulas")
    print()
    pause()

def configurar_solver() -> Dict[str, Any]:
    """
    Permite configurar las opciones del solver
    
    Returns:
        Diccionario con la configuración
    """
    config = {
        "verbose": False,
        "heuristica": "jeroslow_wang",
        "mostrar_pasos": False,
        "limite_tiempo": None
    }
    
    while True:
        clear_screen()
        print("="*50)
        print("         CONFIGURACIÓN DEL SOLVER")
        print("="*50)
        print(f"1. Modo verbose: {'Activado' if config['verbose'] else 'Desactivado'}")
        print(f"2. Heurística: {config['heuristica']}")
        print(f"3. Mostrar pasos: {'Sí' if config['mostrar_pasos'] else 'No'}")
        print(f"4. Límite de tiempo: {config['limite_tiempo'] or 'Sin límite'}")
        print("0. Volver")
        print("="*50)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "0":
            break
        elif opcion == "1":
            config["verbose"] = not config["verbose"]
        elif opcion == "2":
            print("\nHeurísticas disponibles:")
            print("1. first (primera variable)")
            print("2. most_frequent (más frecuente)")
            print("3. jeroslow_wang (Jeroslow-Wang)")
            
            heur_opcion = input("Seleccione heurística (1-3): ").strip()
            heuristicas = {"1": "first", "2": "most_frequent", "3": "jeroslow_wang"}
            if heur_opcion in heuristicas:
                config["heuristica"] = heuristicas[heur_opcion]
        elif opcion == "3":
            config["mostrar_pasos"] = not config["mostrar_pasos"]
        elif opcion == "4":
            try:
                limite = input("Límite de tiempo en segundos (Enter para sin límite): ").strip()
                config["limite_tiempo"] = float(limite) if limite else None
            except ValueError:
                print("Valor inválido.")
                pause()
    
    return config

def resolver_formula_con_opciones(formula: CNFFormula, config: Dict[str, Any]):
    """
    Resuelve una fórmula con las opciones configuradas
    
    Args:
        formula: La fórmula a resolver
        config: Configuración del solver
    """
    print("\nResolviendo fórmula...")
    solver = DPLLSolver(
        verbose=config["verbose"],
        heuristic=config["heuristica"]
    )
    
    resultado = solver.solve(formula)
    
    print("\n" + "="*50)
    print("RESULTADO")
    print("="*50)
    
    if resultado["satisfacible"]:
        print("✓ SATISFACIBLE")
        if resultado["asignacion"]:
            print("\nAsignación encontrada:")
            print_assignment(resultado["asignacion"])
            
            # Preguntar si guardar la solución
            if input("\n¿Guardar solución en archivo? (s/n): ").strip().lower() == 's':
                try:
                    archivo = input("Nombre del archivo: ").strip()
                    if not archivo.endswith('.txt'):
                        archivo += '.txt'
                    
                    with open(archivo, 'w', encoding='utf-8') as f:
                        f.write("Solución de la fórmula CNF\n")
                        f.write("=" * 30 + "\n")
                        f.write(f"Fórmula: {format_formula(formula.clausulas)}\n\n")
                        f.write("Asignación:\n")
                        for var, value in sorted(resultado["asignacion"].items()):
                            f.write(f"{var} = {value}\n")
                        f.write("\nEstadísticas:\n")
                        for key, value in resultado["estadisticas"].items():
                            f.write(f"{key}: {value}\n")
                    
                    print(f"✓ Solución guardada en: {archivo}")
                except Exception as e:
                    print(f"✗ Error al guardar: {e}")
    else:
        print("✗ INSATISFACIBLE")
    
    if config["mostrar_pasos"] and "pasos" in resultado:
        print("\nPasos del algoritmo:")
        # Los pasos se imprimen automáticamente durante la ejecución del algoritmo
    
    print("\nEstadísticas:")
    print_statistics(resultado["estadisticas"])
    
    return resultado

def guardar_formula_interactivo(formula: CNFFormula):
    """
    Permite guardar una fórmula en un archivo
    
    Args:
        formula: La fórmula a guardar
    """
    try:
        archivo = input("Ingrese el nombre del archivo (sin extensión): ").strip()
        if not archivo:
            print("Nombre de archivo inválido.")
            return
        
        if not archivo.endswith('.cnf'):
            archivo += '.cnf'
        
        save_formula_to_file(formula, archivo)
        print(f"✓ Fórmula guardada en: {archivo}")
        
    except Exception as e:
        print(f"✗ Error al guardar: {e}")

def analizar_formula(formula: CNFFormula):
    """
    Analiza las propiedades de una fórmula
    
    Args:
        formula: La fórmula a analizar
    """
    print("\n" + "="*50)
    print("ANÁLISIS DE LA FÓRMULA")
    print("="*50)
    
    stats = formula.get_statistics()
    
    print(f"Número de variables: {stats['num_variables']}")
    print(f"Número de cláusulas: {stats['num_clausulas']}")
    print(f"Número total de literales: {stats['num_literales']}")
    print(f"Tamaño promedio de cláusula: {stats['tamano_promedio_clausula']:.2f}")
    print(f"Tamaño máximo de cláusula: {stats['tamano_max_clausula']}")
    print(f"Tamaño mínimo de cláusula: {stats['tamano_min_clausula']}")
    
    # Detectar cláusulas especiales
    unit_clauses = formula.get_unit_clauses()
    if unit_clauses:
        print(f"\nCláusulas unitarias: {len(unit_clauses)}")
        for clause in unit_clauses[:5]:  # Mostrar máximo 5
            print(f"  {format_clause(clause)}")
        if len(unit_clauses) > 5:
            print(f"  ... y {len(unit_clauses) - 5} más")
    
    pure_literals = formula.get_pure_literals()
    if pure_literals:
        print(f"\nLiterales puros: {len(pure_literals)}")
        for literal in list(pure_literals)[:10]:  # Mostrar máximo 10
            print(f"  {format_literal(literal)}")
        if len(pure_literals) > 10:
            print(f"  ... y {len(pure_literals) - 10} más")
    
    # Verificar si es trivialmente satisfacible o insatisfacible
    if formula.is_empty():
        print("\n✓ Fórmula vacía (trivialmente satisfacible)")
    elif formula.has_empty_clause():
        print("\n✗ Contiene cláusula vacía (insatisfacible)")
    
    print(f"\nFórmula completa:")
    print(f"{format_formula(formula.clausulas)}")

def buscar_todas_soluciones(formula: CNFFormula, config: Dict[str, Any]):
    """
    Busca todas las soluciones de una fórmula
    
    Args:
        formula: La fórmula a resolver
        config: Configuración del solver
    """
    print("\nBuscando todas las soluciones...")
    
    solver = DPLLSolver(
        verbose=config["verbose"],
        heuristic=config["heuristica"]
    )
    
    try:
        soluciones = solver.find_all_solutions(formula)
        
        print("\n" + "="*50)
        print("TODAS LAS SOLUCIONES")
        print("="*50)
        
        if not soluciones:
            print("✗ No hay soluciones (fórmula insatisfacible)")
        else:
            print(f"✓ Se encontraron {len(soluciones)} solución(es)")
            
            for i, solucion in enumerate(soluciones, 1):
                print(f"\nSolución {i}:")
                print_assignment(solucion)
                
                if i >= 10:  # Limitar a 10 soluciones mostradas
                    if len(soluciones) > 10:
                        print(f"\n... y {len(soluciones) - 10} soluciones más")
                    break
        
        # Mostrar estadísticas del solver
        info = solver.get_solver_info()
        if info:
            print("\nEstadísticas del solver:")
            print_statistics(info)
            
    except Exception as e:
        print(f"✗ Error al buscar soluciones: {e}")

def ejecutar_algoritmo_fuerza_bruta():
    """
    Ejecuta el algoritmo de fuerza bruta
    """
    clear_screen()
    print("="*60)
    print("           ALGORITMO DE FUERZA BRUTA")
    print("="*60)
    
    formula = ingresar_formula_manual()
    if formula:
        print("\nResolviendo con algoritmo de fuerza bruta...")
        solver = BruteForceSolver(verbose=True)
        resultado = solver.solve(formula)
        
        print("\n" + "="*50)
        print("RESULTADO")
        print("="*50)
        
        if resultado["satisfacible"]:
            print("✓ SATISFACIBLE")
            if resultado["asignacion"]:
                print("\nAsignación encontrada:")
                print_assignment(resultado["asignacion"])
        else:
            print("✗ INSATISFACIBLE")
        
        print("\nEstadísticas:")
        print_statistics(resultado["estadisticas"])
    
    pause()

def ejecutar_algoritmo_dpll():
    """
    Ejecuta el algoritmo DPLL
    """
    clear_screen()
    print("="*60)
    print("           ALGORITMO DPLL")
    print("="*60)
    
    formula = ingresar_formula_manual()
    if formula:
        config = {
            "verbose": True,
            "heuristica": "jeroslow_wang",
            "mostrar_pasos": False,
            "limite_tiempo": None
        }
        resolver_formula_con_opciones(formula, config)
    
    pause()

def main():
    """
    Función principal del programa
    """
    while True:
        mostrar_menu_principal()
        
        try:
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "0":
                print("\n¡Gracias por usar el solver SAT!")
                break
            elif opcion == "1":
                ejecutar_algoritmo_fuerza_bruta()
            elif opcion == "2":
                ejecutar_algoritmo_dpll()
            else:
                print("\nOpción no válida. Intente nuevamente.")
                pause()
                
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")
            pause()

if __name__ == "__main__":
    main()