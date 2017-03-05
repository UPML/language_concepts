import commands

# последний свободный элемент стека
stack_till = 0
# команды записаны в виде "name" ->[ номер, количество параметров]
commands = {'ip': (1, 1), # перейти на строку с номером x
            'inp' : (2, 1), # считать число с клавиатуры записать по адресу х
            'dec' : (3, 1), # из числа по адресу x - вычесть 1
            'push' : (4, 1), # положить на вершину стека значение по адресу а
            'pushaddr' : (5, 1), # положить на вершину стека адрес а
            'pop' : (6, 1), # снять с вершины стека значение, записать его в а
            'cmp' : (7, 2), # сравнить a и b по значению
            'cjump' : (8, 1), # если пред сравнение false то прыгнуть на х иначе ничего не делать
            'add' : (9, 2), # сложить значения а и b результат записать в а
            'move' : (10, 1), # перейти по адресу х
            'ret' : (11, 1), # снять с вершины стека значение и перейти в ячейку с таким адресом
            'copy' : (12, 2), # записать по адресу а значение из b
            'out' : (13, 1), # вывести значение по адресу х на экран
            'stop' : (14, 0), # завершить исполнение
            'res' : (15, 1), # зарезервировать на стеке место для х переменных
            'sin': (16, 1),  # синхронизировать окно и окно вначале программы
            'prin' : (17, 1) # вывести на дисплей фразу (Идеалогически фраза записывается в особый раздел,
                            # на данный момент на конец стека, далее аргумент - адрес начала записи,
                            # запись заканчивается нулем)
            }


def getBinary(a, block_size):
    ans = []
    for i in range(block_size):
        ans += [a % 16 ** 2]
        a //= 16 ** 2
    return bytearray(ans)


def changeMemoryLine(line_number, newValue):
    global memory
    memory = memory[:(line_number * 5)]  + newValue + memory[((line_number + 1) * 5):]


def processPrint(words, output):
    global stack_till
    global memory
    old_stack_till = stack_till
    for i in range(len(words)):
        for c in words[i]:
            changeMemoryLine(stack_till, getBinary(ord(c), 5))
            stack_till -= 1
        if i != len(words) - 1:
            changeMemoryLine(stack_till, getBinary(ord(' '), 5))
        else:
            changeMemoryLine(stack_till, getBinary(0, 5))
        stack_till -= 1
    return bytearray([old_stack_till // 16 ** 2, old_stack_till % 16 ** 2 ]) + bytearray([0, 0])


def translateLine(line, output):
    global memory
    words = line.split()
    newBytes = []
    newBytes.append(commands[words[0]][0])

    if commands[words[0]][1] == 0:
        newBytes += [0, 0, 0, 0]
    elif commands[words[0]][0] == 17:
        newBytes += processPrint(words[1:-1], output)
    elif commands[words[0]][1] == 1:
        argument = int(words[1])
        newBytes += [argument // 16 ** 2, argument % 16 ** 2, 0, 0]
    else:
        a = int(words[1])
        b = int(words[2])
        newBytes += [a // 16 ** 2, a % 16 ** 2, b // 16 ** 2, b % 16 ** 2]
    print(newBytes)
    memory += bytearray(newBytes)
    if(words[0] == 'ip'):
        global stack_till
        stack_till = int(words[1]) - 1
        for i in range(int(words[1]) - 1):
            memory += bytearray([0, 0, 0, 0, 0])

if __name__ == '__main__':
    file = open("fib.txt")
    lines = file.readlines()
    output = open("bin", "wb+")
    global memory
    memory = bytearray()
    for line in lines:
        translateLine(line, output)
    output.write(memory)