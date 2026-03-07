# English-Sharp
It is a simple esoteric programming language interpreted in Python, it has English style syntax.

# E# (English Sharp)

## Overview

E# (English Sharp) is a natural language-based programming language interpreter written in Python. It allows users to write code using English-like syntax, making programming accessible without traditional syntax barriers. This interpreter supports variables, control flow, functions, structures, file operations, and various libraries.

Version: 3.2
Author: hotdogdevourer (Alias: Iris500)
License: MIT
Filename: parser1.py

## Requirements

- Python 3.x
- Standard libraries (os, time, sys, re, random, math, difflib, getpass, readline, decimal, fractions, typing, datetime, collections, statistics)

## Installation and Usage

### Running a Script

To execute an E# script file, pass the filename as an argument to the parser.

```bash
python parser1.py script.esh
```

### Interactive REPL Mode

To start the interactive shell, run the parser without arguments.

```bash
python parser1.py
```

In REPL mode, you can type commands directly. Use `help` to see available commands, `demo` to run a demonstration script, and `exit` to quit.

## Language Syntax and Features

### Comments and Configuration

Comments are enclosed in double colons. Configuration lines enable specific libraries.

```text
:: This is a comment ::
this script uses: mathlib, random, syslib
```

### Variables and Data Types

Variables are declared with a specific type. Supported types include integer, float, string, decimal, fraction, and bytes.

```text
the number count is 5 and it should be integer
the text greeting is "Hello World" and it should be string
the number pi is 3.14 and it should be float
the value of result should be 10 divided by 2
```

Filler words such as "please", "lol", "um", "uh", "like", "actually", "basically", "just", "really", "very", "an", "a" are automatically ignored by the parser.

### Operators

#### Arithmetic
- plus (+)
- minus (-)
- times (*)
- divided by (/)
- modulo (%)

#### Bitwise
- bitwise and (&)
- bitwise or (|)
- bitwise xor (^)
- bitwise nor
- bitwise nand
- bitwise xnor
- left shift (<<)
- right shift (>>)

#### Boolean
- bool and
- bool or
- bool xor
- bool nor
- bool nand
- bool xnor
- bool not

#### Comparison
- equal to (==)
- not equal to (!=)
- greater than (>)
- less than (<)
- greater than or equal to (>=)
- less than or equal to (<=)

Synonyms are supported (e.g., "is" equals "equal to", "more than" equals "greater than").

### Control Flow

#### Conditional Statements

```text
if x greater than 5 then
    display the text "Greater"
otherwise if x equal to 5 then
    display the text "Equal"
otherwise
    display the text "Less"
end if
```

#### Loops

Fixed Count Loop:
```text
do the following 5 times
    display the text "Hello"
end doing
```

While Loop:
```text
while x less than 10 do
    the value of x should be x plus 1
end while
```

Break Statement:
```text
break
```

### Functions

Functions are defined with arguments and types, and can return values using "give back".

```text
create a function called add that takes:
    number a
    number b
with the code:
    give back a plus b
end function definition

run the function add with 5, 10 saving the result in sum
```

### Structures

Custom data structures can be defined with fields and types.

```text
create a structure named Person with:
    string name
    integer age
end structure definition
```

### Collections (Lists/Arrays)

```text
create list numbers as [1, 2, 3, 4, 5]
create list names as ["Alice", "Bob", "Charlie"]
```

### Input and Output

#### Standard I/O
```text
display the text "Welcome to E#"
show the text "Hello"
ask "What is your name?" and save the answer in name as string
```

#### System I/O (Requires syslib)
```text
sys write "Direct output"
sys read input saving in user_input
sys read hidden input saving in password
sys get platform saving in platform_info
```

### File Operations

File operations require appropriate security policies to be enabled.

```text
read "file.txt" from "path/to/dir" with encoding "utf-8" saving the result in content
write content to "output.txt" in "path/to/dir" with encoding "utf-8"
delete "old_file.txt" from "path/to/dir"
list files in "path/to/dir" saving in file_list
create directory "new_folder"
move file "src.txt" in path "src_path" to "dst.txt" in path "dst_path"
```

### Libraries

Libraries must be enabled at the start of the script using `this script uses`.

- **mathlib**: Mathematical functions (sqrt, pow, sin, cos, tan, abs, floor, ceil, round, min, max, mean, median, variance).
- **random**: Random number generation (generate a random number from X to Y, shuffle_list).
- **osrand**: Secure OS random number generation (generate an os random number, os random bytes).
- **easyio**: Easy input/output operations (display, show, ask).
- **syslib**: System-level operations (write, read, platform info).
- **strproclib**: String processing (substring, split, join, replace, uppercase, lowercase, trim, regex_match, length).

Example usage:
```text
this script uses random
generate a random number from 1 to 100 saving the result in rand_num
```

### Error Handling

Try-catch blocks handle runtime errors.

```text
try
    the value of x should be 10 divided by 0
catch error as e
    display the text "Error occurred"
end try
```

### System Commands

```text
wait for 2 seconds
clear the screen
end program
```

### Debugging and Help

#### Help System
The `explain` command provides documentation for topics.
```text
explain topics
explain variables
explain if
```

#### Debugger
The `debug` command controls execution flow.
```text
debug start
debug step
debug show
debug break at line 10
```

## Security Constraints

The interpreter includes a security policy class that can restrict certain operations:
- File write permissions
- OS random number generation
- Memory limits
- Execution time limits

By default, file writing and OS random are enabled but can be disabled in the source code security policy settings.

## Error Reporting

The interpreter provides enhanced error reporting including:
- Line numbers
- Context of the error
- Expected syntax
- Suggestions for corrections based on similar valid commands

## License

MIT License. See the LICENSE file in the project root for details.

## Author

hotdogdevourer (Alias: Iris500)
