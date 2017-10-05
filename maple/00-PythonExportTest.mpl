
with(CodeGeneration);# 
;
f := proc (x) options operator, arrow; piecewise(0 < x and x < 1, 200, 1 < x and x < 2, 100) end proc;
Python(int(f(x), x = 0 .. .10), resultname = "w");
M := Matrix(5, 5);
ExportMatrix("test.txt", M);

