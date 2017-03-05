block_size = 5
current_line = 0
stack_head = 1
cmp_flag = False
stack_window = []
frame_pointer = 0

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
name_by_id = ['', 'ip',  # перейти на строку с номером x
              'inp',  # считать число с клавиатуры записать по адресу х
              'dec',  # из числа по адресу x - вычесть 1
              'push',  # положить на вершину стека значение по адресу а
              'pushaddr',  # положить на вершину стека адрес а
              'pop',  # снять с вершины стека значение, записать его в а
              'cmp',  # сравнить a и b по значению
              'cjump',  # если пред сравнение false то прыгнуть на х иначе ничего не делать
              'add',  # сложить значения а и b результат записать в а
              'move',  # перейти по адресу х
              'ret',  # снять с вершины стека значение и перейти в ячейку с таким адресом
              'copy',  # записать по адресу а значение из b
              'out',  # вывести значение по адресу х на экран
              'stop',
              'res',
              'sin',
              'prin'
              ]


def getParams(line):
    return [line[1] * 16 ** 2 + line[2], line[3] * 16 ** 2 + line[4]]


def getBinary(a):
    ans = []
    for i in range(block_size):
        ans += [a % 16 ** 2]
        a //= 16 ** 2
    return bytearray(ans)


def getValue(line):
    ans = 0
    mult = 1
    for i in range(block_size):
        ans += mult * line[i]
        mult *= 16 ** 2
    return ans


def incLineNumber():
    global current_line
    current_line += 1


def changeMemoryLine(line_number, newValue):
    global memory
    memory = memory[:line_number * 5]  + newValue + memory[(line_number + 1) * 5:]



def ip(memory, line):
    global current_line
    current_line = getParams(line)[0]


def inp(memory, line):
    a = int(input())
    line_number = getParams(line)[0]
    changeMemoryLine(line_number, getBinary(a))
    incLineNumber()


def dec(memory, line):
    line_number = getParams(line)[0]
    value = memory[line_number * 5:(line_number + 1) * 5]
    changeMemoryLine(line_number, getBinary(getValue(value) - 1))
    print(str(getValue(value)) + " -> " + str(getValue(value) - 1))
    incLineNumber()


def push(memory_, line):
    global stack_head
    global memory
    line_number = getParams(line)[0]
    changeMemoryLine(stack_head, getBinary(getValue(memory[line_number * 5: (line_number + 1) * 5])))
    print(str(getValue(memory[stack_head * 5: (stack_head + 1) * 5 ] ) ))
    print("stack_head", str(stack_head))
    stack_head += 1
    incLineNumber()


def pushaddr(memory_, line):
    global stack_head
    global memory
    changeMemoryLine(stack_head, getBinary(getParams(line)[0]))
    print(str(getValue(memory[stack_head * 5: (stack_head + 1) * 5] ) ))
    print("stack_head", str(stack_head))
    stack_head += 1
    incLineNumber()


def pop(memory, line):
    line_number = getParams(line)[0]
    global stack_head
    global stack_window
    stack_head -= (1 + len(stack_window))
    changeMemoryLine(line_number, memory[stack_head * 5: (stack_head + 1) * 5])
    print(getValue(memory[stack_head * 5: (stack_head + 1) * 5]))
    print("stack_head", str(stack_head))
    stack_head += 1 + len(stack_window)
    incLineNumber()


def cmp(memory, line):
    params = getParams(line)
    global cmp_flag
    a = getValue(memory[params[0] * 5: (params[0] + 1) * 5])
    b = getValue(memory[params[1] * 5: (params[1] + 1) * 5])
    cmp_flag = a == b
    print("a = " + str(a) + " b = " + str(b))
    incLineNumber()


def cjump(memory, line):
    global cmp_flag
    if cmp_flag == False:
        for i in range(getParams(line)[0]):
            incLineNumber()
    incLineNumber()


def add(memory, line):
    params = getParams(line)
    a = getValue(memory[params[0] * 5: (params[0] + 1) * 5])
    b = getValue(memory[params[1] * 5: (params[1] + 1) * 5])
    changeMemoryLine(params[0], getBinary(a + b))
    incLineNumber()


def move(memory, line):
    global current_line
    current_line = getParams(line)[0]


def ret(memory, line):
    global frame_pointer
    global stack_window
    frame_pointer = stack_window[0]
    print("FP " + str(frame_pointer))
    start_index = getParams(line)[0]
    for i in range(len(stack_window)):
        stack_window[i] = getValue(memory[(frame_pointer + i) * 5: (frame_pointer + i + 1) * 5])
        if i != 0:
            changeMemoryLine(start_index + i - 1, memory[(frame_pointer + i) * 5: (frame_pointer + i + 1) * 5])
        print("index " + str( frame_pointer + i ) + " value " + str(getValue(memory[(frame_pointer + i) * 5: (frame_pointer + i + 1) * 5])))

    global stack_head
    global current_line
    stack_head -= len(stack_window)
    stack_head -= 2
    current_line = getValue(memory[stack_head * 5 : (stack_head + 1) * 5])


def copy(memory, line):
    params = getParams(line)
    print("from " + str(params[1]) + " to " + str(params[0]))
    changeMemoryLine(params[0], memory[params[1] * 5: (params[1] + 1) * 5])
    incLineNumber()


def out(memory, line):
    line_number = getParams(line)[0]
    print(getValue(memory[line_number * 5: (line_number + 1) * 5]))
    incLineNumber()


def stop(memory, line):
    exit()


def res(memory, line):
    global stack_window
    new_stack_window = [0]*(getParams(line)[0] + 1)
    global stack_head
    global frame_pointer
    changeMemoryLine(stack_head, getBinary(frame_pointer))
    new_stack_window[0] = frame_pointer
    frame_pointer = stack_head
    stack_head += len(new_stack_window)
    stack_window = new_stack_window
    incLineNumber()


def sin(memory, line):
    global frame_pointer
    global stack_window
    start_index = getParams(line)[0]
    for i in range(1, len(stack_window)):
        changeMemoryLine(frame_pointer + i, memory[(start_index + i - 1) * 5: (start_index + i + 1 - 1) * 5])
        print("index " + str(frame_pointer + i) + " value " + str(getValue(memory[(start_index + i - 1) * 5: (start_index + i + 1 - 1) * 5])))
    incLineNumber()


def prin(memory, line):
    word = ""
    line_number = getParams(line)[0]
    while getValue(memory[line_number * 5: (line_number + 1) * 5]) != 0:
        word += chr(getValue(memory[line_number * 5: (line_number + 1) * 5]))
        line_number -= 1
    print(word)
    incLineNumber()


def process():
    global current_line
    global memory
    global stack_window
    stack_window = [0]
    current_line = 0
    while (True):
        nextLine = memory[current_line * block_size: (current_line + 1) * block_size]
        func = name_by_id[nextLine[0]]
        str_to_write = func + " " + str(current_line)
        print(str_to_write)
        globals()[func](memory, nextLine)

if __name__ == '__main__':
    bin = open("bin", "rb")
    global memory
    memory = bin.read()
    process()
