import os
import shutil

path = ('id1', 'id2', 'id3', 'file')

print(path[len(path)-1])
file = (path[len(path)-1])

print(path[:len(path)-1])
ids = (path[:len(path)-1])
lol = '/'.join(ids) + f'/{file}'

print(lol)
os.makedirs('./id1/id2/id3/file.txt')
# shutil.move("./test.txt", "./testing/test.txt")
