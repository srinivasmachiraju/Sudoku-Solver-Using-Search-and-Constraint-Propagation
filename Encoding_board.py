#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 00:15:10 2019

@author: srinivas
"""


from utils import display


rows = 'ABCDEFGHI'
cols = '123456789'



def cross(a, b):
      return [s+t for s in a for t in b]
  
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]

column_units = [cross(rows, c) for c in cols]

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

input_string='..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def grid_values(input_string,boxes):
    Mapping={}
    if(len(input_string)==81):
        for i in range(0,len(boxes)):
            Mapping[boxes[i]]=input_string[i]
        return Mapping

dictionary=grid_values(input_string,boxes)

display(dictionary)


def grid_values_update1(dictionary):
    for i in dictionary.keys():
        if dictionary[i]=='.':
            dictionary[i]='123456789'
    return dictionary

dictionary=grid_values_update1(dictionary)

display(dictionary)

def eliminate(values):
    for box in values.keys():
        if len(values[box])==1:
            for peer_box in peers[box]:
               values[peer_box] = values[peer_box].replace(values[box],'')
    return values

dictionary=eliminate(dictionary)

display(dictionary)

value=dictionary
#
#for i in range(0,5):
#    value=eliminate(value)
#
#display(value)

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

dictionary=only_choice(dictionary)

display(dictionary)



def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

dictionary=reduce_puzzle(dictionary)


display(dictionary)



def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

dictionary=search(dictionary)

display(dictionary)
