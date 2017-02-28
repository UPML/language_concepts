import commands

def translateLine(line, output):
    words = line.split()
    newBytes = []
    newBytes.append(commands[words[0]][0])
    if commands[words[0]][1] == 0:
        newBytes += [0, 0, 0, 0]
    elif commands[words[0]][1] == 1:
        argument = int(words[1])
        newBytes += [argument // 16**2, argument % 16**2, 0, 0]
    else:
        a = int(words[1])
        b = int(words[2])
        newBytes += [a // 16 ** 2, a % 16 ** 2, b // 16**2, b % 16**2]
    print(newBytes)
    newFileByteArray = bytearray(newBytes)
    output.write(newFileByteArray)

if __name__ == '__main__':
    file = open("fib.txt")
    lines = file.readlines()
    output = open("bin", "wb+")
    for line in lines:
        translateLine(line, output)
