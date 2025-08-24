#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clase CNFFormula para representar fórmulas en Forma Normal Conjuntiva
Parte del proyecto de implementación del algoritmo DPLL
"""

from typing import List, Set, Dict, Optional, Tuple
from utils import (
    get_variable_from_literal, 
    is_negative_literal, 
    negate_literal,
    format_formula,
    validate_cnf_formula
)

class CNFFormula:
    """Representa una fórmula en Forma Normal Conjuntiva (CNF)"""
    
    def __init__(self, clausulas: List[List[str]]):
        """
        Inicializa una fórmula CNF
        
        Args:
            clausulas: Lista de cláusulas, donde cada cláusula es una lista de literales
        
        Raises:
            ValueError: Si la fórmula no es válida
        """
        # Validar la fórmula
        is_valid, error_msg = validate_cnf_formula(clausulas)
        if not is_valid:
            raise ValueError(error_msg)
        
        self.clausulas = [clause[:] for clause in clausulas]  # Copia profunda
        self._variables = None  # Cache para las variables
        self._unit_clauses = None  # Cache para cláusulas unitarias
        self._pure_literals = None  # Cache para literales puros
    
    def __str__(self) -> str:
        """Representación en string de la fórmula"""
        return format_formula(self.clausulas)
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"CNFFormula({self.clausulas})"
    
    def __eq__(self, other) -> bool:
        """Compara dos fórmulas CNF"""
        if not isinstance(other, CNFFormula):
            return False
        return self.clausulas == other.clausulas
    
    def copy(self) -> 'CNFFormula':
        """Crea una copia de la fórmula"""
        return CNFFormula(self.clausulas)
    
    def get_variables(self) -> Set[str]:
        """Obtiene todas las variables de la fórmula"""
        if self._variables is None:
            variables = set()
            for clausula in self.clausulas:
                for literal in clausula:
                    variables.add(get_variable_from_literal(literal))
            self._variables = variables
        return self._variables.copy()
    
    def get_literals(self) -> Set[str]:
        """Obtiene todos los literales de la fórmula"""
        literals = set()
        for clausula in self.clausulas:
            for literal in clausula:
                literals.add(literal)
        return literals
    
    def is_empty(self) -> bool:
        """Verifica si la fórmula está vacía (satisfacible trivialmente)"""
        return len(self.clausulas) == 0
    
    def has_empty_clause(self) -> bool:
        """Verifica si la fórmula contiene una cláusula vacía (insatisfacible)"""
        return any(len(clausula) == 0 for clausula in self.clausulas)
    
    def get_unit_clauses(self) -> List[str]:
        """Obtiene todas las cláusulas unitarias (con un solo literal)"""
        unit_clauses = []
        for clausula in self.clausulas:
            if len(clausula) == 1:
                unit_clauses.append(clausula[0])
        return unit_clauses
    
    def get_pure_literals(self) -> Set[str]:
        """Obtiene todos los literales puros (que aparecen solo en una polaridad)"""
        positive_literals = set()
        negative_literals = set()
        
        for clausula in self.clausulas:
            for literal in clausula:
                if is_negative_literal(literal):
                    negative_literals.add(get_variable_from_literal(literal))
                else:
                    positive_literals.add(literal)
        
        # Un literal es puro si aparece solo positivo o solo negativo
        pure_literals = set()
        
        # Literales que aparecen solo positivos
        for var in positive_literals:
            if var not in negative_literals:
                pure_literals.add(var)
        
        # Literales que aparecen solo negativos
        for var in negative_literals:
            if var not in positive_literals:
                pure_literals.add(f"-{var}")
        
        return pure_literals
    
    def assign_literal(self, literal: str) -> 'CNFFormula':
        """
        Asigna un valor a un literal y simplifica la fórmula
        
        Args:
            literal: El literal a asignar como verdadero
        
        Returns:
            Nueva fórmula CNF simplificada
        """
        new_clausulas = []
        negated_literal = negate_literal(literal)
        
        for clausula in self.clausulas:
            if literal in clausula:
                # Si el literal está en la cláusula, la cláusula se satisface
                continue
            elif negated_literal in clausula:
                # Si la negación del literal está en la cláusula, eliminarla
                new_clausula = [lit for lit in clausula if lit != negated_literal]
                new_clausulas.append(new_clausula)
            else:
                # La cláusula no se ve afectada
                new_clausulas.append(clausula[:])
        
        return CNFFormula(new_clausulas)
    
    def unit_propagation(self) -> Tuple['CNFFormula', Dict[str, bool]]:
        """
        Aplica propagación unitaria hasta que no haya más cláusulas unitarias
        
        Returns:
            Tupla con la nueva fórmula y las asignaciones realizadas
        """
        current_formula = self.copy()
        assignments = {}
        
        while True:
            unit_clauses = current_formula.get_unit_clauses()
            
            if not unit_clauses:
                break
            
            # Tomar la primera cláusula unitaria
            unit_literal = unit_clauses[0]
            
            # Registrar la asignación
            variable = get_variable_from_literal(unit_literal)
            value = not is_negative_literal(unit_literal)
            assignments[variable] = value
            
            # Aplicar la asignación
            current_formula = current_formula.assign_literal(unit_literal)
            
            # Si se genera una cláusula vacía, la fórmula es insatisfacible
            if current_formula.has_empty_clause():
                break
        
        return current_formula, assignments
    
    def pure_literal_elimination(self) -> Tuple['CNFFormula', Dict[str, bool]]:
        """
        Elimina literales puros de la fórmula
        
        Returns:
            Tupla con la nueva fórmula y las asignaciones realizadas
        """
        current_formula = self.copy()
        assignments = {}
        
        pure_literals = current_formula.get_pure_literals()
        
        for pure_literal in pure_literals:
            # Registrar la asignación
            variable = get_variable_from_literal(pure_literal)
            value = not is_negative_literal(pure_literal)
            assignments[variable] = value
            
            # Aplicar la asignación
            current_formula = current_formula.assign_literal(pure_literal)
        
        return current_formula, assignments
    
    def choose_branching_literal(self, heuristic: str = "first") -> Optional[str]:
        """
        Elige un literal para ramificación según la heurística especificada
        
        Args:
            heuristic: Heurística a usar ("first", "most_frequent", "jeroslow_wang")
        
        Returns:
            El literal elegido o None si no hay variables libres
        """
        variables = self.get_variables()
        
        if not variables:
            return None
        
        if heuristic == "first":
            return self._choose_first_literal(variables)
        elif heuristic == "most_frequent":
            return self._choose_most_frequent_literal()
        elif heuristic == "jeroslow_wang":
            return self._choose_jeroslow_wang_literal()
        else:
            return self._choose_first_literal(variables)
    
    def _choose_first_literal(self, variables: Set[str]) -> str:
        """Elige el primer literal disponible"""
        return sorted(variables)[0]
    
    def _choose_most_frequent_literal(self) -> str:
        """Elige el literal que aparece con más frecuencia"""
        literal_count = {}
        
        for clausula in self.clausulas:
            for literal in clausula:
                literal_count[literal] = literal_count.get(literal, 0) + 1
        
        if not literal_count:
            return None
        
        # Encontrar el literal más frecuente
        most_frequent = max(literal_count.items(), key=lambda x: x[1])
        return get_variable_from_literal(most_frequent[0])
    
    def _choose_jeroslow_wang_literal(self) -> str:
        """Elige el literal usando la heurística de Jeroslow-Wang"""
        variable_scores = {}
        
        for clausula in self.clausulas:
            clause_weight = 2 ** (-len(clausula))
            for literal in clausula:
                variable = get_variable_from_literal(literal)
                if variable not in variable_scores:
                    variable_scores[variable] = 0
                variable_scores[variable] += clause_weight
        
        if not variable_scores:
            return None
        
        # Encontrar la variable con mayor puntuación
        best_variable = max(variable_scores.items(), key=lambda x: x[1])
        return best_variable[0]
    
    def simplify(self) -> Tuple['CNFFormula', Dict[str, bool]]:
        """
        Aplica todas las simplificaciones posibles (propagación unitaria y eliminación de literales puros)
        
        Returns:
            Tupla con la fórmula simplificada y todas las asignaciones realizadas
        """
        current_formula = self.copy()
        all_assignments = {}
        
        changed = True
        while changed:
            changed = False
            
            # Aplicar propagación unitaria
            new_formula, unit_assignments = current_formula.unit_propagation()
            if unit_assignments:
                changed = True
                current_formula = new_formula
                all_assignments.update(unit_assignments)
                
                # Si hay cláusula vacía, parar
                if current_formula.has_empty_clause():
                    break
            
            # Aplicar eliminación de literales puros
            new_formula, pure_assignments = current_formula.pure_literal_elimination()
            if pure_assignments:
                changed = True
                current_formula = new_formula
                all_assignments.update(pure_assignments)
        
        return current_formula, all_assignments
    
    def get_statistics(self) -> Dict[str, int]:
        """Obtiene estadísticas de la fórmula"""
        return {
            "num_variables": len(self.get_variables()),
            "num_clauses": len(self.clausulas),
            "num_literals": sum(len(clausula) for clausula in self.clausulas),
            "num_unit_clauses": len(self.get_unit_clauses()),
            "num_pure_literals": len(self.get_pure_literals()),
            "max_clause_length": max(len(clausula) for clausula in self.clausulas) if self.clausulas else 0,
            "min_clause_length": min(len(clausula) for clausula in self.clausulas) if self.clausulas else 0
        }
    
    def to_dimacs(self) -> str:
        """
        Convierte la fórmula al formato DIMACS
        
        Returns:
            String en formato DIMACS
        """
        variables = sorted(self.get_variables())
        var_to_num = {var: i+1 for i, var in enumerate(variables)}
        
        lines = []
        lines.append(f"p cnf {len(variables)} {len(self.clausulas)}")
        
        for clausula in self.clausulas:
            dimacs_clause = []
            for literal in clausula:
                if is_negative_literal(literal):
                    var = get_variable_from_literal(literal)
                    dimacs_clause.append(f"-{var_to_num[var]}")
                else:
                    dimacs_clause.append(str(var_to_num[literal]))
            lines.append(" ".join(dimacs_clause) + " 0")
        
        return "\n".join(lines)
    
    @classmethod
    def from_dimacs(cls, dimacs_str: str) -> 'CNFFormula':
        """
        Crea una fórmula CNF desde formato DIMACS
        
        Args:
            dimacs_str: String en formato DIMACS
        
        Returns:
            Nueva instancia de CNFFormula
        """
        lines = dimacs_str.strip().split('\n')
        
        # Encontrar la línea de problema
        num_vars = 0
        for line in lines:
            if line.startswith('p cnf'):
                parts = line.split()
                num_vars = int(parts[2])
                break
        
        # Crear mapeo de números a variables
        num_to_var = {i+1: f"x{i+1}" for i in range(num_vars)}
        
        clausulas = []
        for line in lines:
            if line.startswith('c') or line.startswith('p') or not line.strip():
                continue
            
            clause = []
            numbers = line.strip().split()
            for num_str in numbers:
                num = int(num_str)
                if num == 0:
                    break
                elif num > 0:
                    clause.append(num_to_var[num])
                else:
                    clause.append(f"-{num_to_var[-num]}")
            
            if clause:
                clausulas.append(clause)
        
        return cls(clausulas)