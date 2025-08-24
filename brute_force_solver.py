#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementación del algoritmo de fuerza bruta para resolver SAT
Genera todas las posibles asignaciones de variables y verifica satisfacibilidad
"""

import time
import itertools
from typing import Dict, List, Optional, Tuple, Any
from cnf_formula import CNFFormula
from utils import (
    create_statistics,
    get_variable_from_literal,
    is_negative_literal
)

class BruteForceSolver:
    """Implementación del algoritmo de fuerza bruta para resolver SAT"""
    
    def __init__(self, verbose: bool = False):
        """
        Inicializa el solver de fuerza bruta
        
        Args:
            verbose: Si True, muestra pasos detallados del algoritmo
        """
        self.verbose = verbose
        self.statistics = create_statistics()
        self.assignments_tested = 0
    
    def solve(self, formula: CNFFormula) -> Dict[str, Any]:
        """
        Resuelve una fórmula CNF usando fuerza bruta
        
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
        self.assignments_tested = 0
        
        if self.verbose:
            print("\n=== ALGORITMO DE FUERZA BRUTA ===")
            print(f"Fórmula a resolver: {formula}")
        
        # Obtener todas las variables de la fórmula
        variables = list(formula.get_variables())
        
        if not variables:
            # Fórmula sin variables
            if not formula.clausulas:
                # Fórmula vacía es satisfacible
                result = {
                    'satisfacible': True,
                    'asignacion': {},
                    'estadisticas': self._get_statistics(time.time() - start_time)
                }
            else:
                # Hay cláusulas pero no variables (imposible)
                result = {
                    'satisfacible': False,
                    'asignacion': None,
                    'estadisticas': self._get_statistics(time.time() - start_time)
                }
            return result
        
        if self.verbose:
            print(f"Variables encontradas: {sorted(variables)}")
            print(f"Total de asignaciones a probar: 2^{len(variables)} = {2**len(variables)}")
        
        # Generar todas las posibles asignaciones
        for assignment_values in itertools.product([False, True], repeat=len(variables)):
            self.assignments_tested += 1
            assignment = dict(zip(variables, assignment_values))
            
            if self.verbose:
                print(f"\nProbando asignación {self.assignments_tested}: {assignment}")
            
            # Verificar si esta asignación satisface la fórmula
            if self._evaluate_formula(formula, assignment):
                if self.verbose:
                    print(f"✓ ¡Asignación satisfactoria encontrada!")
                
                result = {
                    'satisfacible': True,
                    'asignacion': assignment,
                    'estadisticas': self._get_statistics(time.time() - start_time)
                }
                return result
            
            elif self.verbose:
                print(f"✗ Asignación no satisface la fórmula")
        
        # No se encontró ninguna asignación satisfactoria
        if self.verbose:
            print(f"\n✗ No se encontró ninguna asignación satisfactoria")
            print(f"Total de asignaciones probadas: {self.assignments_tested}")
        
        result = {
            'satisfacible': False,
            'asignacion': None,
            'estadisticas': self._get_statistics(time.time() - start_time)
        }
        return result
    
    def find_all_solutions(self, formula: CNFFormula) -> List[Dict[str, bool]]:
        """
        Encuentra todas las soluciones posibles para una fórmula CNF
        
        Args:
            formula: La fórmula CNF a resolver
        
        Returns:
            Lista de todas las asignaciones que satisfacen la fórmula
        """
        start_time = time.time()
        self.assignments_tested = 0
        solutions = []
        
        variables = list(formula.get_variables())
        
        if not variables:
            if not formula.clausulas:
                return [{}]  # Fórmula vacía tiene una solución vacía
            else:
                return []  # No hay soluciones
        
        if self.verbose:
            print(f"\n=== BÚSQUEDA DE TODAS LAS SOLUCIONES (FUERZA BRUTA) ===")
            print(f"Variables: {sorted(variables)}")
        
        # Generar todas las posibles asignaciones
        for assignment_values in itertools.product([False, True], repeat=len(variables)):
            self.assignments_tested += 1
            assignment = dict(zip(variables, assignment_values))
            
            if self._evaluate_formula(formula, assignment):
                solutions.append(assignment.copy())
                if self.verbose:
                    print(f"Solución {len(solutions)}: {assignment}")
        
        if self.verbose:
            print(f"\nTotal de soluciones encontradas: {len(solutions)}")
            print(f"Total de asignaciones probadas: {self.assignments_tested}")
        
        return solutions
    
    def _evaluate_formula(self, formula: CNFFormula, assignment: Dict[str, bool]) -> bool:
        """
        Evalúa si una asignación satisface la fórmula CNF
        
        Args:
            formula: La fórmula CNF
            assignment: Asignación de variables
        
        Returns:
            True si la asignación satisface la fórmula, False en caso contrario
        """
        for clause in formula.clausulas:
            clause_satisfied = False
            
            for literal in clause:
                variable = get_variable_from_literal(literal)
                is_negative = is_negative_literal(literal)
                
                if variable in assignment:
                    literal_value = assignment[variable]
                    if is_negative:
                        literal_value = not literal_value
                    
                    if literal_value:
                        clause_satisfied = True
                        break
            
            # Si alguna cláusula no se satisface, la fórmula no es satisfacible
            if not clause_satisfied:
                return False
        
        # Todas las cláusulas se satisfacen
        return True
    
    def _get_statistics(self, execution_time: float) -> Dict[str, Any]:
        """
        Obtiene las estadísticas de ejecución
        
        Args:
            execution_time: Tiempo de ejecución en segundos
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'tiempo': execution_time,
            'asignaciones_probadas': self.assignments_tested,
            'algoritmo': 'Fuerza Bruta'
        }
    
    def reset_statistics(self):
        """Reinicia las estadísticas del solver"""
        self.statistics = create_statistics()
        self.assignments_tested = 0
    
    def get_solver_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el solver
        
        Returns:
            Diccionario con información del solver
        """
        return {
            'nombre': 'Solver de Fuerza Bruta',
            'descripcion': 'Algoritmo que prueba todas las posibles asignaciones de variables',
            'complejidad': 'O(2^n) donde n es el número de variables',
            'ventajas': [
                'Garantiza encontrar la solución si existe',
                'Puede encontrar todas las soluciones',
                'Implementación simple y directa'
            ],
            'desventajas': [
                'Complejidad exponencial',
                'Ineficiente para fórmulas con muchas variables',
                'No utiliza técnicas de optimización'
            ]
        }