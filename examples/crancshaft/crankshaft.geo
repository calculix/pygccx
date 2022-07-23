// Simple crankshaft
// Created 10.05.2015 by Matthias Sedlmaier
// Created for GMSH 2.9.3
Merge "crankshaft.stp";
Mesh.Algorithm = 2;
Mesh.ElementOrder = 2;
Mesh.SecondOrderIncomplete = 1;
Mesh.HighOrderOptimize = 1;
Mesh.CharacteristicLengthMin = 1;
Mesh.CharacteristicLengthMax = 7;
Mesh.MinimumCurvePoints = 2;
Mesh.MinimumCirclePoints = 3;

Physical Surface('FIX1') = {86};
Physical Surface('FIX2') = {30};
Physical Surface('LOAD') = {13,74};
Physical Volume('Crankshaft') = {1};

Field[1] = Attractor;
Field[1].FacesList = {28,31,82,83,87,95,97,104};
Field[2] = Threshold;
Field[2].IField = 1;
Field[2].LcMin = 1.5;
Field[2].LcMax = 7;
Field[2].DistMin = 1.5;
Field[2].DistMax = 7;
Background Field = 2;
Mesh.SaveGroupsOfNodes = 1;
Mesh 3;
