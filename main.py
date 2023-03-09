from Graph import Graph_Simulator
from Utils import Utils
if __name__ == '__main__':
    s = Utils().graph_parser(r'C:\Users\yoyom\Desktop\gonen_graph.txt')
    print(s)
    Graph_Simulator(r'C:\Users\yoyom\Desktop\gonen_graph.txt').run()



