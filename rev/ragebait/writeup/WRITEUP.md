# Template 

Solving this challenge has two basic steps: 
1. Find the correct function
2. Extract the flag (as input)

# 1. Finding the Correct Function
There are a variety of ways to find the correct function. The easiest would probably be searching for strlen in Ghidra, but any of the significant differences in functionality will do. Once we know the correct function, we can leverage the flag format (leaked through the "gaslight" functions) to make it so we only have two characters of our hash to brute force.

# 2. Extracting the flag
This can be done with a properly constrained angr search (intended based on challenge theme) or by reversing the logic manually using Z3.