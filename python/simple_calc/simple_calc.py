# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Simple Calculator
--------------------------------------------------------------------------
License:   
Copyright 2020 Nicolas Escobar

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple calculator that will 
  - Take in two numbers from the user
  - Take in an operator from the user
  - Perform the mathematical operation and provide the number to the user
  - Repeat

Operations:
  - addition
  - subtraction
  - multiplication
  - division
  - exponentiation
  - modulo
  - left/right binary shift

Error conditions:
  - Invalid operator --> Program should ask for new input
  - Invalid number   --> Program should ask for new input
  - Overflow error --> Program should ask for new input

--------------------------------------------------------------------------
"""
import operator

#Compatability with Python 2
try:
    input = raw_input
except NameError:
    pass

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
possOp = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "^": operator.pow,
    "%": operator.mod,
    ">>": operator.rshift,
    "<<": operator.lshift
}

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def calc(ans):
    #accept inputs
    num1 = input("First Number:   ")
    opStr = input("Operator:      ")
    num2 = input("Second Number:  ")
    print("------------------------------")
    
    #data validation
    op = possOp.get(opStr,)
    if op == None:
        print("Please choose a valid operator. Options are:")
        print("+, -, *, /, ^, %, >>, <<\n")
        return ans
    
    #there's probably a good way to repeat this with a list/loop but it's only 2 numbers    
    if num1 == "ans": #check for answer
        num1 = ans
    try:
        num1 = float(num1) #convert to float
    except:
        print("Please input a number or 'ans' for the previous answer.\n") #NaN error
        return ans
    if opStr in [">>", "<<"]: #shift operators need integers, truncation is fine
        num1 = int(num1)
        
    if num2 == "ans":
        num2 = ans
    try:
        num2 = float(num2)
    except:
        print("Please input a number or 'ans' for the previous answer.\n")
        return ans
    if opStr in [">>", "<<"]:
        num2 = int(num2)


    #computation
    try:
        ans = op(num1,num2)
        dispAns = str(ans)
        print("Answer:        " + dispAns + "\n")
    except OverflowError:
        print("Overflow Error. Max float value 1.798e+308.\n")
    return ans

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == "__main__":
    #initialize variables
    ans = 0
    
    #calculator loop
    while True:
        ans = calc(ans)
        
    
    
    
    