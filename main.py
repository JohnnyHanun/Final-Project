import Menu as menu
from Graph import Graph_Simulator
from StackVisualizer import StackVisualizer
from BinarySearchTree import BSTVisualizer
from Heap import HeapNode

if __name__ == '__main__':
    menu.main()
    from sys import getsizeof

    x = "a"
    print(getsizeof(x))
    # Graph_Simulator(r'C:\Users\yoyom\Desktop\gonen_graph2.txt').run()
    # Graph_Simulator(file_name=r'/Users/gonenselner/Desktop/gonen_graph 2.txt').run()
    #menu.main()
    # lst = []
    # lst.append(HeapNode((0,0),5))
    # lst.append(HeapNode((0, 0),2))
    # lst.append(HeapNode((0, 0), 3))
    # lst.append(HeapNode((0, 0), 54))
    # x = lst[0]
    # xx = [5]
    # print(type(x))
    # print( x in xx)


    #BSTVisualizer().run()




