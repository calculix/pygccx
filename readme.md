# What is Pygccx
Pygccx is a framework to build, solve and postprocess finite element models
made out of 3D solid elements using gmsh and CalculiX.<br><br>
After instanciating a pygccx model you can use the included Gmsh-Python-API
to build your geometry, mesh it and define physical groups (sets). For the usage of the Gmsh API look at http://gmsh.info//doc/texinfo/gmsh.html#Gmsh-API<br><br>
The gmsh mesh can then be converted to a pygccx mesh object, which
is more closely related to Calculix. All nodes and solid elements which are at least in one physical group will be convertet and all physical groups to node or element sets.<br><br>
Finally you have to define the keywords for the ccx input file.<br>
Each Keyword is represented by a class. Each class takes the parameters and data the keyword
needs.<br>
So your model basically consits of the mesh object and a list of keyword objects.<br><br>
When the model is build you can either export the CCX input file or solve the model directly
in pygccx.

Look in the examples folder for a quick start and to learn more about how to use pygccx.

ATM no postprocessing capabilities are impemented.<br>

# Planned capabilities of Pygccx:
- Static analysis of 3D structures (only solid elements, no shells or beams)
- Read and convert 3D mesh (only nodes, sets and solid elements) from GMSH to CCX
- Add additional abstract elements (SPRING, GAP, MASS) to model
- Support of all CCX keywords for static analysis
- Writing of CCX input file
- Solve CCX input file
- Read result files
- Provide result object for quering results
- Postpro in CGX
- Postpro in GMSH

# Design guidelines
Provide the users the most support of theis IDEs. This means:
- Use of type hints and protocols where ever possible
- No module, class, or class members without a docstring
- Use Enums for options, not strings
- Write docstrings for the Enums
- Each Enum class name starts with an "E" and is placed in the modul "enums"

Maintainability:
- Use depedancy injection and inversion of control
- Write code against protocols not implementations
- Each protocol class name starts with an "I" and is placed in the module "protocols"
- Classes are only instanciated in class "Model" or by the user to pass it to other classes
- Write for every class a unit test with 100% coverage.
- If possible, write an integation test (i.e. a ccx model which uses the new class / feature)
- Use dataclasses 
- Validate data in classes using \_\_setattr__ and raise exceptions accordingly.


# Prerequisites
- Python 3.10
- Packages from requirements.txt
