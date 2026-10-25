TARGET = worker
OBJECTS = main.o
CPPFLAGS = -Iinclude

$(TARGET): ${OBJECTS}
	gcc ${OBJECTS} -l sqlite3 -o $(TARGET)

main.o: src/main.c
	gcc ${CPPFLAGS} -c src/main.c -o main.o
