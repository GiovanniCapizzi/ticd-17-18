g++ -m64 -shared -Wl,-soname,KS -o KS.so -fPIC KS.cpp
g++ KS.cpp -o KS.exe