import commands


def process(line):



if __name__ == '__main__':
    bin = open("bin", "rb")
    while True:
        line = bin.read(5)
        if(bin):
            process(line)
        else:
            break