# -*- coding: utf-8 -*-

def BinarySearch(array, t):
    low = 0
    high = len(array)-1
    # t = int(t)
    while low <= high:
        mid = (low+high)//2

        if array[mid] < t:
            low = mid+1

        elif array[mid] > t:
            high = mid-1

        else:
            return array[mid],mid

    return -1

if __name__ == '__main__':
    li = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(li[0])
    a = []
    print(BinarySearch(li,3))

    print(int(4.7))