#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementación del algoritmo DPLL (Davis-Putnam-Logemann-Loveland)
Solucionador de satisfacibilidad booleana para fórmulas CNF
"""

import time
from typing import Dict, List, Optional, Tuple, Any
from cnf_formula import CNFFormula
from utils import (
    print_step, 
    print_assignment, 
    print_formula_state,
    create_statistics,
    get_variable_from_literal,
    is_negative_literal
)

class DPLLSolver:
    """Implementación del algoritmo DPLL para resolver SAT"""
    
    def __init__(self, verbose: bool = False, heuristic: str = "first"):
        """
        Inicializa el solver DPLL
        
        Args:
            verbose: Si True, muestra pasos detallados del algoritmo
            heuristic: Heurística para elegir literales ("first", "most_frequent", "jeroslow_wang")
        """
        self.verbose = verbose
        self.heuristic = heuristic
        self.statistics = create_statistics()
        self.step_counter = 0
        self.current_depth = 0
        self.assignment_stack = []  # Para backtracking
    
    def solve(self, formula: CNFFormula) -> Dict[str, Any]:
        """
        Resuelve una fórmula CNF usando el algoritmo DPLL
        
        Args:
            formula: La fórmula CNF a resolver
        
        Returns:
            Diccionario con el resultado:
            {
                'satisfacible': bool,
                'asignacion': Dict[str, bool] o None,
                'estadisticas': Dict[str, Any]
            }
        """
        start_time = time.time()
        self._reset_statistics()
        
        if self.verbose:
            print("\n" + "="*60)
            print("    INICIANDO ALGORITMO DPLL")
            print("="*60)
            print_formula_state(formula.clausulas, "Fórmula inicial")
        
        # Ejecutar el algoritmo DPLL
        result, assignment = self._dpll_recursive(formula, {})
        
        # Calcular estadísticas finales
        end_time = time.time()
        self.statistics['tiempo'] = end_time - start_time
        
        if self.verbose:
            print("\n" + "="*60)
            print("    ALGORITMO DPLL COMPLETADO")
            print("="*60)
            if result:
                print("✓ RESULTADO: SATISFACIBLE")
                if assignment:
                    print_assignment(assignment)
            else:
                print("✗ RESULTADO: INSATISFACIBLE")
        
        return {
            'satisfacible': result,
            'asignacion': assignment if result else None,
            'estadisticas': self.statistics.copy()
        }
    
    def _reset_statistics(self):
        """Reinicia las estadísticas para una nueva ejecución"""
        self.statistics = create_statistics()
        self.step_counter = 0
        self.current_depth = 0
        self.assignment_stack = []
    
    def _dpll_recursive(self, formula: CNFFormula, assignment: Dict[str, bool]) -> Tuple[bool, Dict[str, bool]]:
        """
        Implementación recursiva del algoritmo DPLL
        
        Args:
            formula: Fórmula CNF actual
            assignment: Asignación parcial actual
        
        Returns:
            Tupla (es_satisfacible, asignacion_completa)
        """
        self.statistics['nodos_explorados'] += 1
        self.current_depth += 1
        self.statistics['max_depth'] = max(self.statistics['max_depth'], self.current_depth)
        
        if self.verbose:
            self._print_current_state(formula, assignment)
        
        # Paso 1: Verificar condiciones de parada
        if formula.is_empty():
            if self.verbose:
                print_step(self.step_counter, "Fórmula vacía encontrada - SATISFACIBLE")
            self.current_depth -= 1
            return True, assignment.copy()
        
        if formula.has_empty_clause():
            if self.verbose:
                print_step(self.step_counter, "Cláusula vacía encontrada - CONFLICTO")
            self.current_depth -= 1
            return False, {}
        
        # Paso 2: Aplicar simplificaciones
        simplified_formula, new_assignments = formula.simplify()
        
        # Actualizar asignación con las simplificaciones
        updated_assignment = assignment.copy()
        updated_assignment.update(new_assignments)
        
        if new_assignments:
            if self.verbose:
                self._print_simplifications(new_assignments)
            
            # Actualizar estadísticas
            unit_clauses = formula.get_unit_clauses()
            pure_literals = formula.get_pure_literals()
            self.statistics['propagaciones'] += len(unit_clauses)
            self.statistics['literales_puros'] += len(pure_literals)
            
            # Recursión con fórmula simplificada
            result, final_assignment = self._dpll_recursive(simplified_formula, updated_assignment)
            self.current_depth -= 1
            return result, final_assignment
        
        # Paso 3: Elegir literal para ramificación
        branching_literal = simplified_formula.choose_branching_literal(self.heuristic)
        
        if branching_literal is None:
            # No hay más variables libres, la fórmula es satisfacible
            if self.verbose:
                print_step(self.step_counter, "No hay más variables libres - SATISFACIBLE")
            self.current_depth -= 1
            return True, updated_assignment.copy()
        
        if self.verbose:
            self.step_counter += 1
            print_step(self.step_counter, f"Ramificación en variable '{branching_literal}'")
        
        # Paso 4: Probar con literal positivo
        if self.verbose:
            print(f"\n  → Probando {branching_literal} = True")
        
        # Crear nueva asignación
        positive_assignment = updated_assignment.copy()
        positive_assignment[branching_literal] = True
        
        # Aplicar asignación a la fórmula
        positive_formula = simplified_formula.assign_literal(branching_literal)
        
        # Recursión con literal positivo
        self.assignment_stack.append((branching_literal, True))
        result_positive, assignment_positive = self._dpll_recursive(positive_formula, positive_assignment)
        self.assignment_stack.pop()
        
        if result_positive:
            if self.verbose:
                print(f"  ✓ Rama {branching_literal} = True es satisfacible")
            self.current_depth -= 1
            return True, assignment_positive
        
        # Paso 5: Probar con literal negativo (backtracking)
        if self.verbose:
            print(f"  ✗ Rama {branching_literal} = True falló")
            print(f"  → Probando {branching_literal} = False (backtracking)")
        
        self.statistics['backtracking_count'] += 1
        
        # Crear nueva asignación
        negative_assignment = updated_assignment.copy()
        negative_assignment[branching_literal] = False
        
        # Aplicar asignación negativa a la fórmula
        negative_literal = f"-{branching_literal}"
        negative_formula = simplified_formula.assign_literal(negative_literal)
        
        # Recursión con literal negativo
        self.assignment_stack.append((branching_literal, False))
        result_negative, assignment_negative = self._dpll_recursive(negative_formula, negative_assignment)
        self.assignment_stack.pop()
        
        if result_negative:
            if self.verbose:
                print(f"  ✓ Rama {branching_literal} = False es satisfacible")
            self.current_depth -= 1
            return True, assignment_negative
        else:
            if self.verbose:
                print(f"  ✗ Rama {branching_literal} = False también falló")
                print(f"  → Ambas ramas fallaron - INSATISFACIBLE")
            self.current_depth -= 1
            return False, {}
    
    def _print_current_state(self, formula: CNFFormula, assignment: Dict[str, bool]):
        """Imprime el estado actual del algoritmo"""
        print(f"\n--- Profundidad {self.current_depth} ---")
        print_assignment(assignment)
        
        if len(formula.clausulas) <= 10:  # Solo mostrar fórmulas pequeñas
            print_formula_state(formula.clausulas, "Fórmula actual")
        else:
            stats = formula.get_statistics()
            print(f"Fórmula actual: {stats['num_clauses']} cláusulas, {stats['num_variables']} variables")
    
    def _print_simplifications(self, new_assignments: Dict[str, bool]):
        """Imprime las simplificaciones aplicadas"""
        if new_assignments:
            self.step_counter += 1
            details = []
            for var, value in new_assignments.items():
                details.append(f"Asignado {var} = {value}")
            print_step(self.step_counter, "Simplificaciones aplicadas", details)
    
    def solve_with_all_solutions(self, formula: CNFFormula) -> List[Dict[str, bool]]:
        """
        Encuentra todas las soluciones posibles de una fórmula CNF
        
        Args:
            formula: La fórmula CNF a resolver
        
        Returns:
            Lista de todas las asignaciones que satisfacen la fórmula
        """
        all_solutions = []
        self._find_all_solutions(formula, {}, all_solutions)
        return all_solutions
    
    def _find_all_solutions(self, formula: CNFFormula, assignment: Dict[str, bool], solutions: List[Dict[str, bool]]):
        """
        Función auxiliar recursiva para encontrar todas las soluciones
        """
        # Verificar condiciones de parada
        if formula.has_empty_clause():
            return
        
        if formula.is_empty():
            # Completar asignación con variables restantes
            complete_assignment = assignment.copy()
            all_vars = formula.get_variables() if hasattr(formula, '_original_variables') else set()
            for var in all_vars:
                if var not in complete_assignment:
                    complete_assignment[var] = True  # Valor por defecto
            solutions.append(complete_assignment)
            return
        
        # Aplicar simplificaciones
        simplified_formula, new_assignments = formula.simplify()
        updated_assignment = assignment.copy()
        updated_assignment.update(new_assignments)
        
        if new_assignments:
            self._find_all_solutions(simplified_formula, updated_assignment, solutions)
            return
        
        # Elegir literal para ramificación
        branching_literal = simplified_formula.choose_branching_literal(self.heuristic)
        
        if branching_literal is None:
            solutions.append(updated_assignment.copy())
            return
        
        # Probar ambas ramas
        for value in [True, False]:
            new_assignment = updated_assignment.copy()
            new_assignment[branching_literal] = value
            
            literal = branching_literal if value else f"-{branching_literal}"
            new_formula = simplified_formula.assign_literal(literal)
            
            self._find_all_solutions(new_formula, new_assignment, solutions)
    
    def get_conflict_analysis(self, formula: CNFFormula) -> Dict[str, Any]:
        """
        Analiza los conflictos en una fórmula insatisfacible
        
        Args:
            formula: Fórmula CNF insatisfacible
        
        Returns:
            Análisis de conflictos
        """
        analysis = {
            'empty_clauses': [],
            'unit_conflicts': [],
            'pure_literal_conflicts': []
        }
        
        # Encontrar cláusulas vacías
        for i, clause in enumerate(formula.clausulas):
            if not clause:
                analysis['empty_clauses'].append(i)
        
        # Analizar conflictos unitarios
        unit_clauses = formula.get_unit_clauses()
        unit_vars = {get_variable_from_literal(lit): lit for lit in unit_clauses}
        
        for var, literal in unit_vars.items():
            opposite = f"-{var}" if not is_negative_literal(literal) else var
            if opposite in unit_clauses:
                analysis['unit_conflicts'].append((literal, opposite))
        
        return analysis
    
    def get_solver_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre la configuración del solver
        
        Returns:
            Información del solver
        """
        return {
            'algorithm': 'DPLL (Davis-Putnam-Logemann-Loveland)',
            'version': '1.0',
            'heuristic': self.heuristic,
            'verbose_mode': self.verbose,
            'features': [
                'Unit Propagation',
                'Pure Literal Elimination',
                'Backtracking',
                'Multiple Heuristics',
                'Conflict Analysis',
                'All Solutions Finding'
            ]
        }