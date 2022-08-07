# What is Pygccx
Pygccx is a python framework to build, solve and postprocess finite element models
made out of 3D solid elements using Gmsh and CalculiX.<br><br>
After instantiating a pygccx model you can use the included Gmsh-Python-API
to build your geometry, mesh it and define physical groups (sets). For the usage of the Gmsh API look at http://gmsh.info//doc/texinfo/gmsh.html#Gmsh-API<br><br>
The gmsh mesh can then be converted to a pygccx mesh object, which
is more closely related to CalculiX. All nodes and solid elements which are at least in one physical group will be converted and all physical groups to node or element sets.<br><br>
Finally you have to define the keywords for the ccx input file.<br>
Each Keyword is represented by a class. Each class takes the parameters and data the keyword
needs.<br>
So your model basically consist of the mesh object and a list of keyword objects.<br><br>
When the model is build you can either export the CCX input file or solve the model directly
in pygccx.

Look in the examples folder for a quick start and to learn more about how to use pygccx.

ATM no postprocessing capabilities are implemented. This is one of next mile stones.<br>

# Install Pygccx
Up to now there is no pip package. To use pygccx do the following:
- Install Python 3.10 or higher
- Download the whole Project.
- Install requirements from requirements.txt with pip install -r requirements.txt
- Append the path to pygccx to sys.path
- Now import pygccx should work

# Capabilities of Pygccx:
- Static analysis of 3D structures (only solid elements, no shells or beams)
- Build geometry and mesh using Gmsh-Python API
- Read and convert 3D mesh (only nodes, sets and solid elements) from GMSH to CCX
- Add additional abstract elements (SPRING, GAP, MASS) to model
- Writing of CCX input file<br>
    - Implemented model keywords:
        - *AMPLIUTUDE
        - *BOUNDARY (homogenous)
        - *CLEARANCE
        - *CONTACT PAIR
        - *COUPLING
        - *DISTRIBUTING COUPLING
        - *EALSTIC
        - *FRICTION
        - *GAP
        - *MASS
        - *MATERIAL
        - *ORIENTATION
        - *PLASTIC
        - *RIGID BODY
        - *SOLID SECTION
        - *SPRING
        - *SURFACE BEHAVIOR
        - *SURFACE INTERACTION
        - *TRANSFORM <br>
    - Implemented step keywords:
        - *BOUNDARY (inhomogenous)
        - *CLOAD
        - *CONTACT FILE
        - *EL FILE
        - *NODE FILE
        - *STATIC
        - *STEP
        - *TIME POINTS
- Show CCX input file in CGX
- Solve CCX input file
- Show result file in CGX

# Planned capabilities of Pygccx:
- Support of all CCX keywords for static analysis
- Read result files
- Provide result object for querying results
- Postpro in GMSH

# Design guidelines
Provide the users the most support of their IDEs. This means:
- Use of type hints and protocols where ever possible
- No module, class, or class members without a docstring
- Use Enums for options, not strings
- Write docstrings for the Enums
- Each Enum class name starts with an "E" and is placed in the module "enums"

Maintainability:
- Use dependency injection and inversion of control
- Write code against protocols not implementations
- Each protocol class name starts with an "I" and is placed in the module "protocols"
- Classes are only instantiated in class "Model" or by the user to pass it to other classes
- Write for every class a unit test with 100% coverage.
- If possible, write an integration test (i.e. a ccx model which uses the new class / feature)
- Use data classes 
- Validate data in classes using \_\_setattr__ and raise exceptions accordingly.


# Prerequisites
- Python 3.10
- Packages from requirements.txt
