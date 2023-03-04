class Utils:
    def gen_letters(self):
        lst = ['A']
        while True:
            yield ''.join(lst)
            if all(list(map(lambda x: x == 'Z', lst))):
                for i in range(len(lst)):
                    lst[i] = 'A'
                lst.append('A')
            elif lst[-1] == 'Z':
                index = -1
                while lst[index] == 'Z':
                    lst[index] = 'A'
                    index += -1
                lst[index] = chr(ord(lst[index]) + 1)
            else:
                lst[-1] = chr(ord(lst[-1]) + 1)

    def graph_parser(self, file_name):
        file = open(file_name, 'r')
        if file:
            lst = file.read().splitlines()
            directed = True if lst[0] == "Directed" else "Undirected"
            edges = lst[1:]
            edges = [i.split() for i in edges]
            print(edges)
            weighted = True if len(edges[0]) == 3 else False
            nodes = set()
            for edge in edges:
                nodes.add(edge[0])
                nodes.add(edge[1])
            nodes = list(nodes)
            nodes.sort()
            print(nodes)
            graph = {i: [] for i in nodes}
            if directed:
                for edge in edges:
                    graph[edge[0]].append((edge[1], int(edge[2])))

                print(graph)

            else:
                for edge in edges:
                    graph[edge[0]].append((edge[1], int(edge[2])))
                    graph[edge[1]].append((edge[0], int(edge[2])))


            print(graph)