# -*- coding:utf-8 -*-
import math
import time
def isPrimeNumber(num):
    if (num == 2):
        return True
    if (num < 2 or num % 2 == 0):
        return False
    i = 3
    while i <=math.sqrt(num):
        if (num % i == 0):
            return False
        i +=2
    return True

def get_prime_list(number):
    prime_list = []
    i = 2
    while i <= number:
        j =2
        while j <=number:
            if (j == i or (number-i-j == i) or (number-i-j == j)):
                j = j+1
                continue
            if(isPrimeNumber(i) and isPrimeNumber(j) and isPrimeNumber(number-i-j)):
                prime_str = "{},{},{}".format(i,j,number-i-j)
                prime_list.append(prime_str)
            j = j+1
        i = i+1
    return prime_list

def main():
    # number = 2000
    # prime_list = get_prime_list(number)
    # print prime_list
    num = 26285431
    while True:
        if isPrimeNumber(num):
            print(num)
            num = num +2
        num = num+2

if __name__ == "__main__":
    begin = time.time()
    main()
    end = time.time()
    durution = end - begin
    print durution
