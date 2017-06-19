"""
Program: Project 2 (Match Game)
Author: Kenny Truong
Course: CS 115
Description: A simple matching game. Users will click on cards one at a time, to flip them over to find pairs.
"""

from match_graphics import *
from random import seed
import random


def shuffle_cards():
    '''
    Generates a shuffled deck of cards. When done, cards[i][j] is the name of the card in
    row i and column j. It is a 5x5 grid comprised of 12 card pairs and one extra card.

    :param: None
    :return: cards
    '''

    seed()
    cards = []
    random.shuffle(images)

    count = 0
    for i in range(5):
        row = []
        for j in range(5):
            item = images[count]
            count += 1
            if count == 13:
                count = 0
            row.append(item)
        cards.append(row)
    random.shuffle(cards)

    return cards

def show_card(win, cards, i, j):
    '''
    Shows the card at row i and column j in the 5x5 grid in the window.

    :param win: the game window
    :param cards: the images
    :param i: row named i
    :param j: column named j
    :return: board
    '''

    board = []
    card = Image(Point(i * CARD_WIDTH + XMARGIN + CARD_WIDTH / 2, j * CARD_HEIGHT + YMARGIN + CARD_HEIGHT / 2),
                 cards[i][j])


    column = []
    column.append(cards)
    top_left_point = Point(i*CARD_WIDTH+XMARGIN, j*CARD_HEIGHT+YMARGIN)
    bottom_right_point = Point(i*CARD_WIDTH+CARD_WIDTH+XMARGIN, j*CARD_HEIGHT+CARD_HEIGHT+YMARGIN)
    enclosing_rectangle = Rectangle(top_left_point, bottom_right_point)
    enclosing_rectangle.setOutline("yellow")
    enclosing_rectangle.setWidth(5)
    enclosing_rectangle.draw(win)
    board.append(column)

    card.draw(win)

    return board

def hide_card(win, cards, i, j):
    '''

    Takes the window and cards and hides the card at row i and column j.

    :param win: the game window
    :param cards: the images
    :param i: row named i
    :param j: column named j
    :return: board
    '''


    board = []
    card = Image(Point(i * CARD_WIDTH + XMARGIN + CARD_WIDTH / 2, j * CARD_HEIGHT + YMARGIN + CARD_HEIGHT / 2),
                 cards[i][j])
    card.draw(win)

    column = []
    top_left_point = Point(i * CARD_WIDTH + XMARGIN, j * CARD_HEIGHT + YMARGIN)
    bottom_right_point = Point(i * CARD_WIDTH + CARD_WIDTH + XMARGIN, j * CARD_HEIGHT + CARD_HEIGHT + YMARGIN)
    enclosing_rectangle = Rectangle(top_left_point, bottom_right_point)
    enclosing_rectangle.setOutline("yellow")
    enclosing_rectangle.setFill("LightGreen")
    enclosing_rectangle.setWidth(5)
    enclosing_rectangle.draw(win)
    board.append(column)

    return board


def mark_card(win, cards, i, j):
    '''
    Takes the window and cards and marks the card at row i and column j with a red X.

    :param win: the game window
    :param cards: the images
    :param i: row named i
    :param j: column named j
    :return: cards
    '''


    top_left_point = Point(i * CARD_WIDTH + XMARGIN, j * CARD_HEIGHT + YMARGIN)
    bottom_right_point = Point(i * CARD_WIDTH + CARD_WIDTH + XMARGIN, j * CARD_HEIGHT + CARD_HEIGHT + YMARGIN)

    diagonal_lines = Line(top_left_point, bottom_right_point)
    diagonal_lines.draw(win)
    diagonal_lines.setOutline("red")
    diagonal_lines.setWidth(5)

    top_right_point = Point(i * CARD_WIDTH + XMARGIN + CARD_WIDTH, j * CARD_HEIGHT + YMARGIN)
    bottom_right_point = Point(i * CARD_WIDTH + XMARGIN, j * CARD_HEIGHT + CARD_HEIGHT + YMARGIN)

    diagonal_lines = Line(top_right_point, bottom_right_point)
    diagonal_lines.draw(win)
    diagonal_lines.setOutline("red")
    diagonal_lines.setWidth(5)

    return cards


def get_col(x):
    '''
    Takes the x-coordinate and returns the column.
    If the x coordinate is outside the board, returns -1.

    :param x: x-coordinate
    :return: columns
    '''

    columns = ((x-XMARGIN) // CARD_WIDTH)  # This code defines the size of a column.
    if columns < 0 or columns > 4:
        return -1
    else:
        return int(columns)  # Returns columns but in integer.




def get_row(y):
    '''
    Takes the y-coordinate and returns the row.
    If it it outside the board, returns -1.

    :param y: y-coordinate
    :return: row
    '''

    rows = ((y - YMARGIN) // CARD_HEIGHT)
    if rows < 0 or rows > 4:
        return -1
    return int(rows)


def main():
    '''
    Main will go through the process of each step and will call other functions when necessary.
    '''


    win = create_board()
    cards = shuffle_cards()

    for i in range(5):
        for j in range(5):
            hide_card(win, cards, i, j)

    fpick = 0
    frow = -1
    fcol = -1
    marked = []
    try:
        while True:
            click = win.getMouse()
            column = get_col(click.getX())
            row = get_row(click.getY())

            while (row == -1 or column == -1) or (frow == row and fcol == column) or ((column, row) in marked):
                click = win.getMouse()
                column = get_col(click.getX())
                row = get_row(click.getY())

            if (column, row) in marked:
                print("pass")

            elif fpick == 0:
                show_card(win, cards, column, row)
                frow = row
                fcol = column
                fpick += 1

            elif fpick == 1 and (column, row) not in marked:
                show_card(win, cards, column, row)
                fpick += 1
                game_delay(1)
                if cards[column][row] == cards[fcol][frow]:
                    mark_card(win, cards, column, row)
                    mark_card(win, cards, fcol, frow)
                    a = (column, row)
                    b = (fcol, frow)
                    marked.append(a)
                    marked.append(b)
                else:
                    hide_card(win, cards, column, row)
                    hide_card(win, cards, fcol, frow)
                fpick = 0

            if len(marked) == 24:
                you_won(win)


    except GraphicsError:  #  This line of code will make the program exit cleanly.
        win.close()


main()