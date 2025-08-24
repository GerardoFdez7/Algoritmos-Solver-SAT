#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para el proyecto DPLL
Funciones auxiliares para la interfaz y manejo de datos
"""

import os
import sys
import time

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")

def format_literal(literal):
    """Formatea un literal para mostrar correctamente"""
    if literal.startswith('-'):
        return f"¬{literal[1:]}"
    return literal

def format_clause(clause):
    """Formatea una cláusula para mostrar correctamente"""
    if not clause:
        return "□"  # Cláusula vacía
    
    formatted_literals = [format_literal(lit) for lit in clause]
    return f"({' ∨ '.join(formatted_literals)})"

def format_formula(clauses):
    """Formatea una fórmula CNF completa para mostrar correctamente"""
    if not clauses:
        return "⊤"  # Fórmula vacía (verdadera)
    
    formatted_clauses = [format_clause(clause) for clause in clauses]
    return " ∧ ".join(formatted_clauses)

def validate_variable_name(var_name):
    """Valida que el nombre de variable sea válido"""
    if not var_name:
        return False
    
    # Debe empezar con letra y contener solo letras, números y guiones bajos
    if not var_name[0].isalpha():
        return False
    
    return all(c.isalnum() or c == '_' for c in var_name)

def parse_literal(literal_str):
    """Parsea un literal desde string"""
    literal_str = literal_str.strip()
    
    if literal_str.startswith('-'):
        var_name = literal_str[1:].strip()
        if not validate_variable_name(var_name):
            raise ValueError(f"Nombre de variable inválido: {var_name}")
        return f"-{var_name}"
    else:
        if not validate_variable_name(literal_str):
            raise ValueError(f"Nombre de variable inválido: {literal_str}")
        return literal_str

def parse_clause(clause_str):
    """Parsea una cláusula desde string"""
    if not clause_str.strip():
        return []
    
    literals = []
    # Aceptar tanto comas como espacios como separadores
    if ',' in clause_str:
        separators = clause_str.split(',')
    else:
        separators = clause_str.split()
    
    for literal_str in separators:
        literal_str = literal_str.strip()
        if literal_str:  # Ignorar strings vacíos
            literal = parse_literal(literal_str)
            literals.append(literal)
    
    return literals

def parse_cnf_formula(formula_str):
    """Parsea una fórmula CNF completa desde string"""
    if not formula_str.strip():
        return []
    
    clauses = []
    for clause_str in formula_str.split(';'):
        clause = parse_clause(clause_str)
        if clause:  # Solo agregar cláusulas no vacías
            clauses.append(clause)
    
    return clauses

def get_variable_from_literal(literal):
    """Extrae el nombre de la variable de un literal"""
    if literal.startswith('-'):
        return literal[1:]
    return literal

def is_negative_literal(literal):
    """Verifica si un literal es negativo"""
    return literal.startswith('-')

def negate_literal(literal):
    """Niega un literal"""
    if literal.startswith('-'):
        return literal[1:]
    return f"-{literal}"

def print_step(step_number, description, details=None):
    """Imprime un paso del algoritmo de forma formateada"""
    print(f"\n--- Paso {step_number}: {description} ---")
    if details:
        for detail in details:
            print(f"  • {detail}")

def print_assignment(assignment):
    """Imprime una asignación de variables de forma formateada"""
    if not assignment:
        print("  Asignación vacía")
        return
    
    print("  Asignación actual:")
    for var, value in sorted(assignment.items()):
        symbol = "✓" if value else "✗"
        print(f"    {var} = {value} {symbol}")

def print_formula_state(clauses, title="Estado de la fórmula"):
    """Imprime el estado actual de la fórmula"""
    print(f"\n{title}:")
    if not clauses:
        print("  ⊤ (fórmula vacía - satisfacible)")
        return
    
    for i, clause in enumerate(clauses, 1):
        if not clause:
            print(f"  Cláusula {i}: □ (cláusula vacía - conflicto)")
        else:
            formatted = format_clause(clause)
            print(f"  Cláusula {i}: {formatted}")

def measure_time(func):
    """Decorador para medir el tiempo de ejecución de una función"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

def create_statistics():
    """Crea un diccionario para almacenar estadísticas"""
    return {
        'tiempo': 0.0,
        'nodos_explorados': 0,
        'propagaciones': 0,
        'literales_puros': 0,
        'backtracking_count': 0,
        'max_depth': 0
    }

def print_statistics(stats):
    """Imprime las estadísticas de ejecución"""
    print("\n" + "="*40)
    print("    ESTADÍSTICAS DE EJECUCIÓN")
    print("="*40)
    print(f"Tiempo total: {stats['tiempo']:.4f} segundos")
    
    # Estadísticas específicas del algoritmo
    if 'algoritmo' in stats:
        print(f"Algoritmo: {stats['algoritmo']}")
    
    if 'asignaciones_probadas' in stats:
        # Estadísticas de fuerza bruta
        print(f"Asignaciones probadas: {stats['asignaciones_probadas']}")
    else:
        # Estadísticas de DPLL
        print(f"Nodos explorados: {stats.get('nodos_explorados', 0)}")
        print(f"Propagaciones unitarias: {stats.get('propagaciones', 0)}")
        print(f"Literales puros eliminados: {stats.get('literales_puros', 0)}")
        print(f"Operaciones de backtracking: {stats.get('backtracking_count', 0)}")
        print(f"Profundidad máxima: {stats.get('max_depth', 0)}")
    
    print("="*40)

def save_formula_to_file(clauses, filename):
    """Guarda una fórmula CNF en un archivo"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Fórmula CNF\n")
            f.write("# Formato: cada línea representa una cláusula\n")
            f.write("# Los literales se separan por comas\n")
            f.write("# Use '-' para negación\n\n")
            
            for i, clause in enumerate(clauses, 1):
                clause_str = ','.join(clause)
                f.write(f"{clause_str}\n")
        
        return True
    except Exception as e:
        print(f"Error al guardar archivo: {e}")
        return False

def load_formula_from_file(filename):
    """Carga una fórmula CNF desde un archivo"""
    try:
        clauses = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorar comentarios y líneas vacías
                if line and not line.startswith('#'):
                    clause = parse_clause(line)
                    if clause:
                        clauses.append(clause)
        
        return clauses
    except Exception as e:
        print(f"Error al cargar archivo: {e}")
        return None

def validate_cnf_formula(clauses):
    """Valida que una fórmula CNF sea correcta"""
    if not isinstance(clauses, list):
        return False, "La fórmula debe ser una lista de cláusulas"
    
    for i, clause in enumerate(clauses):
        if not isinstance(clause, list):
            return False, f"La cláusula {i+1} debe ser una lista de literales"
        
        for j, literal in enumerate(clause):
            if not isinstance(literal, str):
                return False, f"El literal {j+1} en la cláusula {i+1} debe ser una cadena"
            
            try:
                parse_literal(literal)
            except ValueError as e:
                return False, f"Error en literal {j+1} de cláusula {i+1}: {e}"
    
    return True, "Fórmula CNF válida"