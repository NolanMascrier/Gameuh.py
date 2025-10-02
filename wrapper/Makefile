# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+: :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nmascrie <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/14 14:03:30 by nmascrie          #+#    #+#              #
#    Updated: 2025/10/02 by nmascrie                  ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

BIN = launcher
CFLAGS += -std=c99 -O2
SRC = launcher.c
OBJ = $(SRC:.c=.o)
CC = gcc

ifeq ($(OS),Windows_NT)
    BIN := $(BIN).exe
    GTK_CFLAGS := $(shell pkg-config --cflags gtk+-3.0)
    GTK_LIBS := $(shell pkg-config --libs gtk+-3.0)
else
    GTK_CFLAGS := $(shell pkg-config --cflags gtk+-3.0)
    GTK_LIBS := $(shell pkg-config --libs gtk+-3.0)
endif

all: $(BIN)

$(BIN): $(SRC) $(CC) $(CFLAGS) $(GTK_CFLAGS) $(SRC) -o $(BIN) $(GTK_LIBS)

clean:
ifeq ($(OS),Windows_NT)
    del /f /q $(BIN) $(OBJ) 2>nul || exit 0
else
	rm -f $(BIN) $(OBJ)
endif

re: clean all

.PHONY: all clean re