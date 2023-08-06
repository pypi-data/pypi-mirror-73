import math
from random import randint


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

number_of_digits = int(input("How many digit number would you like to guess? \n"))
computer_number= random_with_N_digits(number_of_digits)
guessed_number= 0
guess_count=0

while computer_number != guessed_number :
    #print(computer_number)
    
    computer_number_list = list(map(int, str(computer_number)))
    guessed_number= int(input("What would be your guess? \n"))
    guessed_number_list = list(map(int, str(guessed_number)))
    #common_number_list = list(set(computer_number_list).intersection(guessed_number_list))
    common_number_list=[]
    
    for i in computer_number_list:
        if i in guessed_number_list:
            common_number_list.append(i)
        
    
        
          
    common_number_list_total = len(common_number_list)
    
    same_place_number_list = []
    guess_count+=1
    
    for i in range(len(computer_number_list)):
        if (computer_number_list[i] == guessed_number_list[i]):
            same_place_number_list.append(i)
    
    
    same_digit_at_place_count = len(same_place_number_list)
            
            
            
        
         
    print(("{} out of {} numbers are are at its correct place \n ").format(same_digit_at_place_count,number_of_digits))
    print(("{} out of {} numbers are present in the number \n ").format(common_number_list_total,number_of_digits))
    
    if (computer_number != guessed_number):
        print("Give it an another tryy!!")
        
    
    
    else:
        print("You Won")
        print(("It took you {} counts to find the correct number").format(guess_count))
        
   
    
    
    
    
    
    
    
    



    
