import commands

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
            'sin': (16, 1)  # синхронизировать окно и окно вначале программы
            }

def translateLine(line, output):
    words = line.split()
    newBytes = []
    newBytes.append(commands[words[0]][0])
    if commands[words[0]][1] == 0:
        newBytes += [0, 0, 0, 0]
    elif commands[words[0]][1] == 1:
        argument = int(words[1])
        newBytes += [argument // 16 ** 2, argument % 16 ** 2, 0, 0]
    else:
        a = int(words[1])
        b = int(words[2])
        newBytes += [a // 16 ** 2, a % 16 ** 2, b // 16 ** 2, b % 16 ** 2]
    print(newBytes)
    newFileByteArray = bytearray(newBytes)
    output.write(newFileByteArray)
    if(words[0] == 'ip'):
        for i in range(int(words[1]) - 1):
            output.write(bytearray([0, 0, 0, 0, 0]))

if __name__ == '__main__':
    file = open("fib.txt")
    lines = file.readlines()
    output = open("bin", "wb+")
    for line in lines:
        translateLine(line, output)
