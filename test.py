# import os
# import shutil
#
# path = ('id1', 'id2', 'id3', 'file')
#
# print(path[len(path)-1])
# file = (path[len(path)-1])
#
# print(path[:len(path)-1])
# ids = (path[:len(path)-1])
# lol = '/'.join(ids) + f'/{file}'
#
# print(lol)
# os.makedirs('./id1/id2/id3/file.txt')
# # shutil.move("./test.txt", "./testing/test.txt")
import abc


class Ab(metaclass=abc.ABC):

    def __init__(self):
        super(Ab, self).__init__()


    @abc.abstractmethod
    def afun(self):
        print(12)


new = Ab()
new.afun()
