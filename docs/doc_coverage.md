# Documentation Coverage

PyPort includes tools for analyzing and ensuring documentation coverage. This document explains how to use these tools and interpret their results.

## Overview

The documentation coverage tools help you:

1. **Measure Documentation Coverage**: Calculate the percentage of documented code
2. **Identify Undocumented Code**: Find classes, methods, and functions that need documentation
3. **Enforce Documentation Standards**: Ensure that code meets documentation standards
4. **Generate Documentation Reports**: Create reports showing documentation coverage

## Using the Documentation Coverage Tools

### Local CICD Tool

The easiest way to run documentation coverage analysis is through the local CICD tool:

```bash
python utilz/local_cicd/cicd.py
```

Then select option 8 (Documentation Coverage Analysis) from the menu.

### Command Line

You can also run documentation coverage analysis directly from the command line:

```bash
python utilz/local_cicd/cicd.py 8
```

### Using Interrogate Directly

The documentation coverage tools use the `interrogate` package under the hood. You can also use `interrogate` directly:

```bash
interrogate -v src/pyport
```

### Programmatic Usage

You can use the documentation coverage tools programmatically:

```python
from utilz.local_cicd.svc.doc_coverage import analyze_doc_coverage

# Analyze documentation coverage for PyPort
report = analyze_doc_coverage(src_dir="src/pyport", min_coverage=80.0)

# Check if the coverage meets the minimum requirement
if report["success"]:
    print("Documentation coverage check passed!")
else:
    print("Documentation coverage check failed!")

# Print the coverage percentage
print(f"Documentation coverage: {report['coverage']:.1f}%")

# Print files with low coverage
for file in report["files"]:
    if file["file"].strip() and "%" in file["cover_pct"]:
        try:
            cover_pct = float(file["cover_pct"].replace("%", ""))
            if cover_pct < 80.0:
                print(f"{file['file']}: {file['cover_pct']}")
        except ValueError:
            pass
```

## Interpreting Results

The documentation coverage report includes:

### Overall Coverage

The percentage of documented code in the codebase.

### Files with Low Coverage

A list of files that have documentation coverage below the minimum requirement.

### Detailed Coverage Information

For each file, the report includes:
- Total number of objects (classes, methods, functions)
- Number of undocumented objects
- Number of documented objects
- Documentation coverage percentage

## CI/CD Integration

The documentation coverage tools are integrated with the CI/CD pipeline:

1. **GitHub Actions**: Documentation coverage checking is included in the GitHub Actions workflow
2. **Pre-release Checks**: Documentation coverage is checked before releasing a new version
3. **Local Development**: Documentation coverage analysis is available through the local CICD tool

## Documentation Standards

To ensure high documentation coverage, follow these standards:

1. **Module Docstrings**: Every module should have a docstring explaining its purpose
2. **Class Docstrings**: Every class should have a docstring explaining its purpose and behavior
3. **Method Docstrings**: Every method should have a docstring explaining its purpose, parameters, and return value
4. **Function Docstrings**: Every function should have a docstring explaining its purpose, parameters, and return value

Example of a well-documented function:

```python
def calculate_total(items: List[Dict[str, Any]], tax_rate: float = 0.0) -> float:
    """
    Calculate the total cost of items including tax.
    
    Args:
        items: A list of items, where each item is a dictionary with a 'price' key.
        tax_rate: The tax rate as a decimal (e.g., 0.1 for 10% tax).
        
    Returns:
        The total cost including tax.
        
    Raises:
        ValueError: If any item does not have a 'price' key or if the tax rate is negative.
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = 0.0
    for item in items:
        if 'price' not in item:
            raise ValueError("Each item must have a 'price' key")
        subtotal += item['price']
    
    return subtotal * (1 + tax_rate)
```

## Best Practices

1. **Write Documentation First**: Write docstrings before implementing code
2. **Keep Documentation Updated**: Update docstrings when code changes
3. **Be Concise but Complete**: Docstrings should be concise but include all necessary information
4. **Use Type Hints**: Combine docstrings with type hints for better documentation
5. **Run Coverage Checks Regularly**: Check documentation coverage regularly to catch issues early
