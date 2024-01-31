def swap(matrix,x,y,m,n):
    temp = matrix[x][y]
    matrix[x][y] = matrix[m][n]
    matrix[m][n] = temp

f = open('D:/桌面/puzzle/puzzle4_test.txt', 'r')
store = []
for line in f:
    s = line.strip().split(' ')
    store.append(s[1:])
#matrix = [[11, 3, 1, 7],[4 ,6 ,8 ,2],[15 ,9 ,10, 13],[14, 12, 5, 0]]
#matrix = [[14 ,10 ,6 ,0],[4 ,9 ,1 ,8],[2 ,3 ,5 ,11],[12 ,13 ,7 ,15]]
#matrix = [[0 ,5 ,15 ,14],[7, 9, 6 ,13],[1 ,2 ,12 ,10],[8 ,11 ,4 ,3]]
matrix = [[6 ,10 ,3, 15],[14, 8, 7 ,11],[5 ,1 ,0 ,2],[13, 12, 9, 4]]
for s in store:
    x = (int(s[0])-1) // 4
    y = (int(s[0])-1) % 4
    m = (int(s[1])-1) // 4
    n = (int(s[1])-1) % 4
    swap(matrix,x,y,m,n)
print(matrix)