CC = gcc
CFLAGS = -O0 -s -fno-stack-protector -no-pie

TARGET = switcheroo
SRC = switcheroo.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

