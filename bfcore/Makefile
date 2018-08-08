DST = test.exe
MODULE = bfcore.o

$(DST): $(MODULE) test.o
	g++ test.o $(MODULE) -o $(DST)

bfcore.o: bfcore.cpp
	g++ -c bfcore.cpp -o bfcore.o

test.o: test.cpp
	g++ -c test.cpp -o test.o