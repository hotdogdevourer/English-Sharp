"""
Author: hotdogdevourer (Alias: Iris500)
License: MIT
See the LICENSE file in the project root.
Language name: E# (Full name: English Sharp)
VERSION: 3.2
███████╗ ██╗ ██╗ 
██╔════╝████████╗
█████╗  ╚██╔═██╔╝
██╔══╝  ████████╗
███████╗╚██╔═██╔╝
╚══════╝ ╚═╝ ╚═╝ 
"""
import os
import time
import sys
import re
import random
import math
import difflib
import getpass
import readline
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import statistics as stats_module

# --- Configuration ---
VALID_COMMANDS = [
    "this script uses:", "the number", "the text", "the value of",
    "do the following", "end doing", "while", "end while", "if", "end if", "otherwise if", "otherwise",
    "create a function", "end function definition", "give back",
    "create a structure", "end structure definition",
    "create list", "create array",
    "try", "catch", "end try",
    "display", "show", "ask", "read", "write", "delete",
    "generate", "wait", "clear", "sys",
    "end program", "break", "explain", "debug",
    "list files", "create directory", "move file"
]

FILLER_WORDS = {'please', 'lol', 'um', 'uh', 'like', 'actually', 'basically', 'just', 'really', 'very'}

# --- Documentation System ---
DOCUMENTATION = {
    # Commands
    "display": {
        "category": "I/O",
        "syntax": 'display the text "Hello World"',
        "description": "Print text to the console",
        "examples": [
            'display the text "Welcome to E#"',
            'display the text "{variable_name}"'
        ]
    },
    "show": {
        "category": "I/O",
        "syntax": 'show the text "Hello World"',
        "description": "Print text to the console (alias for display)",
        "examples": [
            'show the text "Hello"'
        ]
    },
    "ask": {
        "category": "I/O",
        "syntax": 'ask "prompt" and save the answer in VAR as TYPE',
        "description": "Read user input and save it to a variable",
        "examples": [
            'ask "What is your name?" and save the answer in name as string',
            'ask "Enter a number:" and save the answer in num as integer'
        ]
    },
    "variables": {
        "category": "Data",
        "syntax": 'the number/text VAR is VALUE and it should be TYPE',
        "description": "Declare and initialize a variable with a type",
        "types": ["integer", "float", "string", "decimal", "fraction"],
        "examples": [
            'the number count is 5 and it should be integer',
            'the text greeting is "Hello" and it should be string',
            'the number pi is 3.14 and it should be float'
        ]
    },
    "arithmetic": {
        "category": "Math",
        "syntax": "the value of RESULT should be X OPERATOR Y",
        "description": "Perform arithmetic operations",
        "operators": ["plus", "minus", "times", "divided by", "modulo"],
        "examples": [
            'the value of sum should be 5 plus 3',
            'the value of product should be 4 times 2',
            'the value of quotient should be 10 divided by 2'
        ]
    },
    "bitwise": {
        "category": "Bitwise",
        "syntax": "the value of RESULT should be X OPERATOR Y",
        "description": "Perform bitwise operations on integers",
        "operators": ["bitwise and", "bitwise or", "bitwise xor", "bitwise nor", "bitwise nand", "bitwise xnor"],
        "examples": [
            'the value of result should be 5 bitwise and 3',
            'the value of result should be 8 bitwise or 4',
            'the value of result should be 7 bitwise xor 3'
        ]
    },
    "bit_shift": {
        "category": "Bitwise",
        "syntax": "the value of RESULT should be X left/right shift N",
        "description": "Shift bits left or right",
        "examples": [
            'the value of result should be 8 left shift 2',
            'the value of result should be 16 right shift 1'
        ]
    },
    "boolean": {
        "category": "Boolean",
        "syntax": "the value of RESULT should be X OPERATOR Y",
        "description": "Perform boolean logical operations",
        "operators": ["bool and", "bool or", "bool xor", "bool nor", "bool nand", "bool xnor"],
        "examples": [
            'the value of result should be 1 bool and 1',
            'the value of result should be 0 bool or 1'
        ]
    },
    "if": {
        "category": "Control Flow",
        "syntax": "if CONDITION then\n  ...\nend if",
        "description": "Conditional execution of code blocks",
        "examples": [
            'if x greater than 5 then\n  display the text "Greater"\nend if',
            'if age greater than or equal to 18 then\n  display the text "Adult"\notherwise\n  display the text "Minor"\nend if'
        ]
    },
    "loop": {
        "category": "Control Flow",
        "syntax": "do the following N times\n  ...\nend doing",
        "description": "Repeat a block of code N times",
        "examples": [
            'do the following 5 times\n  display the text "Hello"\nend doing'
        ]
    },
    "while": {
        "category": "Control Flow",
        "syntax": "while CONDITION do\n  ...\nend while",
        "description": "Repeat a block while a condition is true",
        "examples": [
            'while x less than 10 do\n  the value of x should be x plus 1\nend while'
        ]
    },
    "function": {
        "category": "Functions",
        "syntax": "create a function called NAME that takes:\n  TYPE ARG\nwith the code:\n  ...\nend function definition",
        "description": "Define a reusable function",
        "examples": [
            'create a function called add that takes:\n  number a\n  number b\nwith the code:\n  give back a plus b\nend function definition'
        ]
    },
    "structure": {
        "category": "Data Types",
        "syntax": "create a structure named NAME with:\n  TYPE field_name\nend structure definition",
        "description": "Define a custom data structure",
        "examples": [
            'create a structure named Person with:\n  string name\n  integer age\nend structure definition'
        ]
    },
    "list": {
        "category": "Collections",
        "syntax": "create list NAME as [item1, item2, ...]",
        "description": "Create an array/list of items",
        "examples": [
            'create list numbers as [1, 2, 3, 4, 5]',
            'create list names as ["Alice", "Bob", "Charlie"]'
        ]
    },
    "try": {
        "category": "Error Handling",
        "syntax": "try\n  ...\ncatch ERROR as VAR\n  ...\nend try",
        "description": "Handle errors with try-catch blocks",
        "examples": [
            'try\n  the value of x should be 10 divided by 0\ncatch error as e\n  display the text "Error: division by zero"\nend try'
        ]
    },
    "break": {
        "category": "Control Flow",
        "syntax": "break",
        "description": "Exit the nearest enclosing loop",
        "examples": [
            'do the following 10 times\n  if x equal to 5 then\n    break\n  end if\nend doing'
        ]
    },
    "mathlib": {
        "category": "Libraries",
        "description": "Mathematical functions library",
        "functions": ["sqrt", "pow", "sin", "cos", "tan", "abs", "floor", "ceil", "round", "min", "max", "mean", "median", "variance"],
        "usage": "Must enable with:  this script uses: mathlib"
    },
    "random": {
        "category": "Libraries",
        "description": "Random number generation library",
        "functions": ["generate a random number from X to Y", "shuffle_list"],
        "usage": "Must enable with: this script uses: random"
    },
    "osrand": {
        "category": "Libraries",
        "description": "Secure OS random number generation",
        "functions": ["generate an os random number", "os random bytes"],
        "usage": "Must enable with: this script uses: osrand"
    },
    "easyio": {
        "category": "Libraries",
        "description": "Easy input/output operations",
        "functions": ["display", "show", "ask"],
        "usage": "Must enable with: this script uses: easyio"
    },
    "syslib": {
        "category": "Libraries",
        "description": "System-level operations (write, read, platform info)",
        "functions": ["sys write", "sys read", "sys get platform"],
        "usage": "Must enable with: this script uses: syslib"
    },
    "strproclib": {
        "category": "Libraries",
        "description": "String processing and manipulation",
        "functions": ["substring", "split", "join", "replace", "uppercase", "lowercase", "trim", "regex_match", "length"],
        "usage": "Must enable with: this script uses: strproclib"
    },
    "operators": {
        "category": "Reference",
        "description": "Comparison and logical operators",
        "comparison": ["equal to", "not equal to", "greater than", "less than", "greater than or equal to", "less than or equal to"],
        "logical": ["and", "or", "not"],
        "arithmetic": ["plus", "minus", "times", "divided by", "modulo"],
        "bitwise": ["bitwise and", "bitwise or", "bitwise xor", "bitwise nor", "bitwise nand", "bitwise xnor", "left shift", "right shift"],
        "boolean": ["bool and", "bool or", "bool xor", "bool nor", "bool nand", "bool xnor", "bool not"]
    },
    "types": {
        "category": "Data Types",
        "description": "Available data types in E#",
        "types": {
            "integer": "Whole numbers (int, integer, whole number)",
            "float": "Decimal numbers (flt, float, decimal number)",
            "string": "Text (str, string, text)",
            "decimal": "High-precision decimals (dec, decimal)",
            "fraction": "Rational numbers (frc, fraction)",
            "bytes": "Binary data (bytes, binary)"
        }
    }
}

VALID_LIBRARIES = {'mathlib', 'random', 'osrand', 'easyio', 'syslib', 'strproclib'}

def display_help(topic):
    """Display help documentation for a topic"""
    topic = topic.lower().strip()
    
    # Handle special cases
    if topic in ["topics", "all", "help", ""]:
        list_documentation_topics()
        return True
    
    # Try exact match first
    if topic in DOCUMENTATION:
        doc = DOCUMENTATION[topic]
        print(f"\n{'=' * 60}")
        print(f"{topic.upper()}")
        print(f"{'=' * 60}")
        
        if "category" in doc:
            print(f"Category: {doc['category']}")
        
        if "description" in doc:
            print(f"\nDescription: {doc['description']}")
        
        if "syntax" in doc:
            print(f"\nSyntax:\n  {doc['syntax']}")
        
        if "types" in doc:
            print(f"\nTypes:")
            for t in doc["types"]:
                print(f"  - {t}")
        
        if "operators" in doc:
            print(f"\nOperators:")
            for op in doc["operators"]:
                print(f"  - {op}")
        
        if "comparison" in doc:
            print(f"\nComparison Operators:")
            for op in doc["comparison"]:
                print(f"  - {op}")
        
        if "logical" in doc:
            print(f"\nLogical Operators:")
            for op in doc["logical"]:
                print(f"  - {op}")
        
        if "arithmetic" in doc:
            print(f"\nArithmetic Operators:")
            for op in doc["arithmetic"]:
                print(f"  - {op}")
        
        if "bitwise" in doc:
            print(f"\nBitwise Operators:")
            for op in doc["bitwise"]:
                print(f"  - {op}")
        
        if "boolean" in doc:
            print(f"\nBoolean Operators:")
            for op in doc["boolean"]:
                print(f"  - {op}")
        
        if "functions" in doc:
            print(f"\nFunctions:")
            for func in doc["functions"]:
                print(f"  - {func}")
        
        if "examples" in doc:
            print(f"\nExamples:")
            for ex in doc["examples"]:
                print(f"  {ex}")
        
        if "usage" in doc:
            print(f"\nUsage: {doc['usage']}")
        
        print(f"\n{'=' * 60}\n")
        return True
    
    # Try partial match
    matches = [key for key in DOCUMENTATION.keys() if topic in key or key in topic]
    if matches:
        print(f"\n No exact match for '{topic}'. Did you mean:")
        for match in matches[:5]:
            print(f"  • {match}")
        print(f"\nType: explain {matches[0]}\n")
        return False
    
    print(f"\n No documentation found for '{topic}'")
    print(f"Type 'explain topics' to see all available topics.\n")
    return False

def list_documentation_topics():
    """List all available documentation topics"""
    categories = {}
    for topic, doc in DOCUMENTATION.items():
        cat = doc.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(topic)
    
    print(f"\n{'=' * 60}")
    print("AVAILABLE DOCUMENTATION TOPICS")
    print(f"{'=' * 60}\n")
    
    for category in sorted(categories.keys()):
        topics = sorted(categories[category])
        print(f"{category}:")
        for topic in topics:
            print(f"   • {topic}")
        print()
    
    print(f"Usage: explain [topic]")
    print(f"{'=' * 60}\n")

# --- Operator Synonyms ---
OPERATOR_SYNONYMS = {
    'more than': 'greater than',
    'bigger than': 'greater than',
    'larger than': 'greater than',
    'smaller than': 'less than',
    'is more than': 'greater than',
    'is greater than': 'greater than',
    'is bigger than': 'greater than',
    'is larger than': 'greater than',
    'is smaller than': 'less than',
    'is less than': 'less than',
    'equals': 'equal to',
    'is equal to': 'equal to',
    'is': 'equal to',
    'does not equal': 'not equal to',
    'is not': 'not equal to',
    '+': 'plus',
    '-': 'minus',
    '*': 'times',
    '/': 'divided by',
    '%': 'modulo',
    # Bitwise operators
    'bitwise and': 'bitwise and',
    'bitwise or': 'bitwise or',
    'bitwise xor': 'bitwise xor',
    'bitwise nor': 'bitwise nor',
    'bitwise not': 'bitwise not',
    'bitwise nand': 'bitwise nand',
    'bitwise xnor': 'bitwise xnor',
    'left shift': 'left shift',
    'right shift': 'right shift',
    '&': 'bitwise and',
    '|': 'bitwise or',
    '^': 'bitwise xor',
    '~': 'bitwise not',
    '<<': 'left shift',
    '>>': 'right shift',
    # Boolean operators
    'bool and': 'bool and',
    'bool or': 'bool or',
    'bool xor': 'bool xor',
    'bool nor': 'bool nor',
    'bool not': 'bool not',
    'bool nand': 'bool nand',
    'bool xnor': 'bool xnor',
}

# --- Global Debug State ---
class DebugState:
    def __init__(self):
        self.breakpoints = set()
        self.step_mode = False
        self.show_vars = False
        self.paused = False

debug_state = DebugState()

# --- Security Constraints ---
class SecurityPolicy:
    def __init__(self):
        self.allow_file_write = True
        self.allow_os_random = True
        self.memory_limit = None
        self.max_execution_time = None

security_policy = SecurityPolicy()

# --- Helper Functions ---
def suggest_correction(token, valid_options):
    """Suggests the closest match for a typo."""
    matches = difflib.get_close_matches(token, valid_options, n=1, cutoff=0.6)
    return matches[0] if matches else None

def raise_error(expectation, line, line_number, original_lines, suggestion=None):
    """Enhanced error reporting with line number, context, and suggestions."""
    context_line = line
    if 0 <= line_number - 1 < len(original_lines):
        context_line = original_lines[line_number - 1]
    error_msg = f"\n[Syntax Error] at line {line_number}:\n"
    error_msg += f"    {context_line}\n"
    error_msg += f"        ^ Unexpected keyword :(\n"
    error_msg += f"I expected: {expectation}\n"
    error_msg += f"But you wrote: {line}"
    if suggestion:
        error_msg += f"\nDid you mean: '{suggestion}'?"
    raise Exception(error_msg)

def remove_filler_words(text):
    """Remove common filler words from text, preserving spaces inside quotes."""
    # Find quoted strings and protect them
    protected = []
    def replace_quotes(match):
        placeholder = f"__PROTECTED_{len(protected)}__"
        protected.append(match.group(0))
        return placeholder
    
    # Temporarily replace quoted strings
    temp_text = re.sub(r'"[^"]*"', replace_quotes, text)
    
    # Process the rest
    words = temp_text.split()
    cleaned = [w for w in words if w.lower() not in FILLER_WORDS]
    result = ' '.join(cleaned)
    
    # Restore quoted strings
    for i, original in enumerate(protected):
        result = result.replace(f"__PROTECTED_{i}__", original)
        
    return result

def normalize_operators(text):
    """Normalize operator synonyms to standard form using word boundaries."""
    normalized = text
    for synonym, standard in OPERATOR_SYNONYMS.items():
        if len(synonym) == 1:
            normalized = normalized.replace(synonym, standard)
        else:
            pattern = r'\b' + re.escape(synonym) + r'\b'
            normalized = re.sub(pattern, standard, normalized, flags=re.IGNORECASE)
    return normalized

def handle_tokens(text, variables):
    def hex_replacer(match):
        hex_codes = match.group(1).split(",")
        chars = ""
        for code in hex_codes:
            code = code.strip()
            if code.startswith("0x") or code.startswith("0X"):
                chars += chr(int(code, 16))
            else:
                chars += chr(int(code, 16))
        return chars
    text = re.sub(r"\[(.*?)\]", hex_replacer, text)
    
    def decimal_replacer(match):
        return chr(int(match.group(1)))
    text = re.sub(r"\((\d+)\)", decimal_replacer, text)
    
    def variable_replacer(match):
        var_name = match.group(1).strip()
        if var_name in variables:
            val = variables[var_name]
            if isinstance(val, bytes):
                return val.decode('utf-8', errors='replace')
            return str(val)
        return match.group(0)
    text = re.sub(r"\{([^}]+)\}", variable_replacer, text)
    return text

def get_value(val, variables):
    val = val.strip()
    if val in variables:
        return variables[val]
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except:
        return val

def convert_to_type(value, type_name):
    type_name = type_name.lower()
    if type_name in ['int', 'integer', 'whole number']:
        return int(float(value))
    elif type_name in ['flt', 'float', 'decimal number']:
        return float(value)
    elif type_name in ['str', 'string', 'text']:
        return str(value)
    elif type_name in ['dec', 'decimal']:
        return Decimal(str(value))
    elif type_name in ['frc', 'fraction']:
        return Fraction(str(value))
    elif type_name in ['bytes', 'binary']:
        if isinstance(value, str):
            return value.encode('utf-8')
        elif isinstance(value, bytes):
            return value
        else:
            return str(value).encode('utf-8')
    else:
        raise Exception(f"Unknown type: {type_name}")

def try_convert_to_number(val):
    if isinstance(val, (int, float, Decimal, Fraction)):
        return val
    if isinstance(val, str):
        val = val.strip()
        try:
            if '.' in val:
                return float(val)
            return int(val)
        except:
            return val
    return val

def evaluate_condition(left, operator, right, variables):
    left_val = get_value(left, variables)
    right_val = get_value(right, variables)
    left_val = try_convert_to_number(left_val)
    right_val = try_convert_to_number(right_val)
    if operator in ['equal to', 'equals']: return left_val == right_val
    elif operator in ['not equal to', 'does not equal']: return left_val != right_val
    elif operator in ['more than', 'greater than']: return left_val > right_val
    elif operator in ['less than', 'smaller than']: return left_val < right_val
    elif operator in ['more than or equal to', 'greater than or equal to']: return left_val >= right_val
    elif operator in ['less than or equal to', 'smaller than or equal to']: return left_val <= right_val
    else: raise Exception(f"Unknown operator: {operator}")

def safe_numeric_operation(val):
    """Preserves Decimal/Fraction precision, falls back to float."""
    if isinstance(val, (Decimal, Fraction)):
        return val
    try:
        return float(val)
    except:
        return val

def normalize_number(val):
    """Converts floats representing integers back to integers."""
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val

def get_return_value(value_str, variables):
    """Properly handles return values - variables, strings, or numbers."""
    value_str = value_str.strip()
    if value_str.startswith('"') and value_str.endswith('"'):
        return handle_tokens(value_str[1:-1], variables)
    if value_str in variables:
        return variables[value_str]
    try:
        if '.' in value_str:
            return float(value_str)
        return int(value_str)
    except:
        return value_str

# --- Structure Support ---
class ESharpStruct:
    """Represents a user-defined structure/record in E#"""
    def __init__(self, name, fields, field_types):
        self.name = name
        self.fields = fields
        self.field_types = field_types
        self.values = {f: None for f in fields}
    
    def set_field(self, field_name, value):
        if field_name not in self.fields:
            raise Exception(f"Field '{field_name}' not found in structure '{self.name}'")
        self.values[field_name] = value
    
    def get_field(self, field_name):
        if field_name not in self.fields:
            raise Exception(f"Field '{field_name}' not found in structure '{self.name}'")
        return self.values[field_name]
    
    def __repr__(self):
        items = ", ".join([f"{k}: {self.values[k]}" for k in self.fields])
        return f"{self.name}({items})"

# --- Array/List Support ---
class ESharpList:
    """Represents a list/array in E#"""
    def __init__(self, items=None):
        self.items = items if items else []
    
    def append(self, item):
        self.items.append(item)
    
    def get_at(self, index):
        try:
            return self.items[int(index)]
        except (IndexError, ValueError):
            raise Exception(f"Index {index} out of bounds for list of length {len(self.items)}")
    
    def set_at(self, index, value):
        try:
            self.items[int(index)] = value
        except (IndexError, ValueError):
            raise Exception(f"Index {index} out of bounds for list of length {len(self.items)}")
    
    def length(self):
        return len(self.items)
    
    def __repr__(self):
        return f"[{', '.join(str(i) for i in self.items)}]"

# --- Libraries ---
class Mathlib:
    @staticmethod
    def add(x, y, variables, output_var):
        vx = safe_numeric_operation(get_value(x, variables))
        vy = safe_numeric_operation(get_value(y, variables))
        if isinstance(vx, (Decimal, Fraction)) and isinstance(vy, (Decimal, Fraction)) and type(vx) == type(vy):
            variables[output_var] = normalize_number(vx + vy)
        else:
            variables[output_var] = normalize_number(float(vx) + float(vy))

    @staticmethod
    def sub(x, y, variables, output_var):
        vx = safe_numeric_operation(get_value(x, variables))
        vy = safe_numeric_operation(get_value(y, variables))
        if isinstance(vx, (Decimal, Fraction)) and isinstance(vy, (Decimal, Fraction)) and type(vx) == type(vy):
            variables[output_var] = normalize_number(vx - vy)
        else:
            variables[output_var] = normalize_number(float(vx) - float(vy))

    @staticmethod
    def mul(x, y, variables, output_var):
        vx = safe_numeric_operation(get_value(x, variables))
        vy = safe_numeric_operation(get_value(y, variables))
        if isinstance(vx, (Decimal, Fraction)) and isinstance(vy, (Decimal, Fraction)) and type(vx) == type(vy):
            variables[output_var] = normalize_number(vx * vy)
        else:
            variables[output_var] = normalize_number(float(vx) * float(vy))

    @staticmethod
    def div(x, y, variables, output_var):
        vx = safe_numeric_operation(get_value(x, variables))
        vy = safe_numeric_operation(get_value(y, variables))
        if isinstance(vx, (Decimal, Fraction)) and isinstance(vy, (Decimal, Fraction)) and type(vx) == type(vy):
            variables[output_var] = normalize_number(vx / vy)
        else:
            variables[output_var] = normalize_number(float(vx) / float(vy))

    @staticmethod
    def mod(x, y, variables, output_var):
        variables[output_var] = normalize_number(float(get_value(x, variables)) % float(get_value(y, variables)))

    @staticmethod
    def sqrt(x, variables, output_var):
        variables[output_var] = normalize_number(math.sqrt(float(get_value(x, variables))))

    @staticmethod
    def log(x, variables, output_var):
        variables[output_var] = normalize_number(math.log(float(get_value(x, variables))))

    @staticmethod
    def pow(base, exp, variables, output_var):
        variables[output_var] = normalize_number(math.pow(float(get_value(base, variables)), float(get_value(exp, variables))))

    @staticmethod
    def sin(x, variables, output_var):
        variables[output_var] = normalize_number(math.sin(math.radians(float(get_value(x, variables)))))

    @staticmethod
    def cos(x, variables, output_var):
        variables[output_var] = normalize_number(math.cos(math.radians(float(get_value(x, variables)))))

    @staticmethod
    def tan(x, variables, output_var):
        variables[output_var] = normalize_number(math.tan(math.radians(float(get_value(x, variables)))))

    @staticmethod
    def asin(x, variables, output_var):
        variables[output_var] = normalize_number(math.degrees(math.asin(float(get_value(x, variables)))))

    @staticmethod
    def acos(x, variables, output_var):
        variables[output_var] = normalize_number(math.degrees(math.acos(float(get_value(x, variables)))))

    @staticmethod
    def atan(x, variables, output_var):
        variables[output_var] = normalize_number(math.degrees(math.atan(float(get_value(x, variables)))))

    @staticmethod
    def abs(x, variables, output_var):
        variables[output_var] = normalize_number(abs(float(get_value(x, variables))))

    @staticmethod
    def floor(x, variables, output_var):
        variables[output_var] = normalize_number(math.floor(float(get_value(x, variables))))

    @staticmethod
    def ceil(x, variables, output_var):
        variables[output_var] = normalize_number(math.ceil(float(get_value(x, variables))))

    @staticmethod
    def round_func(x, variables, output_var):
        variables[output_var] = normalize_number(round(float(get_value(x, variables))))

    @staticmethod
    def factorial(x, variables, output_var):
        variables[output_var] = normalize_number(math.factorial(int(float(get_value(x, variables)))))

    @staticmethod
    def min(x, y, variables, output_var):
        variables[output_var] = normalize_number(min(float(get_value(x, variables)), float(get_value(y, variables))))

    @staticmethod
    def max(x, y, variables, output_var):
        variables[output_var] = normalize_number(max(float(get_value(x, variables)), float(get_value(y, variables))))

    @staticmethod
    def mean(numbers_var, variables, output_var):
        nums_list = get_value(numbers_var, variables)
        if isinstance(nums_list, ESharpList):
            nums = [float(x) for x in nums_list.items]
        else:
            nums = [float(x) for x in nums_list]
        variables[output_var] = normalize_number(stats_module.mean(nums))

    @staticmethod
    def median(numbers_var, variables, output_var):
        nums_list = get_value(numbers_var, variables)
        if isinstance(nums_list, ESharpList):
            nums = [float(x) for x in nums_list.items]
        else:
            nums = [float(x) for x in nums_list]
        variables[output_var] = normalize_number(stats_module.median(nums))

    @staticmethod
    def variance(numbers_var, variables, output_var):
        nums_list = get_value(numbers_var, variables)
        if isinstance(nums_list, ESharpList):
            nums = [float(x) for x in nums_list.items]
        else:
            nums = [float(x) for x in nums_list]
        variables[output_var] = normalize_number(stats_module.variance(nums))

    # --- Bitwise Operations ---
    @staticmethod
    def bitwise_and(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = vx & vy

    @staticmethod
    def bitwise_or(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = vx | vy

    @staticmethod
    def bitwise_xor(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = vx ^ vy

    @staticmethod
    def bitwise_nor(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = ~(vx | vy)

    @staticmethod
    def bitwise_nand(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = ~(vx & vy)

    @staticmethod
    def bitwise_xnor(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = ~(vx ^ vy)

    @staticmethod
    def bitwise_not(x, variables, output_var):
        vx = int(float(get_value(x, variables)))
        variables[output_var] = ~vx

    @staticmethod
    def left_shift(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = vx << vy

    @staticmethod
    def right_shift(x, y, variables, output_var):
        vx = int(float(get_value(x, variables)))
        vy = int(float(get_value(y, variables)))
        variables[output_var] = vx >> vy

    # --- Boolean Operations ---
    @staticmethod
    def bool_and(x, y, variables, output_var):
        vx = bool(get_value(x, variables))
        vy = bool(get_value(y, variables))
        variables[output_var] = int(vx and vy)

    @staticmethod
    def bool_or(x, y, variables, output_var):
        vx = bool(get_value(x, variables))
        vy = bool(get_value(y, variables))
        variables[output_var] = int(vx or vy)

    @staticmethod
    def bool_xor(x, y, variables, output_var):
        vx = bool(get_value(x, variables))
        vy = bool(get_value(y, variables))
        variables[output_var] = int(vx != vy)

    @staticmethod
    def bool_nor(x, y, variables, output_var):
        vx = bool(get_value(x, variables))
        vy = bool(get_value(y, variables))
        variables[output_var] = int(not (vx or vy))

    @staticmethod
    def bool_nand(x, y, variables, output_var):
        vx = bool(get_value(x, variables))
        vy = bool(get_value(y, variables))
        variables[output_var] = int(not (vx and vy))

    @staticmethod
    def bool_xnor(x, y, variables, output_var):
        vx = bool(get_value(x, variables))
        vy = bool(get_value(y, variables))
        variables[output_var] = int(vx == vy)

    @staticmethod
    def bool_not(x, variables, output_var):
        vx = bool(get_value(x, variables))
        variables[output_var] = int(not vx)

class Strproclib:
    """String Processing Library"""
    @staticmethod
    def substring(text_var, start, end, variables, output_var):
        text = str(get_value(text_var, variables))
        s = int(get_value(start, variables))
        e = int(get_value(end, variables))
        variables[output_var] = text[s:e]

    @staticmethod
    def split(text_var, delimiter, variables, output_var):
        text = str(get_value(text_var, variables))
        delim = str(get_value(delimiter, variables))
        parts = text.split(delim)
        variables[output_var] = ESharpList(parts)

    @staticmethod
    def join(list_var, delimiter, variables, output_var):
        lst = get_value(list_var, variables)
        delim = str(get_value(delimiter, variables))
        if isinstance(lst, ESharpList):
            result = delim.join(str(x) for x in lst.items)
        else:
            result = delim.join(str(x) for x in lst)
        variables[output_var] = result

    @staticmethod
    def replace(text_var, old, new, variables, output_var):
        text = str(get_value(text_var, variables))
        old_str = str(get_value(old, variables))
        new_str = str(get_value(new, variables))
        variables[output_var] = text.replace(old_str, new_str)

    @staticmethod
    def uppercase(text_var, variables, output_var):
        text = str(get_value(text_var, variables))
        variables[output_var] = text.upper()

    @staticmethod
    def lowercase(text_var, variables, output_var):
        text = str(get_value(text_var, variables))
        variables[output_var] = text.lower()

    @staticmethod
    def trim(text_var, variables, output_var):
        text = str(get_value(text_var, variables))
        variables[output_var] = text.strip()

    @staticmethod
    def regex_match(text_var, pattern, variables, output_var):
        text = str(get_value(text_var, variables))
        pat = str(get_value(pattern, variables))
        match = re.search(pat, text)
        variables[output_var] = bool(match)

    @staticmethod
    def length(text_var, variables, output_var):
        text = str(get_value(text_var, variables))
        variables[output_var] = len(text)

class Syslib:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else "clear")

    @staticmethod
    def stdout_write(text, variables):
        text = handle_tokens(text, variables)
        sys.stdout.write(text)

    @staticmethod
    def stdout_flush():
        sys.stdout.flush()

    @staticmethod
    def stdin_read(echo, variables, output_var):
        if echo:
            sys.stdout.flush()
            value = sys.stdin.readline().rstrip('\n')
        else:
            value = getpass.getpass("")
        variables[output_var] = value

    @staticmethod
    def get_platform(variables, output_var):
        variables[output_var] = sys.platform

class Easyio:
    @staticmethod
    def print_func(text, variables, kwargs=None):
        if kwargs is None: kwargs = {}
        text = handle_tokens(text, variables)
        end = kwargs.get('end', '\n')
        flush = kwargs.get('flush', False)
        sys.stdout.write(text + end)
        if flush: sys.stdout.flush()

    @staticmethod
    def input_func(prompt, variables, output_var):
        prompt = handle_tokens(prompt, variables)
        sys.stdout.write(prompt)
        sys.stdout.flush()
        value = sys.stdin.readline().rstrip('\n')
        variables[output_var] = value

class Timelib:
    @staticmethod
    def sleep(time_):
        time.sleep(time_)

    @staticmethod
    def get_timestamp(variables, output_var):
        variables[output_var] = int(datetime.now().timestamp())

    @staticmethod
    def format_date(timestamp, format_str, variables, output_var):
        ts = int(get_value(timestamp, variables))
        fmt = str(get_value(format_str, variables))
        dt = datetime.fromtimestamp(ts)
        variables[output_var] = dt.strftime(fmt)

class Fileio:
    @staticmethod
    def read_file(filename, path, encoding, variables, output_var):
        full_path = os.path.join(path, filename)
        try:
            with open(full_path, 'r', encoding=encoding) as f:
                content = f.read()
            variables[output_var] = content
        except Exception as e:
            raise Exception(f"Failed to read file: {e}")

    @staticmethod
    def write_file(content, filename, path, encoding, variables):
        if not security_policy.allow_file_write:
            raise Exception("File writing is disabled by security policy")
        full_path = os.path.join(path, filename)
        try:
            os.makedirs(path, exist_ok=True)
            with open(full_path, 'w', encoding=encoding) as f:
                f.write(str(content))
        except Exception as e:
            raise Exception(f"Failed to write file: {e}")

    @staticmethod
    def delete_file(filename, path, variables):
        if not security_policy.allow_file_write:
            raise Exception("File deletion is disabled by security policy")
        full_path = os.path.join(path, filename)
        try:
            os.remove(full_path)
        except Exception as e:
            raise Exception(f"Failed to delete file: {e}")

    @staticmethod
    def list_files(path, variables, output_var):
        try:
            files = os.listdir(path)
            variables[output_var] = ESharpList(files)
        except Exception as e:
            raise Exception(f"Failed to list files: {e}")

    @staticmethod
    def create_directory(path, variables):
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            raise Exception(f"Failed to create directory: {e}")

    @staticmethod
    def move_file(src, src_path, dst, dst_path, variables):
        try:
            full_src = os.path.join(src_path, src)
            full_dst = os.path.join(dst_path, dst)
            os.makedirs(dst_path, exist_ok=True)
            import shutil
            shutil.move(full_src, full_dst)
        except Exception as e:
            raise Exception(f"Failed to move file: {e}")

class Randlib:
    @staticmethod
    def generate_int(min_val, max_val, variables, output_var):
        variables[output_var] = random.randint(int(min_val), int(max_val))

    @staticmethod
    def generate_bytes(count, variables, output_var):
        b = bytes([random.randint(0, 255) for _ in range(int(count))])
        variables[output_var] = b

    @staticmethod
    def shuffle_list(list_var, variables, output_var):
        lst = get_value(list_var, variables)
        if isinstance(lst, ESharpList):
            shuffled = lst.items.copy()
            random.shuffle(shuffled)
            variables[output_var] = ESharpList(shuffled)
        else:
            shuffled = list(lst)
            random.shuffle(shuffled)
            variables[output_var] = ESharpList(shuffled)

    @staticmethod
    def weighted_choice(items_var, weights_var, variables, output_var):
        items = get_value(items_var, variables)
        weights = get_value(weights_var, variables)
        if isinstance(items, ESharpList):
            items = items.items
        if isinstance(weights, ESharpList):
            weights = weights.items
        weights = [float(w) for w in weights]
        variables[output_var] = random.choices(items, weights=weights, k=1)[0]

class Osrandlib:
    @staticmethod
    def generate_int(min_val, max_val, variables, output_var):
        if not security_policy.allow_os_random:
            raise Exception("OS random is disabled by security policy")
        sec_random = random.SystemRandom()
        variables[output_var] = sec_random.randint(int(min_val), int(max_val))

    @staticmethod
    def generate_bytes(count, variables, output_var):
        if not security_policy.allow_os_random:
            raise Exception("OS random is disabled by security policy")
        b = os.urandom(int(count))
        variables[output_var] = b

# --- Parsing & Validation ---
def remove_comments(text):
    lines = text.splitlines()
    cleaned = []
    for i, line in enumerate(lines):
        original_num = i + 1
        line = re.sub(r"::.*?::", "", line, flags=re.DOTALL)
        cleaned.append((original_num, line))
    return cleaned

class FunctionReturn(Exception):
    def __init__(self, value):
        self.value = value

class ProgramExit(Exception):
    """Raised by 'end program' to immediately terminate execution."""
    pass

class LoopBreak(Exception):
    """Raised by 'break' to exit the nearest enclosing loop."""
    def __init__(self, line=None, line_num=0, original_lines=None):
        self.line = line
        self.line_num = line_num
        self.original_lines = original_lines or []

class CatchException(Exception):
    """Raised by catch blocks"""
    def __init__(self, error_msg):
        self.error_msg = error_msg

def parse_condition(condition_str):
    condition_str = remove_filler_words(condition_str)
    condition_str = normalize_operators(condition_str)
    english_operators = [
        "greater than or equal to",
        "less than or equal to",
        "not equal to",
        "equal to",
        "greater than",
        "less than"
    ]
    operator = None
    left = None
    right = None
    for op in english_operators:
        if op in condition_str:
            operator = op
            parts = condition_str.split(op, 1)
            left = parts[0].strip()
            right = parts[1].strip()
            break
    return left, operator, right

def parse_boolean_condition(condition_str, variables):
    """Parse conditions with boolean algebra (and, or, not)."""
    condition_str = remove_filler_words(condition_str)
    condition_str = normalize_operators(condition_str)
    if ' or ' in condition_str:
        parts = condition_str.split(' or ', 1)
        left_result = parse_boolean_condition(parts[0].strip(), variables)
        right_result = parse_boolean_condition(parts[1].strip(), variables)
        return left_result or right_result
    if ' and ' in condition_str:
        parts = condition_str.split(' and ', 1)
        left_result = parse_boolean_condition(parts[0].strip(), variables)
        right_result = parse_boolean_condition(parts[1].strip(), variables)
        return left_result and right_result
    if condition_str.startswith('not '):
        inner_result = parse_boolean_condition(condition_str[4:].strip(), variables)
        return not inner_result
    left, operator, right = parse_condition(condition_str)
    if operator:
        return evaluate_condition(left, operator, right, variables)
    if condition_str in variables:
        return bool(variables[condition_str])
    raise Exception(f"Could not parse condition: {condition_str}")

def validate_syntax(lines_with_nums):
    if_stack = []
    loop_stack = []
    while_stack = []
    func_stack = []
    struct_stack = []
    try_stack = []
    
    for line_num, line in lines_with_nums:
        line = line.strip()
        if not line:
            continue
        if line.startswith("if ") and ("then" in line or ":" in line):
            if_stack.append(line_num)
        elif line.startswith("end if"):
            if not if_stack:
                raise_error("matching 'if'", "end if", line_num, [l[1] for l in lines_with_nums])
            if_stack.pop()
        elif line.startswith("do the following"):
            loop_stack.append(line_num)
        elif line.startswith("end doing"):
            if not loop_stack:
                raise_error("matching 'do the following'", "end doing", line_num, [l[1] for l in lines_with_nums])
            loop_stack.pop()
        elif line.startswith("while ") and ("do" in line or ":" in line):
            while_stack.append(line_num)
        elif line.startswith("end while"):
            if not while_stack:
                raise_error("matching 'while'", "end while", line_num, [l[1] for l in lines_with_nums])
            while_stack.pop()
        elif line.startswith("create a function"):
            func_stack.append(line_num)
        elif line.startswith("end function definition"):
            if not func_stack:
                raise_error("matching 'create a function'", "end function definition", line_num, [l[1] for l in lines_with_nums])
            func_stack.pop()
        elif line.startswith("create a structure"):
            struct_stack.append(line_num)
        elif line.startswith("end structure definition"):
            if not struct_stack:
                raise_error("matching 'create a structure'", "end structure definition", line_num, [l[1] for l in lines_with_nums])
            struct_stack.pop()
        elif line.startswith("try"):
            try_stack.append(line_num)
        elif line.startswith("end try"):
            if not try_stack:
                raise_error("matching 'try'", "end try", line_num, [l[1] for l in lines_with_nums])
            try_stack.pop()

    if if_stack:
        raise_error("block to be closed with 'end if'", "if...", if_stack[-1], [l[1] for l in lines_with_nums])
    if loop_stack:
        raise_error("block to be closed with 'end doing'", "do the following...", loop_stack[-1], [l[1] for l in lines_with_nums])
    if while_stack:
        raise_error("block to be closed with 'end while'", "while...", while_stack[-1], [l[1] for l in lines_with_nums])
    if func_stack:
        raise_error("block to be closed with 'end function definition'", "create a function...", func_stack[-1], [l[1] for l in lines_with_nums])
    if struct_stack:
        raise_error("block to be closed with 'end structure definition'", "create a structure...", struct_stack[-1], [l[1] for l in lines_with_nums])
    if try_stack:
        raise_error("block to be closed with 'end try'", "try...", try_stack[-1], [l[1] for l in lines_with_nums])

def first_pass_analysis(lines_with_nums, original_lines):
    """First pass validation - checks all identifiers BEFORE execution."""
    defined_vars = set()
    defined_funcs = set()
    defined_structs = set()
    enabled_libs = set()
    
    for line_num, line in lines_with_nums:
        line = line.strip()
        if not line:
            continue
        line = remove_filler_words(line)
        
        if line.startswith("this script uses"):
            libs_match = re.search(r'(?:libraries:|uses:)\s*(.+?)(?:\n|$)', line)
            if libs_match:
                libs_str = libs_match.group(1)
                libs = re.findall(r'\b(\w+)\b', libs_str)
                for lib in libs:
                    if lib.lower() not in ['the', 'and', 'libraries', 'uses']:
                        # Validate library name
                        if lib.lower() not in VALID_LIBRARIES:
                            raise_error(
                                f"a valid library name ({', '.join(sorted(VALID_LIBRARIES))})", 
                                line, 
                                line_num, 
                                original_lines
                            )
                        enabled_libs.add(lib.lower())
            else:
                # ERROR IF COLON IS MISSING
                raise_error(
                    "a colon after 'uses' or 'libraries' (e.g., 'this script uses: mathlib')", 
                    line, 
                    line_num, 
                    original_lines
                )
        elif line.startswith("the number") or line.startswith("the text") or line.startswith("the value of"):
            var_match = re.match(r'the\s+(number|text|value\s+of\s+\w+)\s+(\w+)\s+is\s+(.+?)\s+and\s+it\s+should\s+be\s+(\w+)', line)
            if var_match:
                defined_vars.add(var_match.group(2))
        elif line.startswith("create a function"):
            func_match = re.match(r'create\s+a\s+function\s+called\s+(\w+)', line)
            if func_match:
                defined_funcs.add(func_match.group(1))
        elif line.startswith("create a structure"):
            struct_match = re.match(r'create\s+a\s+structure\s+named\s+(\w+)', line)
            if struct_match:
                defined_structs.add(struct_match.group(1))

def execute_block(lines_with_nums, variables, allowed_libs, functions=None, structures=None, in_function=False, original_lines=None):
    if functions is None: functions = {}
    if structures is None: structures = {}
    if original_lines is None: original_lines = [l[1] for l in lines_with_nums]
    
    idx = 0
    while idx < len(lines_with_nums):
        line_num, line = lines_with_nums[idx]
        line = line.strip()
        if not line:
            idx += 1
            continue
        
        clean_line = remove_filler_words(line)

        # Debug breakpoint
        if line_num in debug_state.breakpoints:
            print(f"\n[DEBUG] Breakpoint at line {line_num}")
            print(f"Current variables: {variables}")
            debug_state.paused = True

        # End Program
        if clean_line == "end program":
            raise ProgramExit()

        # Break (exit nearest loop)
        elif clean_line == "break" or clean_line == "break loop":
            raise LoopBreak(line=line, line_num=line_num, original_lines=original_lines)

        # Return/Give Back
        elif clean_line.startswith("give back"):
            if not in_function:
                raise_error("to be inside a function when using give back", line, line_num, original_lines)
            value_str = re.sub(r"^give back\s+", "", clean_line).strip()
            value = get_return_value(value_str, variables)
            raise FunctionReturn(value)

        # Explain command (FULLY FUNCTIONAL)
        elif clean_line.startswith("explain"):
            explain_match = re.match(r'explain\s+(.+)', clean_line)
            if explain_match:
                topic = explain_match.group(1).strip()
                display_help(topic)
            else:
                display_help("")
            idx += 1
            continue

        # Debug command
        elif clean_line.startswith("debug"):
            debug_match = re.match(r'debug\s+(\w+)', clean_line)
            if debug_match:
                action = debug_match.group(1).lower()
                if action == "start":
                    debug_state.step_mode = True
                    print("[DEBUG] Debug mode started")
                elif action == "step":
                    print("[DEBUG] Step execution")
                elif action == "show":
                    print(f"[DEBUG] Variables: {variables}")
                elif action == "break":
                    line_match = re.match(r'debug\s+break\s+at\s+line\s+(\d+)', clean_line)
                    if line_match:
                        debug_state.breakpoints.add(int(line_match.group(1)))
                        print(f"[DEBUG] Breakpoint set at line {line_match.group(1)}")
            idx += 1
            continue

        # Structure Definition (FIXED for multi-line support)
        elif clean_line.startswith("create a structure"):
            struct_match = re.match(r'create\s+a\s+structure\s+named\s+(\w+)', clean_line)
            if struct_match:
                struct_name = struct_match.group(1)
                fields = []
                types = []
                idx += 1
                while idx < len(lines_with_nums):
                    inner_num, inner = lines_with_nums[idx]
                    inner_clean = remove_filler_words(inner.strip())
                    if inner_clean.startswith("end structure definition"):
                        break
                    if inner_clean:
                        field_match = re.match(r'(\w+)\s+(\w+)', inner_clean)
                        if field_match:
                            field_type = field_match.group(1)
                            field_name = field_match.group(2)
                            types.append(field_type)
                            fields.append(field_name)
                    idx += 1
                structures[struct_name] = {'fields': fields, 'types': types}
            idx += 1
            continue

        # List/Array Creation
        elif clean_line.startswith("create list") or clean_line.startswith("create array"):
            list_match = re.match(r'create\s+(?:list|array)\s+(\w+)\s+as\s+\[(.*?)\]', clean_line)
            if list_match:
                list_name = list_match.group(1)
                items_str = list_match.group(2)
                items = [x.strip() for x in items_str.split(',')]
                parsed_items = []
                for item in items:
                    parsed_items.append(get_value(item, variables))
                variables[list_name] = ESharpList(parsed_items)
            idx += 1
            continue

        # Try-Catch
        elif clean_line.startswith("try"):
            try_body = []
            catch_block = None
            idx += 1
            while idx < len(lines_with_nums):
                inner_num, inner = lines_with_nums[idx]
                inner_clean = remove_filler_words(inner.strip())
                if inner_clean.startswith("catch"):
                    catch_match = re.match(r'catch\s+(\w+)\s+as\s+(\w+)', inner_clean)
                    if catch_match:
                        error_type = catch_match.group(1)
                        error_var = catch_match.group(2)
                        catch_body = []
                        idx += 1
                        while idx < len(lines_with_nums):
                            inner2_num, inner2 = lines_with_nums[idx]
                            inner2_clean = remove_filler_words(inner2.strip())
                            if inner2_clean.startswith("end try"):
                                catch_block = {'type': error_type, 'var': error_var, 'body': catch_body}
                                break
                            catch_body.append(lines_with_nums[idx])
                            idx += 1
                        break
                elif inner_clean.startswith("end try"):
                    break
                try_body.append(lines_with_nums[idx])
                idx += 1
            
            try:
                execute_block(try_body, variables, allowed_libs.copy(), functions, structures, in_function, original_lines)
            except Exception as e:
                if catch_block:
                    variables[catch_block['var']] = str(e)
                    execute_block(catch_block['body'], variables, allowed_libs.copy(), functions, structures, in_function, original_lines)
                else:
                    raise
            idx += 1
            continue

        # Function Definition
        elif clean_line.startswith("create a function"):
            func_match = re.match(r'create\s+a\s+function\s+called\s+(\w+)\s+that\s+takes:', clean_line)
            if not func_match:
                raise_error("a function definition like: create a function called name that takes:", line, line_num, original_lines)
            func_name = func_match.group(1)
            arg_names = []
            arg_types = []
            idx += 1
            
            # Collect argument lines until we see "with the code:"
            while idx < len(lines_with_nums):
                arg_num, arg_line = lines_with_nums[idx]
                arg_clean = remove_filler_words(arg_line.strip())
                if arg_clean.startswith("with the code:"):
                    break
                if arg_clean:
                    # Parse argument line: "number A as an integer" or "text B as a string"
                    arg_match = re.match(r'(\w+)\s+(\w+)\s+as\s+(?:an?\s+)?(.+)', arg_clean)
                    if arg_match:
                        arg_type = arg_match.group(1).lower()
                        arg_name = arg_match.group(2)
                        arg_full_type = arg_match.group(3).lower()
                        arg_names.append(arg_name)
                        arg_types.append(arg_full_type)
                idx += 1
            
            # Now collect function body
            func_body = []
            idx += 1
            depth = 1
            while idx < len(lines_with_nums):
                inner_num, inner = lines_with_nums[idx]
                inner_clean = remove_filler_words(inner.strip())
                if inner_clean.startswith("create a function"):
                    depth += 1
                elif inner_clean.startswith("end function definition"):
                    depth -= 1
                    if depth == 0:
                        break
                func_body.append(lines_with_nums[idx])
                idx += 1
            if depth != 0:
                raise_error("the function to be closed with 'end function definition'", line, line_num, original_lines)
            functions[func_name] = {
                'args': arg_names,
                'types': arg_types,
                'body': func_body
            }

        # Function Call
        elif clean_line.startswith("run the function") or clean_line.startswith("execute"):
            func_match = re.match(r'(?:run the function|execute)\s+(\w+)\s+with\s+(.+?)\s+saving\s+the\s+result\s+in\s+(\w+)', clean_line)
            if func_match:
                func_name = func_match.group(1)
                args_str = func_match.group(2).strip()
                output_var = func_match.group(3).strip()
                if func_name not in functions:
                    raise_error(f"a function named '{func_name}' to be defined before calling it", line, line_num, original_lines)
                func_def = functions[func_name]
                call_args = [a.strip() for a in args_str.split(",")]
                if len(call_args) != len(func_def['args']):
                    raise_error(f"{len(func_def['args'])} arguments for this function, but you gave {len(call_args)}", line, line_num, original_lines)
                func_scope = variables.copy()
                for i, (arg_name, expected_type) in enumerate(zip(func_def['args'], func_def['types'])):
                    raw_value = call_args[i]
                    val = get_value(raw_value, variables)
                    try:
                        converted_val = convert_to_type(val, expected_type)
                        func_scope[arg_name] = converted_val
                    except Exception as e:
                        raise_error(f"argument '{arg_name}' to be type {expected_type}, but got an error: {e}", line, line_num, original_lines)
                try:
                    execute_block(func_def['body'], func_scope, allowed_libs.copy(), functions, structures, in_function=True, original_lines=original_lines)
                    variables[output_var] = ""
                except FunctionReturn as ret:
                    variables[output_var] = ret.value
                except LoopBreak:
                    raise_error("'break' to be used inside a loop, not inside a function", line, line_num, original_lines)

        # Conditional (If)
        elif clean_line.startswith("if ") and ("then" in clean_line or ":" in clean_line):
            condition_str = re.sub(r'^if\s+', '', clean_line)
            condition_str = re.sub(r'\s+(then|:).*$', '', condition_str).strip()
            try:
                condition_result = parse_boolean_condition(condition_str, variables)
            except Exception as e:
                raise_error(f"a valid condition, but got: {e}", line, line_num, original_lines)
            if_body = []
            elif_blocks = []
            else_body = []
            idx += 1
            depth = 1
            current_block = if_body
            while idx < len(lines_with_nums):
                inner_num, inner = lines_with_nums[idx]
                inner_clean = remove_filler_words(inner.strip())
                if inner_clean.startswith("if "):
                    depth += 1
                    current_block.append(lines_with_nums[idx])
                elif inner_clean.startswith("otherwise if ") and depth == 1:
                    elif_str = re.sub(r'^otherwise if\s+', '', inner_clean)
                    elif_str = re.sub(r'\s+(then|:).*$', '', elif_str).strip()
                    current_block = []
                    elif_blocks.append({'condition': elif_str, 'body': current_block})
                elif inner_clean.startswith("otherwise") and depth == 1:
                    current_block = else_body
                elif inner_clean.startswith("end if"):
                    depth -= 1
                    if depth == 0:
                        break
                    current_block.append(lines_with_nums[idx])
                else:
                    current_block.append(lines_with_nums[idx])
                idx += 1
            if depth != 0:
                raise_error("the condition to be closed with 'end if'", line, line_num, original_lines)
            if condition_result:
                execute_block(if_body, variables, allowed_libs.copy(), functions, structures, in_function, original_lines)
            else:
                executed = False
                for eb in elif_blocks:
                    try:
                        cond_met = parse_boolean_condition(eb['condition'], variables)
                    except Exception:
                        cond_met = False
                    if cond_met:
                        execute_block(eb['body'], variables, allowed_libs.copy(), functions, structures, in_function, original_lines)
                        executed = True
                        break
                if not executed and else_body:
                    execute_block(else_body, variables, allowed_libs.copy(), functions, structures, in_function, original_lines)

        # Fixed-count Loop
        elif clean_line.startswith("do the following"):
            loop_match = re.match(r'do\s+the\s+following\s+(\d+)\s+times', clean_line)
            if not loop_match:
                raise_error("a loop statement like: do the following N times", line, line_num, original_lines)
            amount = int(loop_match.group(1))
            loop_body = []
            idx += 1
            depth = 1
            while idx < len(lines_with_nums):
                inner_num, inner = lines_with_nums[idx]
                inner_clean = remove_filler_words(inner.strip())
                if inner_clean.startswith("do the following"):
                    depth += 1
                    loop_body.append(lines_with_nums[idx])
                elif inner_clean.startswith("end doing"):
                    depth -= 1
                    if depth == 0:
                        break
                    loop_body.append(lines_with_nums[idx])
                else:
                    loop_body.append(lines_with_nums[idx])
                idx += 1
            if depth != 0:
                raise_error("the loop to be closed with 'end doing'", line, line_num, original_lines)
            for _ in range(amount):
                try:
                    execute_block(loop_body, variables, allowed_libs.copy(), functions, structures, in_function, original_lines)
                except LoopBreak:
                    break

        # While Loop
        elif clean_line.startswith("while ") and ("do" in clean_line or ":" in clean_line):
            condition_str = re.sub(r'^while\s+', '', clean_line)
            condition_str = re.sub(r'\s+(do\s*:?|:)\s*$', '', condition_str).strip()
            while_body = []
            idx += 1
            depth = 1
            while idx < len(lines_with_nums):
                inner_num, inner = lines_with_nums[idx]
                inner_clean = remove_filler_words(inner.strip())
                if inner_clean.startswith("while ") and ("do" in inner_clean or ":" in inner_clean):
                    depth += 1
                    while_body.append(lines_with_nums[idx])
                elif inner_clean.startswith("end while"):
                    depth -= 1
                    if depth == 0:
                        break
                    while_body.append(lines_with_nums[idx])
                else:
                    while_body.append(lines_with_nums[idx])
                idx += 1
            if depth != 0:
                raise_error("the while loop to be closed with 'end while'", line, line_num, original_lines)
            try:
                while parse_boolean_condition(condition_str, variables):
                    try:
                        execute_block(while_body, variables, allowed_libs.copy(), functions, structures, in_function, original_lines)
                    except LoopBreak:
                        break
            except (ProgramExit, LoopBreak):
                raise
            except Exception as e:
                raise_error(f"a valid condition inside 'while', but got: {e}", line, line_num, original_lines)

        # Library Enable
        elif clean_line.startswith("this script uses"):
            libs_match = re.search(r'(?:libraries:|uses:)\s*(.+?)(?:\n|$)', clean_line)
            if libs_match:
                libs_str = libs_match.group(1)
                libs = re.findall(r'\b(\w+)\b', libs_str)
                for lib in libs:
                    if lib.lower() not in ['the', 'and', 'libraries', 'uses']:
                        # Validate library name
                        if lib.lower() not in VALID_LIBRARIES:
                            raise_error(
                                f"a valid library name ({', '.join(sorted(VALID_LIBRARIES))})", 
                                line, 
                                line_num, 
                                original_lines
                            )
                        allowed_libs.add(lib.lower())
            else:
                # ERROR IF COLON IS MISSING
                raise_error(
                    "a colon after 'uses' or 'libraries' (e.g., 'this script uses: mathlib')", 
                    line, 
                    line_num, 
                    original_lines
                )

        # Variable Declaration
        elif clean_line.startswith("the number") or clean_line.startswith("the text"):
            var_match = re.match(r'the\s+(number|text)\s+(\w+)\s+is\s+(.+?)\s+and\s+it\s+should\s+be\s+(\w+)', clean_line)
            if var_match:
                var_type_word = var_match.group(1)
                var_name = var_match.group(2)
                value_raw = var_match.group(3).strip()
                var_type = var_match.group(4).lower()
                if value_raw.startswith('"') and value_raw.endswith('"'):
                    value_raw = value_raw[1:-1]
                if var_type in ['int', 'integer', 'whole number', 'number']:
                    variables[var_name] = int(float(value_raw))
                elif var_type in ['flt', 'float', 'decimal number']:
                    variables[var_name] = float(value_raw)
                elif var_type in ['str', 'string', 'text']:
                    variables[var_name] = str(value_raw)
                elif var_type in ['dec', 'decimal']:
                    variables[var_name] = Decimal(value_raw)
                elif var_type in ['frc', 'fraction']:
                    variables[var_name] = Fraction(value_raw)
                else:
                    raise_error(f"a valid type (int, flt, str, dec, frc), but got: {var_type}", line, line_num, original_lines)

        # Math Operations (Natural Language)
        elif clean_line.startswith("the value of") and ("should be" in clean_line or "equals" in clean_line):
            if 'mathlib' not in allowed_libs:
                raise_error("the mathlib library to be enabled (use: this script uses: mathlib)", line, line_num, original_lines)
            math_match = re.match(r'the\s+value\s+of\s+(\w+)\s+(?:should\s+be|equals)\s+(.+)', clean_line)
            if math_match:
                output_var = math_match.group(1)
                expr = math_match.group(2).strip()
                
                # Try each operator in order of precedence
                if ' bitwise and ' in expr:
                    parts = expr.split(' bitwise and ', 1)
                    Mathlib.bitwise_and(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bitwise or ' in expr:
                    parts = expr.split(' bitwise or ', 1)
                    Mathlib.bitwise_or(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bitwise xor ' in expr:
                    parts = expr.split(' bitwise xor ', 1)
                    Mathlib.bitwise_xor(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bitwise nor ' in expr:
                    parts = expr.split(' bitwise nor ', 1)
                    Mathlib.bitwise_nor(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bitwise nand ' in expr:
                    parts = expr.split(' bitwise nand ', 1)
                    Mathlib.bitwise_nand(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bitwise xnor ' in expr:
                    parts = expr.split(' bitwise xnor ', 1)
                    Mathlib.bitwise_xnor(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' left shift ' in expr:
                    parts = expr.split(' left shift ', 1)
                    Mathlib.left_shift(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' right shift ' in expr:
                    parts = expr.split(' right shift ', 1)
                    Mathlib.right_shift(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bool and ' in expr:
                    parts = expr.split(' bool and ', 1)
                    Mathlib.bool_and(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bool or ' in expr:
                    parts = expr.split(' bool or ', 1)
                    Mathlib.bool_or(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bool xor ' in expr:
                    parts = expr.split(' bool xor ', 1)
                    Mathlib.bool_xor(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bool nor ' in expr:
                    parts = expr.split(' bool nor ', 1)
                    Mathlib.bool_nor(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bool nand ' in expr:
                    parts = expr.split(' bool nand ', 1)
                    Mathlib.bool_nand(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' bool xnor ' in expr:
                    parts = expr.split(' bool xnor ', 1)
                    Mathlib.bool_xnor(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' plus ' in expr:
                    parts = expr.split(' plus ', 1)
                    Mathlib.add(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' minus ' in expr:
                    parts = expr.split(' minus ', 1)
                    Mathlib.sub(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' times ' in expr:
                    parts = expr.split(' times ', 1)
                    Mathlib.mul(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' divided by ' in expr:
                    parts = expr.split(' divided by ', 1)
                    Mathlib.div(parts[0].strip(), parts[1].strip(), variables, output_var)
                elif ' modulo ' in expr:
                    parts = expr.split(' modulo ', 1)
                    Mathlib.mod(parts[0].strip(), parts[1].strip(), variables, output_var)
                else:
                    variables[output_var] = get_value(expr, variables)
            else:
                raise_error("a math statement like: the value of result should be x plus y", line, line_num, original_lines)

        # Display/Show
        elif clean_line.startswith("display") or clean_line.startswith("show"):
            if 'easyio' not in allowed_libs:
                raise_error("the easyio library to be enabled (use: this script uses: easyio)", line, line_num, original_lines)
            text_match = re.match(r'(?:display|show)\s+(?:the\s+text\s+)?"(.+?)"', clean_line)
            if text_match:
                text = text_match.group(1)
                Easyio.print_func(text, variables)
            else:
                raise_error('a display statement like: display the text "Hello"', line, line_num, original_lines)

        # Input
        elif clean_line.startswith("ask"):
            if 'easyio' not in allowed_libs:
                raise_error("the easyio library to be enabled (use: this script uses: easyio)", line, line_num, original_lines)
            input_match = re.match(r'ask\s+"(.+?)"\s+and\s+save\s+the\s+answer\s+in\s+(\w+)\s+as\s+(?:an?\s+)?(\w+)', clean_line)
            if input_match:
                prompt = input_match.group(1)
                var_name = input_match.group(2)
                var_type = input_match.group(3).lower()
                raw_input = Easyio.input_func(prompt, variables, "_temp_input")
                raw_input = variables.pop("_temp_input")
                try:
                    variables[var_name] = convert_to_type(raw_input, var_type)
                except:
                    raise_error(f"the input to be convertible to type {var_type}", line, line_num, original_lines)
            else:
                raise_error('an input statement like: ask "prompt" and save the answer in var as type', line, line_num, original_lines)

        # File Operations
        elif clean_line.startswith("read"):
            file_match = re.match(r'read\s+"([^"]+)"\s+from\s+"([^"]+)"\s+with\s+encoding\s+"([^"]+)"\s+saving\s+the\s+result\s+in\s+(\w+)', clean_line)
            if file_match:
                Fileio.read_file(file_match.group(1), file_match.group(2), file_match.group(3), variables, file_match.group(4))
            else:
                raise_error('a file read statement like: read "name" from "path" with encoding "enc" saving the result in var', line, line_num, original_lines)
        
        elif clean_line.startswith("write"):
            file_match = re.match(r'write\s+(.+?)\s+to\s+"([^"]+)"\s+in\s+"([^"]+)"\s+with\s+encoding\s+"([^"]+)"', clean_line)
            if file_match:
                content = get_value(file_match.group(1), variables)
                Fileio.write_file(content, file_match.group(2), file_match.group(3), file_match.group(4), variables)
            else:
                raise_error('a file write statement like: write [content] to "name" in "path" with encoding "enc"', line, line_num, original_lines)
        
        elif clean_line.startswith("delete"):
            file_match = re.match(r'delete\s+"([^"]+)"\s+from\s+"([^"]+)"', clean_line)
            if file_match:
                Fileio.delete_file(file_match.group(1), file_match.group(2), variables)
            else:
                raise_error('a file delete statement like: delete "name" from "path"', line, line_num, original_lines)

        # File System Navigation
        elif clean_line.startswith("list files"):
            list_match = re.match(r'list\s+files\s+in\s+"([^"]+)"\s+saving\s+in\s+(\w+)', clean_line)
            if list_match:
                Fileio.list_files(list_match.group(1), variables, list_match.group(2))
            else:
                raise_error('a statement like: list files in "path" saving in var', line, line_num, original_lines)
        
        elif clean_line.startswith("create directory"):
            dir_match = re.match(r'create\s+directory\s+"([^"]+)"', clean_line)
            if dir_match:
                Fileio.create_directory(dir_match.group(1), variables)
            else:
                raise_error('a statement like: create directory "path"', line, line_num, original_lines)
        
        elif clean_line.startswith("move file"):
            move_match = re.match(r'move\s+file\s+"([^"]+)"\s+in\s+path\s+"([^"]+)"\s+to\s+"([^"]+)"\s+in\s+path\s+"([^"]+)"', clean_line)
            if move_match:
                Fileio.move_file(move_match.group(1), move_match.group(2), move_match.group(3), move_match.group(4), variables)
            else:
                raise_error('a statement like: move file "src" in path "path" to "dst" in path "path"', line, line_num, original_lines)

        # Random (OS Secure Bytes)
        elif clean_line.startswith("generate") and "os random bytes" in clean_line:
            rand_match = re.match(r'generate\s+(\d+)\s+os\s+random\s+bytes\s+saving\s+the\s+result\s+in\s+(\w+)', clean_line)
            if rand_match:
                if 'osrand' not in allowed_libs:
                    raise_error("the osrand library to be enabled", line, line_num, original_lines)
                Osrandlib.generate_bytes(rand_match.group(1), variables, rand_match.group(2))
            else:
                raise_error('a statement like: generate [n] os random bytes saving the result in [var]', line, line_num, original_lines)

        # Random (Standard Bytes)
        elif clean_line.startswith("generate") and "random bytes" in clean_line:
            rand_match = re.match(r'generate\s+(\d+)\s+random\s+bytes\s+saving\s+the\s+result\s+in\s+(\w+)', clean_line)
            if rand_match:
                if 'random' not in allowed_libs:
                    raise_error("the random library to be enabled", line, line_num, original_lines)
                Randlib.generate_bytes(rand_match.group(1), variables, rand_match.group(2))
            else:
                raise_error('a statement like: generate [n] random bytes saving the result in [var]', line, line_num, original_lines)

        # Random (OS Secure Int)
        elif clean_line.startswith("generate an os random number"):
            rand_match = re.match(r'generate\s+an\s+os\s+random\s+number\s+from\s+(\d+)\s+to\s+(\d+)\s+saving\s+the\s+result\s+in\s+(\w+)', clean_line)
            if rand_match:
                if 'osrand' not in allowed_libs:
                    raise_error("the osrand library to be enabled", line, line_num, original_lines)
                Osrandlib.generate_int(rand_match.group(1), rand_match.group(2), variables, rand_match.group(3))
            else:
                raise_error('a statement like: generate an os random number from [min] to [max] saving the result in [var]', line, line_num, original_lines)

        # Random (Standard Int)
        elif clean_line.startswith("generate a random number"):
            rand_match = re.match(r'generate\s+a\s+random\s+number\s+from\s+(\d+)\s+to\s+(\d+)\s+saving\s+the\s+result\s+in\s+(\w+)', clean_line)
            if rand_match:
                Randlib.generate_int(rand_match.group(1), rand_match.group(2), variables, rand_match.group(3))
            else:
                raise_error('a statement like: generate a random number from [min] to [max] saving the result in [var]', line, line_num, original_lines)

        # Syslib Commands
        elif clean_line.startswith("sys"):
            if 'syslib' not in allowed_libs:
                raise_error("the syslib library to be enabled", line, line_num, original_lines)
            if clean_line.startswith("sys write"):
                text_match = re.match(r'sys\s+write\s+"(.+?)"', clean_line)
                if text_match:
                    Syslib.stdout_write(text_match.group(1), variables)
                else:
                    raise_error('a sys write statement like: sys write "text"', line, line_num, original_lines)
            elif clean_line.startswith("sys flush"):
                Syslib.stdout_flush()
            elif clean_line.startswith("sys read input"):
                input_match = re.match(r'sys\s+read\s+input\s+saving\s+in\s+(\w+)', clean_line)
                if input_match:
                    Syslib.stdin_read(True, variables, input_match.group(1))
                else:
                    raise_error('a sys read statement like: sys read input saving in [var]', line, line_num, original_lines)
            elif clean_line.startswith("sys read hidden input"):
                input_match = re.match(r'sys\s+read\s+hidden\s+input\s+saving\s+in\s+(\w+)', clean_line)
                if input_match:
                    Syslib.stdin_read(False, variables, input_match.group(1))
                else:
                    raise_error('a sys read statement like: sys read hidden input saving in [var]', line, line_num, original_lines)
            elif clean_line.startswith("sys get platform"):
                plat_match = re.match(r'sys\s+get\s+platform\s+saving\s+in\s+(\w+)', clean_line)
                if plat_match:
                    Syslib.get_platform(variables, plat_match.group(1))
                else:
                    raise_error('a sys platform statement like: sys get platform saving in [var]', line, line_num, original_lines)
            else:
                raise_error("a valid sys command (write, flush, read, get)", line, line_num, original_lines)

        # Wait
        elif clean_line.startswith("wait"):
            wait_match = re.match(r'wait\s+for\s+([\d.]+)\s+seconds', clean_line)
            if wait_match:
                Timelib.sleep(float(wait_match.group(1)))
            else:
                raise_error("a wait statement like: wait for N seconds", line, line_num, original_lines)

        # Clear Screen
        elif clean_line == "clear the screen":
            Syslib.clear()

        else:
            first_word = clean_line.split()[0] if clean_line.split() else ""
            suggestion = suggest_correction(first_word, [cmd.split()[0] for cmd in VALID_COMMANDS])
            raise_error(f"Unknown command or opcode", line, line_num, original_lines, suggestion)

        idx += 1

def parse_data(text):
    try:
        original_lines = text.splitlines()
        lines_with_nums = remove_comments(text)
        validate_syntax(lines_with_nums)
        first_pass_analysis(lines_with_nums, original_lines)
        variables = {}
        allowed_libs = set()
        functions = {}
        structures = {}
        execute_block(lines_with_nums, variables, allowed_libs, functions, structures, original_lines=original_lines)
        print("\n[PROGRAM FINISHED]")
    except ProgramExit:
        print("\n[PROGRAM ENDED]")
    except LoopBreak as e:
        try:
            raise_error(
                "'break' to be inside a 'do the following' or 'while' loop",
                e.line or "break",
                e.line_num,
                e.original_lines
            )
        except Exception as err:
            print(err)
    except FunctionReturn:
        print("\n[Runtime Error]: 'give back' used outside of a function")
    except Exception as e:
        print(f"{e}")

def repl_mode():
    """Interactive REPL shell for E# v3.2"""
    print("=" * 50)
    print("E# (English Sharp) v3.2 Interactive Shell")
    print("=" * 50)
    print("Commands: type 'help' for commands, 'exit' to quit\n")
    
    demo_script = """
this script uses: easyio
display the text "Hello,  world!"
display the text "███████╗ ██╗ ██╗ "
display the text "██╔════╝████████╗"
display the text "█████╗  ╚██╔═██╔╝"
display the text "██╔══╝  ████████╗"
display the text "███████╗╚██╔═██╔╝"
display the text "╚══════╝ ╚═╝ ╚═╝ "
display the text "Welcome to E# (English Sharp)!"
"""
    variables = {}
    allowed_libs = set()
    functions = {}
    structures = {}
    
    while True:
        try:
            user_input = input(">> ").strip()
            
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            
            if user_input.lower() == 'demo':
                parse_data(demo_script)
                continue

            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  Variables: the number/text X is ... and it should be TYPE")
                print("  Display: display \"text\" or show \"text\"")
                print("  Input: ask \"prompt\" and save the answer in X as TYPE")
                print("  Arithmetic: the value of X should be Y plus/minus/times/divided by Z")
                print("  Bitwise: the value of X should be Y bitwise and/or/xor/nor/nand/xnor Z")
                print("  Bit Shifts: the value of X should be Y left/right shift N")
                print("  Boolean: the value of X should be Y bool and/or/xor/nor/nand/xnor Z")
                print("  Lists: create list NAME as [1, 2, 3]")
                print("  Conditions: if X greater than Y then ... end if")
                print("  Loops: do the following N times ... end doing")
                print("  Functions: create a function called NAME that takes: ... with the code:")
                print("  Structures: create a structure named NAME with: ... end structure definition")
                print("  Help: explain [topic] to learn about topics")
                print("  Demo: demo")
                print("  Exit: exit\n")
                continue
            
            if not user_input:
                continue
            
            # Execute single line
            lines_with_nums = [(1, user_input)]
            execute_block(lines_with_nums, variables, allowed_libs, functions, structures, original_lines=[user_input])
            
        except KeyboardInterrupt:
            print("\n(interrupted)")
        except Exception as e:
            print(f"Error: {e}")

# ask "What is your name? " and save the answer in name as string
# display the text "Hi {name}!"

if __name__ == "__main__":
    import sys
    print("""
███████╗ ██╗ ██╗
██╔════╝████████╗
█████╗  ╚██╔═██╔╝
██╔══╝  ████████╗
███████╗╚██╔═██╔╝
╚══════╝ ╚═╝ ╚═╝ """)
    
    while True:
        print("\n--- E# v3.2 CLI Menu ---")
        print("1. Start Interactive REPL")
        print("2. Run .esh file")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            repl_mode()
        elif choice == '2':
            filename = input("Enter the .esh file path: ").strip()
            try:
                with open(filename, 'r') as f:
                    code = f.read()
                parse_data(code)
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found")
            except Exception as e:
                print(f"Error running file: {e}")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
