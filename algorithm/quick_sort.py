# -*- coding: utf-8 -*-
import random
import time

def quick_sort(array, left, right):
    if left >= right:
        return
    low = left
    high = right
    key = array[low]
    # print low, high, key
    while left < right:
        while left < right and array[right] > key:
            right -= 1
        # print right
        array[left] = array[right]
        while left < right and array[left] <= key:
            left += 1
        array[right] = array[left]
        # print low, high, key
    # print low, high, key
    array[right] = key
    quick_sort(array, low, left - 1)
    quick_sort(array, left + 1, high)
    return array

def quick_sort2(array):
    if len(array) <= 1:
        return array
    less = []
    greater = []

    base = array.pop()

    for i in array:
        if i < base:
            less.append(i)
        else:
            greater.append(i)

    return quick_sort2(less) + [base] + quick_sort2(greater)

if __name__ == '__main__':
    li = [4,8,1,3,2,5,7,6]

    quick_sort(li, 0, 7)

    print li

    # li = random.sample(range(200000000),1000000)
    # begin1 = time.time()
    # re = quick_sort2(li)
    # end1 = time.time()
    # dur1 = end1-begin1
    # print dur1
    #
    # begin2 = time.time()
    # ge = quick_sort(li,0,len(li)-1)
    # end2 = time.time()
    # dur2 = end2-begin2
    # print dur2