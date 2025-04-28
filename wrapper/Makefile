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

NAME = launcher
SRC = launcher.c

CC = gcc
CFLAGS = -Wall -Wextra -Werror

ifeq ($(OS),Windows_NT)
    EXT = .exe
else
    EXT =
endif

all: $(NAME)$(EXT)

$(NAME)$(EXT): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(NAME)$(EXT)

clean:
	rm -f $(NAME) $(NAME).exe

.PHONY: all clean