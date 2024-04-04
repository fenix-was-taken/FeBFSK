import febfsk


def main():
    print("Basic FeBFSK driver program.")
    inp = input("[S]ending or [R]eceiving? ")
    if inp == "S":
        febfsk.modulate_start()
        flag = False
        while not flag:
            innput = input()
            if innput == '':
                break
            else:
                febfsk.send(febfsk.translation(innput))
        febfsk.modulate_end()
    elif inp == "R":
        febfsk.demodulate_start()
    else:
        print("Input wasn't a S or R.")
        exit()


if __name__ == "__main__":
    main()
