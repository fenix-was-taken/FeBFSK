import febfsk
import time


def main():
    print("Second demonstration program to show longform text, like one might see if they were connecting to a server.")
    febfsk.modulate_start()
    print("Pick a longform text.")
    print("[A]: Original English-only formatted text")
    print("[B]: Japanese test text")
    print("[C]: Binary")
    print("[D]: A test to switch between all of the above")
    print("[E]: A printout like a BBS")
    giveninput = input()
    if giveninput == 'A':
        febfsk.send(febfsk.translation(
            "S␑O ␑I␑'VE MADE A LOT OF FRIENDS BOTH ON AND OFF THE INTERNET WAVES, BUT IT'S SO MUCH EASIER TO HAVE A GET-␤"
            "TOGETHER FOR THE PEOPLE THAT ARE ONLY A MILE OR SO AWAY FROM YOU. ␑T␑HE ONES THAT ARE UPWARDS OF 800, THOUGH?␤"
            "␑Y␑EAH, THAT'S A LOT TOUGHER TO ORGANIZE. ␑I␑T'S ALWAYS NICE TO GET BACK FROM CLASSES AND WORK AND ALWAYS ␤"
            "HAVE SOMEONE TO BE ABLE TO TALK TO ONLINE, BUT SOME OF THESE PEOPLE ␑I␑'VE BEEN TALKING WITH FOR UPWARDS OF, ␤"
            "LIKE, 5 OR SO YEARS AND WE STILL HAVEN'T GOTTEN TOGETHER... BUT NO LONGER. ␑W␑E FINALLY DECIDED TO MEET ␤"
            "AT ONE OF THEIR HOMES IN ␑M␑ARCH 2023, AND ␑I␑'D FINALLY KNOW THE *FACES AND REAL NAMES* OF THE PEOPLE ␑I␑ ␤"
            "CONSIDERED BEST FRIENDS FOR YEARS ALREADY. ␑I␑T'S FUNNY HOW INTERNET FRIENDS WORK LIKE THAT, HUH?␤"
            "␤"
            "␑A␑FTER ABOUT 11 HOURS OF DRIVING FROM ␑V␑ERMILLION TO ␑D␑ENVER, STARTING AT 6␑AM␑ IN THE MORNING, ␑I␑ ␤"
            "FINALLY ARRIVED, AND ␑G␑OD, WAS ␑I␑ TIRED. ␑I␑ REMEMBER LOOKING AROUND FOR THE TWO PEOPLE THAT ␑I␑ WOULD BE ␤"
            "SHARING A ROOM WITH FOR A WEEK, PACING AROUND, THINKING NERVOUSLY OUTSIDE THE APARTMENT DOOR. ␑W␑OULD THEY ␤"
            "LIKE ME? ␑W␑HAT DO THEY LOOK LIKE? ␑W␑ILL THEY ACT ANY DIFFERENT THAN THEY DO ONLINE? ␑W␑AS THIS A BAD IDEA? ␤"
            "␑Y␑OU CAN'T REALLY KNOW A PERSON FROM JUST ONLINE INTERACTIONS, RIGHT?␤"
            "␤"
            "␑I␑T TURNS OUT DURING MY ANXIOUS PACING, ␑I␑ PASSED BY THEM MULTIPLE TIMES AND DIDN'T EVEN KNOW. ␑T␑HEY ␤"
            "WERE GIGGLING TO THEMSELVES THE ENTIRE TIME, WONDERING HOW TO APPROACH ME, WHILE ␑I␑ WALKED AROUND UNSURE ␤"
            "HOW TO APPROACH THEM, NOT KNOWING THEY WERE 10 FEET AWAY FROM ME. ␑O␑NCE ␑I␑ FINALLY REALIZED, THEY LAUGHED ␤"
            "AND BOTH IMMEDIATELY HUGGED ME AS TIGHT AS THEY COULD. ␤"
            "␤"
            "␑M␑AYBE NOT EVERY PERSON YOU MEET ONLINE IS TRYING TO KILL YOU, HUH?␤"
            "␤"
            "-␑FENIX␑"
            "␄"
        ))
    elif giveninput == 'B':
        febfsk.send(febfsk.translation_JP(
            "␒なああああああああああああああああああああ"
        ))
    elif giveninput == 'C':
        febfsk.send(febfsk.translation_binary(
            "␓␂01010101010101010101010101010101␃"
        ))
    elif giveninput == 'D':
        febfsk.send(febfsk.translation(
            "THIS IS A BASIC TEST OF DICTIONARY-SWITCHING BETWEEN LANGUAGES, FIRST SHOULD BE ENGLISH DISPLAYED HERE.␤"
            "NEXT SHOULD BE JAPANESE WHICH WILL BE DISPLAYED BELOW.␤"
        ))
        time.sleep(10)

        febfsk.send(febfsk.translation_JP(
            "␒みんなさん、こんいちは。␤"
        ))
        time.sleep(5)

        febfsk.send(febfsk.translation(
            "␑NEXT SHOULD BE BINARY, USED FOR SENDING FILES WITH NO CHARACTER ENCODING.␤"
        ))
        time.sleep(5)

        febfsk.send(febfsk.translation_binary(
            "␓␂01010101010101010101010101010101␃␤"
        ))
        time.sleep(5)

        febfsk.send(febfsk.translation(
            "␑THAT SHOULD BE IT.␤"
            "␄"
        ))
        time.sleep(3)
    elif giveninput == 'E':
        febfsk.send(febfsk.translation(
            "W␑elcome to:␤"
            "␤"
            " oooooooooooo           oooooooooo.  oooooooooo.   .oooooo..o ␤"
            "`888'     `8           `888'   `␑Y␑8b `888'   `␑Y␑8b d8␑P␑'    `␑Y␑8 ␤"
            " 888          .ooooo.   888     888  888     888 ␑Y␑88bo.      ␤"
            " 888oooo8    d88' `88b  888oooo888'  888oooo888'  `\"␑Y␑8888o.  ␤"
            " 888    \"    888ooo888  888    `88b  888    `88b      `\"␑Y␑88b ␤"
            " 888         888    .o  888    .88␑P␑  888    .88␑P␑ oo     .d8␑P␑ ␤"
            "o888o        `␑Y␑8bod8␑P␑' o888bood8␑P␑'  o888bood8␑P␑'  8""88888␑P␑' ␤"
            "␤"
            "␑V␑ermillion, ␑SD␑ - (605) ␑XXX-XXXX␑ | ␑S␑ys␑O␑p: ␑F␑e ␑N␑ix␤"
            "␑P␑rism (#00843)  |  using ␑BBBS␑/␑L␑i6 v4.10, ␑D␑ada-2␤"
            "␑T␑oday's date: ␑A␑pril 7, 2024 | ␑T␑ime: 12:26␑PM␑ ␑CST␑␤"
            "␑I␑t is currently 55 degrees, light rain showers.␤"
            "␑Y␑ou are the 99th caller.␤"
            "␑Y␑ou have 30 minutes of connect time.␤"
        ))
    else:
        print("Input was none listed.")
        exit(0)

    febfsk.modulate_end()


if __name__ == "__main__":
    main()
