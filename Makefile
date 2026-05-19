FC = gfortran
FFLAGS = -O2

SRC_DIR = ./src
BIN_DIR = ./bin

TARGET = $(BIN_DIR)/surfdisp

SRC = $(SRC_DIR)/surfdisp_main.f \
      $(SRC_DIR)/surfdisp96.f

all: $(TARGET)

$(TARGET): $(SRC)
	$(FC) $(FFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)
