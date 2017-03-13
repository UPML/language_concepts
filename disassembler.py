
# команды записаны в виде "name" ->[ номер, количество параметров]
from vm import block_size, name_by_id, getParams

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


def disassembler(memory):
    current_line = 0
    while current_line * block_size < len(memory):
        nextLine = memory[current_line * block_size: (current_line + 1) * block_size]
        func = name_by_id[nextLine[0]]
        params = getParams(nextLine)
        if nextLine[0] == 1:
            current_line += params[0]
            current_line -= 1
        str_to_write = func
        for i in range(commands[func][1]):
            str_to_write += " " + str(params[i])
        current_line += 1
        print(str_to_write)


if __name__ == '__main__':
    bin = open("bin", "rb")
    memory = bin.read()
    disassembler(memory)