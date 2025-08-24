#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos y casos de prueba para el algoritmo DPLL
Contiene fórmulas predefinidas y funciones de validación
"""

from typing import List, Dict, Any
from cnf_formula import CNFFormula
from dpll_solver import DPLLSolver
from utils import format_formula, print_statistics

def get_example_formulas() -> Dict[str, Dict[str, Any]]:
    """
    Obtiene un conjunto de fórmulas de ejemplo para probar el algoritmo
    
    Returns:
        Diccionario con ejemplos categorizados
    """
    examples = {
        "satisfacibles": {
            "simple": {
                "nombre": "Fórmula satisfacible simple",
                "descripcion": "Una fórmula básica que es satisfacible",
                "formula": "(A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)",
                "cnf": [["A", "B"], ["-A", "C"], ["-B", "-C"]],
                "solucion_esperada": {"A": True, "B": False, "C": True}
            },
            "propagacion_unitaria": {
                "nombre": "Fórmula con propagación unitaria",
                "descripcion": "Demuestra la propagación unitaria en acción",
                "formula": "(A) ∧ (¬A ∨ B) ∧ (¬B ∨ C)",
                "cnf": [["A"], ["-A", "B"], ["-B", "C"]],
                "solucion_esperada": {"A": True, "B": True, "C": True}
            },
            "literales_puros": {
                "nombre": "Fórmula con literales puros",
                "descripcion": "Demuestra la eliminación de literales puros",
                "formula": "(A ∨ B) ∧ (A ∨ C) ∧ (D)",
                "cnf": [["A", "B"], ["A", "C"], ["D"]],
                "solucion_esperada": {"A": True, "B": True, "C": True, "D": True}
            },
            "compleja": {
                "nombre": "Fórmula satisfacible compleja",
                "descripcion": "Una fórmula más compleja que requiere backtracking",
                "formula": "(A ∨ B ∨ C) ∧ (¬A ∨ ¬B) ∧ (¬A ∨ ¬C) ∧ (¬B ∨ ¬C) ∧ (A ∨ D) ∧ (B ∨ D)",
                "cnf": [["A", "B", "C"], ["-A", "-B"], ["-A", "-C"], ["-B", "-C"], ["A", "D"], ["B", "D"]],
                "solucion_esperada": None  # Múltiples soluciones posibles
            }
        },
        "insatisfacibles": {
            "simple": {
                "nombre": "Fórmula insatisfacible simple",
                "descripcion": "Contradicción directa",
                "formula": "(A) ∧ (¬A)",
                "cnf": [["A"], ["-A"]],
                "solucion_esperada": None
            },
            "tres_variables": {
                "nombre": "Insatisfacible con tres variables",
                "descripcion": "Fórmula insatisfacible más compleja",
                "formula": "(A ∨ B ∨ C) ∧ (¬A ∨ B ∨ C) ∧ (A ∨ ¬B ∨ C) ∧ (A ∨ B ∨ ¬C) ∧ (¬A ∨ ¬B ∨ C) ∧ (¬A ∨ B ∨ ¬C) ∧ (A ∨ ¬B ∨ ¬C) ∧ (¬A ∨ ¬B ∨ ¬C)",
                "cnf": [
                    ["A", "B", "C"], ["-A", "B", "C"], ["A", "-B", "C"], ["A", "B", "-C"],
                    ["-A", "-B", "C"], ["-A", "B", "-C"], ["A", "-B", "-C"], ["-A", "-B", "-C"]
                ],
                "solucion_esperada": None
            }
        },
        "casos_especiales": {
            "formula_vacia": {
                "nombre": "Fórmula vacía",
                "descripcion": "Fórmula sin cláusulas (trivialmente satisfacible)",
                "formula": "⊤",
                "cnf": [],
                "solucion_esperada": {}
            },
            "clausula_vacia": {
                "nombre": "Cláusula vacía",
                "descripcion": "Contiene una cláusula vacía (insatisfacible)",
                "formula": "(A) ∧ (□)",
                "cnf": [["A"], []],
                "solucion_esperada": None
            },
            "una_variable": {
                "nombre": "Una sola variable",
                "descripcion": "Fórmula con una sola variable",
                "formula": "(A)",
                "cnf": [["A"]],
                "solucion_esperada": {"A": True}
            }
        }
    }
    
    return examples

def run_example(example_key: str, category: str = None, verbose: bool = False) -> Dict[str, Any]:
    """
    Ejecuta un ejemplo específico
    
    Args:
        example_key: Clave del ejemplo a ejecutar
        category: Categoría del ejemplo (si no se especifica, busca en todas)
        verbose: Si mostrar pasos detallados
    
    Returns:
        Resultado de la ejecución
    """
    examples = get_example_formulas()
    
    # Buscar el ejemplo
    example = None
    found_category = None
    
    if category:
        if category in examples and example_key in examples[category]:
            example = examples[category][example_key]
            found_category = category
    else:
        # Buscar en todas las categorías
        for cat, examples_in_cat in examples.items():
            if example_key in examples_in_cat:
                example = examples_in_cat[example_key]
                found_category = cat
                break
    
    if not example:
        return {"error": f"Ejemplo '{example_key}' no encontrado"}
    
    print(f"\n{'='*60}")
    print(f"EJECUTANDO EJEMPLO: {example['nombre']}")
    print(f"Categoría: {found_category}")
    print(f"{'='*60}")
    print(f"Descripción: {example['descripcion']}")
    print(f"Fórmula: {example['formula']}")
    print(f"CNF: {format_formula(example['cnf'])}")
    
    # Crear y resolver la fórmula
    try:
        formula = CNFFormula(example['cnf'])
        solver = DPLLSolver(verbose=verbose)
        
        result = solver.solve(formula)
        
        print(f"\n{'='*60}")
        print("RESULTADO")
        print(f"{'='*60}")
        
        if result['satisfacible']:
            print("✓ SATISFACIBLE")
            if result['asignacion']:
                print("\nAsignación encontrada:")
                for var, value in sorted(result['asignacion'].items()):
                    print(f"  {var} = {value}")
                
                # Verificar si coincide con la solución esperada
                expected = example.get('solucion_esperada')
                if expected is not None:
                    if verify_solution(formula, result['asignacion']):
                        print("\n✓ La solución es válida")
                    else:
                        print("\n✗ ERROR: La solución no es válida")
        else:
            print("✗ INSATISFACIBLE")
            expected = example.get('solucion_esperada')
            if expected is None:
                print("✓ Resultado esperado")
            else:
                print("✗ ERROR: Se esperaba que fuera satisfacible")
        
        # Mostrar estadísticas
        if verbose:
            print_statistics(result['estadisticas'])
        
        return result
        
    except Exception as e:
        error_msg = f"Error al ejecutar ejemplo: {e}"
        print(f"\n✗ {error_msg}")
        return {"error": error_msg}

def verify_solution(formula: CNFFormula, assignment: Dict[str, bool]) -> bool:
    """
    Verifica si una asignación satisface una fórmula CNF
    
    Args:
        formula: La fórmula CNF
        assignment: La asignación a verificar
    
    Returns:
        True si la asignación satisface la fórmula
    """
    for clause in formula.clausulas:
        clause_satisfied = False
        
        for literal in clause:
            if literal.startswith('-'):
                var = literal[1:]
                if var in assignment and not assignment[var]:
                    clause_satisfied = True
                    break
            else:
                if literal in assignment and assignment[literal]:
                    clause_satisfied = True
                    break
        
        if not clause_satisfied:
            return False
    
    return True

def run_all_examples(verbose: bool = False) -> Dict[str, Any]:
    """
    Ejecuta todos los ejemplos disponibles
    
    Args:
        verbose: Si mostrar pasos detallados
    
    Returns:
        Resumen de todos los resultados
    """
    examples = get_example_formulas()
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "details": {}
    }
    
    for category, examples_in_cat in examples.items():
        results["details"][category] = {}
        
        for example_key in examples_in_cat:
            results["total"] += 1
            
            print(f"\n{'='*80}")
            print(f"EJECUTANDO: {category} -> {example_key}")
            print(f"{'='*80}")
            
            result = run_example(example_key, category, verbose=False)
            
            if "error" in result:
                results["failed"] += 1
                results["details"][category][example_key] = {"status": "error", "result": result}
            else:
                results["passed"] += 1
                results["details"][category][example_key] = {"status": "success", "result": result}
    
    # Mostrar resumen final
    print(f"\n{'='*80}")
    print("RESUMEN FINAL")
    print(f"{'='*80}")
    print(f"Total de ejemplos ejecutados: {results['total']}")
    print(f"Exitosos: {results['passed']}")
    print(f"Fallidos: {results['failed']}")
    print(f"Tasa de éxito: {(results['passed']/results['total']*100):.1f}%")
    
    return results

def benchmark_solver(num_variables: int = 10, num_clauses: int = 20, num_tests: int = 10) -> Dict[str, Any]:
    """
    Ejecuta un benchmark del solver con fórmulas aleatorias
    
    Args:
        num_variables: Número de variables en las fórmulas
        num_clauses: Número de cláusulas en las fórmulas
        num_tests: Número de pruebas a ejecutar
    
    Returns:
        Estadísticas del benchmark
    """
    import random
    
    results = {
        "satisfacible_count": 0,
        "insatisfacible_count": 0,
        "total_time": 0,
        "avg_time": 0,
        "max_time": 0,
        "min_time": float('inf'),
        "tests": []
    }
    
    solver = DPLLSolver(verbose=False)
    
    print(f"\nEjecutando benchmark con {num_tests} fórmulas aleatorias...")
    print(f"Parámetros: {num_variables} variables, {num_clauses} cláusulas")
    
    for i in range(num_tests):
        # Generar fórmula aleatoria
        clauses = []
        variables = [f"x{j+1}" for j in range(num_variables)]
        
        for _ in range(num_clauses):
            clause_size = random.randint(1, min(3, num_variables))
            clause = []
            selected_vars = random.sample(variables, clause_size)
            
            for var in selected_vars:
                if random.choice([True, False]):
                    clause.append(f"-{var}")
                else:
                    clause.append(var)
            
            clauses.append(clause)
        
        # Resolver la fórmula
        try:
            formula = CNFFormula(clauses)
            result = solver.solve(formula)
            
            test_result = {
                "test_id": i + 1,
                "satisfacible": result['satisfacible'],
                "time": result['estadisticas']['tiempo'],
                "nodes": result['estadisticas']['nodos_explorados']
            }
            
            results["tests"].append(test_result)
            
            if result['satisfacible']:
                results["satisfacible_count"] += 1
            else:
                results["insatisfacible_count"] += 1
            
            time_taken = result['estadisticas']['tiempo']
            results["total_time"] += time_taken
            results["max_time"] = max(results["max_time"], time_taken)
            results["min_time"] = min(results["min_time"], time_taken)
            
            print(f"  Prueba {i+1}: {'SAT' if result['satisfacible'] else 'UNSAT'} ({time_taken:.4f}s)")
            
        except Exception as e:
            print(f"  Prueba {i+1}: ERROR - {e}")
    
    results["avg_time"] = results["total_time"] / num_tests if num_tests > 0 else 0
    
    # Mostrar resumen
    print(f"\n{'='*50}")
    print("RESUMEN DEL BENCHMARK")
    print(f"{'='*50}")
    print(f"Fórmulas satisfacibles: {results['satisfacible_count']}")
    print(f"Fórmulas insatisfacibles: {results['insatisfacible_count']}")
    print(f"Tiempo total: {results['total_time']:.4f}s")
    print(f"Tiempo promedio: {results['avg_time']:.4f}s")
    print(f"Tiempo mínimo: {results['min_time']:.4f}s")
    print(f"Tiempo máximo: {results['max_time']:.4f}s")
    
    return results

def interactive_example_menu():
    """
    Menú interactivo para ejecutar ejemplos
    """
    examples = get_example_formulas()
    
    while True:
        print(f"\n{'='*60}")
        print("MENÚ DE EJEMPLOS")
        print(f"{'='*60}")
        
        option_num = 1
        options = {}
        
        for category, examples_in_cat in examples.items():
            print(f"\n{category.upper()}:")
            for example_key, example in examples_in_cat.items():
                print(f"  {option_num}. {example['nombre']}")
                options[str(option_num)] = (category, example_key)
                option_num += 1
        
        print(f"\n{option_num}. Ejecutar todos los ejemplos")
        print(f"{option_num + 1}. Benchmark con fórmulas aleatorias")
        print("0. Volver al menú principal")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == "0":
            break
        elif choice == str(option_num):
            verbose = input("¿Mostrar pasos detallados? (s/n): ").strip().lower() == 's'
            run_all_examples(verbose)
            input("\nPresione Enter para continuar...")
        elif choice == str(option_num + 1):
            try:
                num_vars = int(input("Número de variables (default 10): ") or "10")
                num_clauses = int(input("Número de cláusulas (default 20): ") or "20")
                num_tests = int(input("Número de pruebas (default 10): ") or "10")
                benchmark_solver(num_vars, num_clauses, num_tests)
            except ValueError:
                print("Valores inválidos, usando valores por defecto.")
                benchmark_solver()
            input("\nPresione Enter para continuar...")
        elif choice in options:
            category, example_key = options[choice]
            verbose = input("¿Mostrar pasos detallados? (s/n): ").strip().lower() == 's'
            run_example(example_key, category, verbose)
            input("\nPresione Enter para continuar...")
        else:
            print("Opción no válida.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    # Ejecutar menú interactivo si se ejecuta directamente
    interactive_example_menu()