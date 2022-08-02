# Planned capabilities of Pygccx:
- Static analysis of 3D structures (only solid elements, no shells or beams)
- Read and convert 3D mesh (only solid elements) from GMSH to CCX
- Add additional abstract elements (SPRING, GAP, MASS) to model
- Support of all CCX keywords for static analysis
- Writing of CCX input file
- Solve CCX input file
- Read result files
- Provide result object for quering results
- Postpro in CGX
- Postpro in GMSH

# Design guide lines
Provide the users the most support of theis IDEs. This means:
- Use of type hints and protocolls where ever possible
- No module, class, or class members without a docstring
- Use Enums for options, not strings
- Write docstrings for the Enums
- Each Enum class name starts with an "E" and is placed in the modul "enums"

Maintainability:
- Use depedancy injection and inversion of control
- write code against protocolls not implementations
- Each protocoll class name starts with an "I" and is placed in the module "protocolls"
- classes are only instanciated in class "Model" or by the user to pass it to other classes
- write for every class a unit test with 100% coverage.
- if possible, write an integation test (i.e. a ccx model which uses the new class / feature)
- Use dataclasses 
- Validate data in classes using \_\_setattr__ and raise exceptions accordingly.


# Prerequisites
- Python 3.10
- Packages from requirements.txt
