DST = dlx.exe
MODULE = dlx.o

$(DST): $(MODULE) dlxcore.o
	g++ dlxcore.o $(MODULE) -o $(DST)

dlxcore.o: dlxcore.cpp
	g++ -c dlxcore.cpp -o dlxcore.o

dlx.o: dlx.cpp
	g++ -c dlx.cpp -o dlx.o