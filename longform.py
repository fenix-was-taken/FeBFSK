import febfsk
import time


def main():
    print("Second demonstration program to show longform text, like one might see if they were connecting to a server.")
    febfsk.modulate_start()
    time.sleep(3)
    febfsk.send(febfsk.translation(
        "S␑O ␑I␑'VE MADE A LOT OF FRIENDS BOTH ON AND OFF THE INTERNET WAVES, BUT IT'S SO MUCH EASIER TO HAVE A GET-␤"
        "TOGETHER FOR THE PEOPLE THAT ARE ONLY A MILE OR SO AWAY FROM YOU. ␑T␑HE ONES THAT ARE UPWARDS OF 800, THOUGH?␤"
        "␑Y␑EAH, THAT'S A LOT TOUGHER TO ORGANIZE. ␑I␑T'S ALWAYS NICE TO GET BACK FROM CLASSES AND WORK AND ALWAYS ␤"
        "HAVE SOMEONE TO BE ABLE TO TALK TO ONLINE, BUT SOME OF THESE PEOPLE ␑I␑'VE BEEN TALKING WITH FOR UPWARDS OF, ␤"
        "LIKE, 5 TO 6 YEARS AND WE STILL HAVEN'T GOTTEN TOGETHER... BUT NO LONGER. ␑W␑E FINALLY DECIDED TO MEET ␤"
        "AT A CONVENTION IN ␑D␑ECEMBER 2022, AND ␑I␑'D FINALLY KNOW THE *FACES AND REAL NAMES* OF THE PEOPLE ␑I␑'VE ␤"
        "CONSIDERED BEST FRIENDS FOR YEARS ALREADY. ␑I␑T'S FUNNY HOW INTERNET FRIENDS WORK LIKE THAT, HUH?␤"
        "␤"
        "␑A␑FTER ABOUT 8 HOURS OF DRIVING FROM ␑V␑ERMILLION TO ␑C␑HICAGO, STARTING AT 6␑AM␑ IN THE MORNING, ␑I␑ ␤"
        "FINALLY ARRIVED, AND ␑G␑OD, WAS ␑I␑ TIRED. ␑I␑ REMEMBER LOOKING AROUND FOR THE TWO PEOPLE THAT ␑I␑ WOULD BE ␤"
        "SHARING A ROOM WITH AT THE TIME, PACING AROUND, THINKING NERVOUSLY IN THE HOTEL ROOM LOBBY. ␑W␑OULD THEY ␤"
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
    ))
    time.sleep(95)
    febfsk.modulate_end()


if __name__ == "__main__":
    main()