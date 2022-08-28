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
intellysense and static type checking switched on. So you can see all the members, parameters types and doc strings.
In the folder doc/pygccx you can find an auto generated html documentation of all classes.


# Install Pygccx
- Install Python 3.10 or higher (or make a virtual env of Python 3.10)
- Download pygccx and extract to any location you want.
- install pygccx with pip
    ```
    pip install "path/to/pygccx"   (the folder where setup.py is located)
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
        - *BOUNDARY (inhomogeneous)
        - *CLOAD
        - *CONTACT FILE
        - *CONTACT OUTPUT
        - *CONTACT PRINT
        - *ELEMENT OUTPUT
        - *EL FILE
        - *EL PRINT
        - *NODE FILE
        - *NODE OUTPUT
        - *NODE PRINT
        - *STATIC
        - *STEP
        - *TIME POINTS
- Show CCX input file in CGX
- Solve CCX input file
- Show result file in CGX

# Planned capabilities of Pygccx:
- Support of all CCX keywords for static analysis
- Postpro in GMSH

# Prerequisites
- Python 3.10
- Packages from requirements.txt

# Version history:
0.1.0: <br>
- NEW FEATURES:
    - Added Keywords *NODE PRINT, *EL PRINT, *CONTACT PRINT
    - Added result reader for frd.<br>
        With model.get_frd_results() a result object is returned for querying results from frd file
    - Added result reader for dat.<br>
        With model.get_dat_results() a result object is returned for querying results from dat file
    - Added example "specimen_weibull" as a Jupyter notebook to show
          the use of model.get_dat_results()
- CHANGES:
    - Changed name of enum ENodeResults to ENodeFileResults
    - Changed name of enum EElementResult to EElFileResults
    - Changed name of enum EContactResults to EContactFileResults


0.0.1: First publish
