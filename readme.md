# What is Pygccx
Pygccx is a python framework to build, solve and postprocess finite element models
made out of 3D solid elements using Gmsh and CalculiX.<br><br>
After instantiating a pygccx model you can use the included Gmsh-Python-API
to build your geometry, mesh it and define physical groups (sets). For the usage of the Gmsh API look at http://gmsh.info//doc/texinfo/gmsh.html#Gmsh-API<br><br>
The gmsh mesh can then be converted to a pygccx mesh object, which
is more closely related to CalculiX. All nodes and solid elements which are at least in one physical group will be converted and all physical groups to node- or element sets.<br><br>
Finally you have to define the keywords for the ccx input file.<br>
Each Keyword is represented by a class. Each class takes the parameters and data the keyword
needs.<br>
So your model basically consist of the mesh object and a list of keyword objects.<br><br>
When the model is complete you can either export the CCX input file or solve the model directly
in pygccx.

Look in the examples folder for a quick start and to learn more about how to use pygccx.
The best way to explore pygccx is by using an IDE like VS Code or PyCharm with auto completion,
intellysense and static type checking switched on. So you can see all the members, parameters, types and doc strings.
In the folder docs/pygccx you can find an auto generated html documentation of all classes.


# Install Pygccx
- Install Python 3.10 or higher (or make a virtual env of Python 3.10)
- install pygccx with pip
    ```
    pip install https://github.com/calculix/pygccx/releases/download/v0.2.2/pygccx-0.2.2-py3-none-any.whl
    ```

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
        - *CREEP
        - *DEFORMATION PLASTICITY
        - *DENSITY
        - *DISTRIBUTING COUPLING
        - *DLOAD
        - *EALSTIC
        - *EQUATION
        - *FRICTION
        - *GAP
        - *HEADING
        - *HYPERELASTIC
        - *INCLUDE (also for step keywords)
        - *MASS
        - *MATERIAL
        - *MPC
        - *NO ANALYSIS
        - *ORIENTATION
        - *PLASTIC
        - *PRE-TENSION SECTION
        - *RIGID BODY
        - *SOLID SECTION
        - *SPRING
        - *SURFACE BEHAVIOR
        - *SURFACE INTERACTION
        - *TIE
        - *TRANSFORM <br>
    - Implemented step keywords:
        - *BOUNDARY (inhomogeneous)
        - *CLOAD
        - *CONTACT FILE
        - *CONTACT OUTPUT
        - *CONTACT PRINT
        - *ELEMENT OUTPUT
        - *EL FILE
        - *EL PRINT
        - *GREEN
        - *NODE FILE
        - *NODE OUTPUT
        - *NODE PRINT
        - *STATIC
        - *STEP
        - *TIME POINTS
        - *VISCO
    - [Unsupported keywords](https://github.com/calculix/pygccx/blob/master/unsupported_keywords.md)
- Show CCX input file in CGX
- Solve CCX input file
- Show result file in CGX
- Create result object from *.frd or *.dat files for postprocessing
- Tools for calculate invariant stresses (Mises, Principals, etc.)
- Tools for transformation of coordinates, vectors or tensors between
  coordinate systems
- Tool for generating preloaded bolts consisting of solid elements and
  tools for postprocessing of section forces and moments

# Planned capabilities of Pygccx:
- Support of all CCX keywords for static analysis<br>
[Unsupported keywords](https://github.com/calculix/pygccx/blob/master/unsupported_keywords.md)
- Postpro in GMSH
- Read mesh from *.frd file

# Prerequisites
- Python 3.10
