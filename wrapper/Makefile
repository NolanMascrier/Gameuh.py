# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nmascrie <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/14 14:03:30 by nmascrie          #+#    #+#              #
#    Updated: 2025/04/14 14:03:32 by nmascrie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

BIN = launcher
CFLAGS += -std=c99 -O2

SRC = launcher.c
OBJ = $(SRC:.c=.o)
CC = gcc

ifeq ($(OS),Windows_NT)
BIN := $(BIN).exe
LIBS = -lmingw32 -lSDL2main -lSDL2 -lopengl32 -lm -lGLU32
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Darwin)
		LIBS = -lSDL2 -framework OpenGL -lm
	else
		LIBS = -lSDL2 -lGL -lm -lGLU
	endif
endif

$(BIN):
	$(CC) $(SRC) $(CFLAGS) -o $(BIN)

clean:
	ifeq ($(OS),Windows_NT)
		del /f /q $(BIN) $(OBJ) 2>nul || exit 0
	else
		rm -f $(BIN) $(OBJ)
	endif

re: clean $(BIN)

.PHONY: $(BIN) clean re