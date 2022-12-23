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