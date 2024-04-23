// Gmsh project created on Sun Apr 07 23:05:12 2024
SetFactory("OpenCASCADE");
Merge "model.step";
Physical Volume("NUT_M20", 605) = {1};
Physical Volume("FLANGE_1", 606) = {2};
Physical Volume("FLANGE_2", 607) = {3};
Physical Surface("FLANGE_1_FIX", 608) = {31};
Physical Surface("FLANGE_1_NUT", 609) = {23};
Physical Surface("FLANGE_2_BOLT", 610) = {42};
Physical Surface("FLANGE_2_LOAD", 611) = {38};
Physical Surface("FLANGE_1_CONT", 612) = {26};
Physical Surface("FLANGE_2_CONT", 613) = {43};
Physical Surface("NUT_FLANGE_1", 614) = {18};
Physical Surface("NUT_THREAD", 615) = {1,4};
Physical Surface("ROT_SYM", 616) = {21, 22, 33, 34};

//Face sizing nut thread. If too coarse, issues in tie contact to bolt threads may occure
Field[1] = Constant;
Field[1].VIn = 7;
Field[1].SurfacesList = {1, 4};

//Face sizing clamping interface (main contact)
Field[2] = Constant;
Field[2].VIn = 5;
Field[2].SurfacesList = {26, 43};

//Face fillet radius
Field[3] = Constant;
Field[3].VIn = 4;
Field[3].SurfacesList = {24, 35};

Field[4] = Min;
Field[4].FieldsList = {1, 2, 3};
Background Field = 4;

Transfinite Surface {1,4} = {};

Mesh.ElementOrder = 2;
Mesh.HighOrderOptimize = 2;
Mesh.OptimizeNetgen = 1;
Mesh.MeshSizeMax = 8;
Mesh 3;

