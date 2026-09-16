#!/usr/bin/env python3
"""
Static site generator for the Scottsdale Martial Arts Center (SMAC) website.

No framework, no build step for visitors — this script just stamps shared
header/nav/footer markup onto page content and writes plain .html files to
the repo root. Edit the content below and rerun `python3 build/build.py`
from the repo root to regenerate the site.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_NAME = "Scottsdale Martial Arts Center"
SITE_SHORT = "SMAC"
PHONE = "(602) 676-1684"
PHONE_HREF = "tel:+16026761684"
EMAIL = "scottsdalemartialartscenter@gmail.com"
ADDRESS = "20650 N 29th Pl, Suite 103, Phoenix, AZ 85050"
MEMBER_LOGIN = "https://tko.sparkuniversity.co/"
SOCIALS = {
    "Facebook": "https://www.facebook.com/scottsdalemartialarts/",
    "Instagram": "https://www.instagram.com/scottsdalemartialarts/",
    "Google": "https://g.page/r/CXUOB7sGmLzSEAE",
    "Yelp": "https://biz.yelp.com/r2r/N_Fl9ot9rJc7LZ5_Cr4T0A",
}

# ---------------------------------------------------------------------------
# Content data
# ---------------------------------------------------------------------------

PROGRAMS = [
    dict(
        slug="preschool-martial-arts-classes-scottsdale",
        name="Preschool Martial Arts",
        tag="Ages 3–5",
        banner="kids-silhouette.png",
        banner_alt="Silhouettes of young students practicing a stance in a sunlit dojo",
        short="The perfect blend of building gross motor skills and having TONS of fun! Our preschool martial arts program in Scottsdale gives your little one the tools they need to prepare for school and life.",
        long="Discover why parents love our Preschool Martial Arts Program in Scottsdale. It’s the perfect blend of gross motor skills, personal development, and character enrichment, and gives your little one an edge when they enter a busy school setting.",
        bullets=[
            "Gross motor skills and coordination games built for little bodies",
            "Listening, following directions, and taking turns",
            "Confidence in a structured, classroom-like setting",
            "Focused, high-energy fun that gets the wiggles out",
        ],
    ),
    dict(
        slug="kids-martial-arts-classes-scottsdale",
        name="Kids Martial Arts",
        tag="Ages 6–12",
        banner="kids-silhouette.png",
        banner_alt="Silhouettes of young students practicing a stance in a sunlit dojo",
        short="Our kids martial arts program in Scottsdale gives your child the tools they need to protect themselves with self defense, but it also equips them with incredible life skills like focus, discipline, respect, and more! Watch them improve in school, too!",
        long="Parents LOVE our Scottsdale Kids Martial Arts program because it teaches not only self defense, but also vital life skills like focus, discipline, respect, and more! Watch your child’s confidence flourish and their grades improve with this awesome Child Greatness program.",
        bullets=[
            "Practical, age-appropriate self-defense fundamentals",
            "Focus and discipline that carries straight into schoolwork",
            "Respect for instructors, teammates, and family",
            "Real confidence to stand up to bullies — without becoming one",
            "A clear belt-rank path with goals to work toward",
        ],
    ),
    dict(
        slug="teen-martial-arts-classes-scottsdale",
        name="Teen Martial Arts",
        tag="Ages 13–17",
        banner="hero-kick.png",
        banner_alt="Martial artist executing a front kick, motion blur",
        short="The ultimate tech alternative that gets teens active and engaged- and helps them feel confident, too. Help your teen make friends and get off their screens with our teen martial arts classes in Scottsdale!",
        long="Combining confidence-raising fitness and life-changing self defense, our Scottsdale Teen Martial Arts program keeps your teen’s wellness and happiness in mind. It’s time to get your teenager active, making new friends and bettering themselves.",
        bullets=[
            "Real self-defense and situational awareness",
            "A screen-free outlet for stress and energy",
            "A peer community that exists outside of school",
            "Measurable progress through belt testing",
        ],
    ),
    dict(
        slug="adult-martial-arts-classes-scottsdale",
        name="Adult Martial Arts",
        tag="Adults",
        banner="hero-kick.png",
        banner_alt="Martial artist executing a front kick, motion blur",
        short="Great friends, great fun- crush your fitness goals with our adult martial arts classes in Scottsdale. Learn self defense skills and martial arts together while having a ton of fun. No more boring workouts!",
        long="Our Scottsdale Adult Martial Arts program combines next-level fitness with next-level FUN — no more boring workouts! It’s time to switch up your routine and get the results you’ve been looking for in an awesome community of like-minded people.",
        bullets=[
            "Full-body conditioning that never feels like a treadmill",
            "Practical Wado Ryu karate self-defense",
            "A community that trains together for years, sometimes decades",
            "A real rank system to measure progress against",
        ],
    ),
    dict(
        slug="teen-jujutsu-classes",
        name="Teen Jujutsu",
        tag="Ages 13+",
        banner="jujutsu-grapple.png",
        banner_alt="Two students grappling on the tatami mat, motion blur",
        short="Today’s teens need more than just a workout — they need a place where they can challenge themselves, build confidence, and learn real skills that matter. That’s exactly what our Teen Jujutsu classes in Scottsdale provide.",
        long="Give your teen the tools to succeed on and off the mat with our Teen Jujutsu classes in Scottsdale. Designed specifically for ages 13+, this program blends the tradition of martial arts with the practical skills today’s teens need most.",
        bullets=[
            "Grappling and ground-control fundamentals",
            "Instruction under Hoteikan Jujutsu’s certified coaches",
            "Discipline that transfers to real challenges off the mat",
            "A built-in path into our Elite Competition Team",
        ],
    ),
    dict(
        slug="adult-jujutsu-classes",
        name="Adult Jujutsu",
        tag="Adults",
        banner="jujutsu-grapple.png",
        banner_alt="Two students grappling on the tatami mat, motion blur",
        short="Perfect for a mix of self-defense and real-world applications, adult Jujutsu in Scottsdale is a must if you’re looking for serious martial arts. Jujutsu in Scottsdale will transform your physique while crushing your fitness goals, all while you learn useful and practical self-defense skills.",
        long="Our Scottsdale adult Jujutsu classes are no joke! If you’re ready to ramp up your fitness like never before, learn real-world self defense skills and make new friends while you learn Jujutsu, this is the program for you!",
        bullets=[
            "Olympic-style tatami mat training",
            "Practical grappling for real-world self-defense",
            "A demanding, effective full-body workout",
            "Training under Hoteikan Jujutsu’s senior instructors",
        ],
    ),
    dict(
        slug="weapons-classes-scottsdale",
        name="Weapons",
        tag="All ranks",
        banner="weapons-rack.png",
        banner_alt="Traditional kobudo weapons — bo staff, nunchaku, and sai — on display",
        short="Transform your entire body into a self-defense machine while learning a skill set that could save your life.",
        long="Protect yourself and learn real-world self defense skills with Weapons classes! Our Kobudo program trains traditional Okinawan weapons in a safe, structured environment.",
        bullets=[
            "Traditional Okinawan Kobudo weapons training",
            "Sharper balance, timing, and body control",
            "A rare, specialized skill set few schools teach",
            "A path toward Kobudo black belt rank",
        ],
    ),
]

TESTIMONIALS = [
    "Best karate school in the state!",
    "SMAC has imparted invaluable life lessons to our boys as well, helping them to become leaders, with self confidence and respect for others!",
    "The dedication they have to teaching Karate but most importantly character and life lessons to the students is inspiring!",
    "It is great to have true karate professionals in the Valley. Scottsdale Martial Art Center is a reputable Martial Arts Center!",
    "I love Scottsdale Martial Arts Center!! I feel very fortunate to have found this school and recommend it to anyone with children!",
]

FAQS = [
    (
        "Will my child become a bully?",
        "We find that our students become more confident to stand up to bullies and have more humility and kindness to others through their martial arts lessons.",
    ),
    (
        "Are parents allowed to watch?",
        "Absolutely. Every training floor has a dedicated viewing area with bleacher seating, so you can watch class from arrival to bow-out.",
    ),
    (
        "Do I need to be fit for this?",
        "Not at all. Our programs are built to meet you where you are, from complete beginners to lifelong athletes — the fitness comes as a side effect of consistent training.",
    ),
    (
        "How long until I get my black belt?",
        "It depends on the student and the program, but most dedicated students train for several years. We hold formal belt testing four times a year — March, June, September, and December — so progress is steady and clearly marked.",
    ),
    (
        "How do I claim your limited time offer?",
        "We only have a certain amount of space in our martial arts training area. Take advantage of our limited time offer — the fastest way is to fill in the form. You can also always call us; we’d love to chat about what we do and whether our Scottsdale martial arts classes would be a great fit for you and your family!",
    ),
    (
        "What do I need to bring to my first martial arts lesson?",
        "Just comfortable workout clothes and a water bottle. We’ll get you set up with everything else for your trial class.",
    ),
    (
        "I’m not very sporty or coordinated — will that be a problem?",
        "Not even a little. Many of our most accomplished students started out with zero athletic background — our instructors build everyone up one class at a time.",
    ),
]

HISTORY = [
    ("1976", "Arizona Wado Karate", "Scottsdale Martial Arts Center, Inc. had its beginning under the name Arizona Wado Karate. The center was originally located in Mesa and was owned and operated by Sensei Marlon Moore."),
    ("1986", "Ray Hughes takes the helm", "Sensei Marlon Moore came down with a debilitating illness and turned over operations to his senior student, Ray Hughes. While managing the school, Ray started a second location in Scottsdale at the YMCA, running both under the Arizona Wado Karate name until Sensei Moore returned — after which Ray opened a school in the Scottsdale Airpark, managing both locations until 2002."),
    ("1993", "One school, ten arts", "Ray decided to change the school from a karate-only facility to a multiple-art facility, opening the benefits of martial arts to more people of every age and skill level. The school offered ten different arts and was renamed Scottsdale Martial Arts Center, Inc. to reflect its new direction."),
    ("1998", "Building the dream", "The center had outgrown its space, so Ray began the process of designing and building his own facility — gathering a group of parents from the program who were experts in finance, law, and real estate to help develop Scottsdale’s first purpose-built martial arts center."),
    ("2002", "Doors open", "After nearly four years — about the same time it takes an adult to earn a traditional black belt — Scottsdale Martial Arts Center, Inc. opened its doors on September 5, 2002. That same year, Sensei Ray Hughes handed the YMCA program over to one of his students."),
    ("Today", "Scottsdale’s premier martial arts center", "SMAC is Scottsdale’s oldest martial arts school — and today it’s thriving as the largest and most diversified, too."),
]

FACILITY_FEATURES = [
    ("Main Training Floor", "Rubberized foam mats — the same type used in national and international competitions — plus a large bleacher section for parents, and a state-of-the-art HD projector with an 8 sq. ft. screen for filming class or showing training footage."),
    ("Second Training Floor", "A grappling floor of tatami mats, the same mats used in Olympic judo competition, with its own large viewing area for parents and friends."),
    ("Third Training Floor", "A multi-use floor for karate, weapons training, and other martial arts, with a large viewing area for parents and friends."),
    ("Dressing Rooms", "Separate dressing rooms for men and women, complete with lockers and showers."),
    ("Children’s Playroom", "A dedicated, padded-floor playroom with toys and movies for toddlers to enjoy while siblings train. This is an unsupervised playroom — supervising your child here remains a parent’s responsibility."),
]

INSTRUCTORS = [
    dict(
        name="Ray Hughes",
        role="SMAC Owner — President, Arizona Wado Karate — WKF Official — USA Karate Technical Committee",
        summary=(
            "Ray Hughes is the owner of Scottsdale Martial Arts Center, Inc. (SMAC) — the oldest and largest martial "
            "arts school in Scottsdale, Arizona, which he started in 1986. He is President of Arizona Wado and a member "
            "of the Technical Committee of USA Karate."
        ),
        body=(
            "Mr. Hughes started training in Wado karate in 1976 under Sensei Marlon Moore in Mesa, Arizona. He went "
            "full-time with karate in 1986 and built his own dojo in 2002.\n\n"
            "Ray Hughes holds dan (black belt) ranks in Wado Ryu (4th), JKF Wado Kai (5th), USNKF (6th), 6th dan "
            "awarded by the late Dan Ivan, 7th dan from USA Karate-do Kyokai with Sensei Chuck Merriman and Sensei Lee "
            "Gray on the testing board, and USA Wado Federation (7th).\n\n"
            "Mr. Hughes had an extensive competition career spanning the 1970s through the 2000s. Beyond numerous "
            "local and regional championships, Ray competed on five USA Karate Teams — two that won gold and one "
            "that won silver. His standout year was 1986, when he was voted Outstanding Competitor at the Osawa "
            "Traditional Karate Championships in Las Vegas (and awarded a trip to Japan), Outstanding Competitor at "
            "the USA Wado Ryu Karate Championships in Utah, and School and Competitor of the Year by USA Wado.\n\n"
            "Though Mr. Hughes teaches all age groups and skill levels, his passion is the positive development of "
            "youth through traditional martial arts. He has formed two nonprofit corporations — USA Karate Arizona "
            "ASO and Champions Foundation of Arizona — to further this cause. His mission is to give every child in "
            "Arizona the opportunity to learn life skills through traditional martial arts, and to connect students "
            "with a quality school in their area, regardless of style or art."
        ),
        record=[
            ("2015", "“Man of the Year,” USA Karate"),
            ("1998", "National Champion, Gold Medal — USNKF, Over-40 Kumite (Sparring)"),
            ("1997", "National Champion, Gold Medal — USNKF, Over-40 Kumite (Sparring)"),
            ("1989", "World Wado Championships — London, England"),
            ("1988", "All Japan Wado-Ryu Championships — Yokohama, Japan; Team USA silver medal"),
            ("1986", "Outstanding Competitor, Traditional Karate Championships (Las Vegas) — awarded trip to Japan; Grand Champion, USA Wado Karate Championships (Utah Open), defeating a three-time grand champion; Competitor of the Year and School of the Year, USA Wado-Ryu Karate-Do Federation"),
            ("1985", "USA vs. Canada National Team — Vancouver, Canada; Team USA gold medal"),
            ("1984", "All Japan Wado-Ryu Karate Championships — Tokyo, Japan; USA vs. Canadian National Team, Orange County, CA — Team USA gold medal"),
        ],
    ),
    dict(
        name="Christian Stienstra",
        role="Elite Instructor — Head of the SMAC Elite Competition Team",
        summary="Began Wado training in November 2009 and Kobudo in 2010. Elite Instructor and Head of the SMAC Elite Competition Team since 2020, teaching at SMAC since 2014.",
        body="",
        record=None,
        bullets=[
            "Shodan (1st degree black belt), December 2016 — Nidan (2nd degree), December 2020",
            "Brown Belt in Kobudo (Weapons), 2015 — Shotokan Black Belt, 2018",
            "Elite Athlete since 2015; two-time Junior US Team Member; ISKF National Team Member",
            "7-time US Open medalist; 5-time National Kumite medalist (2 gold, 1 silver, 2 bronze)",
            "3-time Wado Specific Finalist",
            "USANKF Certified Kata and Kumite Coach since 2016",
        ],
    ),
    dict(
        name="Duane Abbajay",
        role="Elite Instructor — in memoriam",
        summary="Sensei Duane passed away on December 6, 2022, after a long illness. It is an honor to keep his name listed here as one of our great instructors.",
        body=(
            "“I brought my son in to try SMAC in 2006 after having tried a couple of different dojos. I was invited to "
            "try the adult class in 2008 by Sensei Ray Hughes. My wife Paula also began training shortly thereafter. "
            "We found ourselves really enjoying the many friendships with other families.\n\n"
            "A few years later, I experienced one of the proudest moments of my life, receiving a black belt with my "
            "son Frazier in 2013.\n\n"
            "Karate has had so many unexpected benefits, including a much-enhanced awareness in everyday life — even "
            "interacting with customers at my work. It has been a great life coping tool, from dealing with the loss "
            "of a loved one to my own life-threatening illness.\n\n"
            "Today, having the opportunity to teach others is a great honor. Assisting them in their personal journey "
            "means to me not so much suggesting what to see, but more importantly, where to look.”"
        ),
        record=None,
        bullets=[
            "Shodan (1st degree black belt), 2013 — Nidan (2nd degree), 2018",
            "Competed at both the US Open and US Nationals, winning gold and silver at the 2010 U.S. Nationals",
            "Served on belt promotion boards and as a tournament referee",
        ],
    ),
    dict(
        name="Kyle Harder",
        role="Elite Instructor",
        summary="Started training in January 1989 at age 5. Has competed in over 500 tournaments and trained under Ray Hughes for 26 years and counting.",
        body="",
        record=None,
        bullets=[
            "Junior Black Belt in Wado at age 11 (1995); trained in Judo for 3 years, ages 13–15",
            "1st degree Black Belt, Shotokan Karate (2008) — 2nd degree Black Belt, Wado (2009)",
            "WKF Referee Standards, Category C Judges Certification for Kumite (2012)",
            "Team USA for the Wado World Championships — Tokyo 1999, Vancouver 2008, Nagoya 2010",
            "Gold, Team Kumite, US National ISKF Karate Tournament (San Francisco) with the Southwest Karate Kumite Team",
            "Teaching Private Lessons since earning his Black Belt in Wado",
        ],
    ),
    dict(
        name="Scott Harrow",
        role="Elite Instructor — SMAC Elite Competition Team Coach",
        summary="Began training in March 2001 and Kobudo/Kobujutsu (weapons) in September 2003. Teaches all levels, from 4-year-old white belts to adult black belts.",
        body="",
        record=None,
        bullets=[
            "Shodan (1st degree), December 2005 — Nidan, November 2009 — Sandan, December 2014 — Yondan, December 2021",
            "Shodan rank in Okinawan Kobudo, December 2009",
            "USANKF Kata and Kumite certified Official since 2012",
            "USANKF SafeSport accredited Coach (SafeSport training + NCSI background check) since 2014",
            "SMAC Elite Competition Team Coach since 2013",
            "Trained in Jujitsu (2001–2002) and Shito Ryu karate since 2007; on belt promotion boards since 2005",
        ],
    ),
    dict(
        name="Pamela Carrus",
        role="Elite Instructor",
        summary="Training since 1986. Current rank: Godan (5th degree black belt). Teaching since 1996.",
        body="",
        record=None,
        bullets=[
            "Shodan (1st degree black belt), 1996",
            "1999 World Wado-Ryu Karate-Do Championship, Tokyo, Japan — Women’s Black Belt Kumite Team, 3rd place",
            "1999 Western States Championship — Individual and Team Kumite, 2nd place",
            "2001 & 2002 Sportsmanship Invitational — Women’s Black Belt Individual Grand Champion",
        ],
    ),
    dict(
        name="Peter Wehner",
        role="Elite Instructor",
        summary="Began Wado-ryu Karate in 1998 under Sensei Ray Hughes, after training in Shito-ryu Karate from 1994 to 1997. Teaching children and adults since 2010.",
        body="",
        record=None,
        bullets=[
            "Shodan (1st degree), 2001 — Nidan, 2006 — Sandan, 2011 — Yondan, 2017",
            "A family affair: his eldest son earned his Shodan at age 15 after 10 years of training, and his wife currently trains as a brown belt",
        ],
    ),
    dict(
        name="Mary Tatum",
        role="Elite Instructor — Belt Promotion Board",
        summary="Began karate study in 1994 and found SMAC in 1999, training in Wado Kai under Sensei Ray Hughes ever since. A member of the Belt Promotion Board since 2004.",
        body=(
            "Mary also trains in Okinawa Kobudo and Kobujitsu since 2003 (Sho Dan black belt, 2010), Shito Ryu and "
            "Goju Ryu under Sensei’s Robert & Robin Hunt since 2003, and Hoteikan Judo/Jujitsu since 2005.\n\n"
            "She earned the 2011 Power Play of the Year Award from the Grand Canyon State Games, recognizing "
            "exceptional character and sportsmanship, and has competed in the Summer and Winter Games since 2000. "
            "Her first tournament, in 1999 as a white belt, earned her a Gold Medal at age 60 — she’s since collected "
            "over 50 medals, including Gold in Kata and Silver in Kumite at the AAU National Karate Championship in "
            "her 55+ age division."
        ),
        record=None,
        bullets=[
            "Shodan (1st degree), 2005 — Nidan, 2009 — Sandan, 2015 — Yondan, 2022",
            "USA National Karate Federation Judge/Referee Certification, 2011",
            "Member: USA National Karate Federation, USA Karate, and the Japan Karate Federation",
        ],
    ),
    dict(
        name="Susana Romo",
        role="Elite Instructor",
        summary="Started training in 1992. USA–NKF Judge since 2011, with Kata Judge C and Kumite Referee D certifications.",
        body="",
        record=None,
        bullets=[
            "Shodan, 1999 — Nidan, 2002 — Sandan, mid-2000s — Yondan, 2015",
            "1999 World Wado-Ryu Karate-Do Championship, Tokyo, Japan — Women’s Black Belt Kumite Team, 3rd place",
            "1999 Arizona Sportsmanship Invitational — Kata & Kumite Grand Champion",
            "Taught private lessons (1999–2004) and co-taught classes (1997–2006)",
        ],
    ),
    dict(
        name="Gabe Williams",
        role="Instructor",
        summary="Started training in 2010, earned his Shodan (1st degree black belt) in 2020, and began teaching that same year.",
        body="",
        record=None,
        bullets=[],
    ),
    dict(
        name="Isabelle Kar",
        role="Instructor",
        summary="Part of the SMAC instructor team.",
        body="",
        record=None,
        bullets=[],
    ),
]

WEEKLY_SCHEDULE = {
    "Monday": [
        ("White", "4:00 – 4:30 PM"),
        ("Green/Purple", "4:00 – 5:15 PM"),
        ("Yellow – Blue", "5:15 – 6:00 PM"),
        ("Application", "6:00 – 6:30 PM"),
        ("Teen/Adult", "6:30 – 7:30 PM"),
        ("Elite", "7:30 – 8:30 PM"),
    ],
    "Tuesday": [
        ("Lil Champions", "4:00 – 4:30 PM"),
        ("Yellow – Blue", "4:30 – 5:15 PM"),
        ("Green/Purple", "5:15 – 6:00 PM"),
        ("Application", "6:00 – 6:30 PM"),
        ("Brown Belt", "6:30 – 7:30 PM"),
        ("Competition", "7:30 – 8:30 PM"),
    ],
    "Wednesday": [
        ("White", "4:00 – 4:30 PM"),
        ("Green/Purple", "4:30 – 5:30 PM"),
        ("Yellow/Blue", "5:30 – 6:30 PM"),
        ("Teen/Adult", "6:30 – 7:30 PM"),
        ("Competition", "7:30 – 8:30 PM"),
    ],
    "Thursday": [
        ("Lil Champions", "4:00 – 4:30 PM"),
        ("Yellow – Blue", "4:30 – 5:30 PM"),
        ("Green/Purple", "5:30 – 6:30 PM"),
        ("Advanced Sparring", "6:30 – 7:30 PM"),
        ("Black Belt", "7:30 – 8:30 PM"),
    ],
    "Friday": [
        ("Lil Champions", "4:00 – 4:30 PM"),
        ("Leadership", "4:30 – 5:30 PM"),
        ("Competition", "5:30 – 7:30 PM"),
    ],
    "Saturday": [
        ("Competition", "11:00 – 12:30 PM"),
        ("Lil Champions", "12:30 – 1:00 PM"),
        ("Yellow – Blue", "1:00 – 2:00 PM"),
        ("Green/Purple", "2:00 – 3:00 PM"),
        ("Application", "3:00 – 3:30 PM"),
        ("Brown/Black", "3:30 – 4:30 PM"),
    ],
    "Sunday": [],
}

TESTING_DATES = [
    ("March", [("Green/Purple", "March 18 @ 4:30"), ("Yellow–Blue", "March 19 @ 4:30"), ("Teen/Adult", "March 23 @ 6:30"), ("Brown Belt", "March 24 @ 6:30")]),
    ("June", [("Green/Purple", "June 17 @ 4:30"), ("Yellow–Blue", "June 18 @ 4:30"), ("Teen/Adult", "June 22 @ 6:30"), ("Brown Belt", "June 23 @ 6:30")]),
    ("September", [("Green/Purple", "Sept. 16 @ 4:30"), ("Yellow–Blue", "Sept. 17 @ 4:30"), ("Teen/Adult", "Sept. 21 @ 6:30"), ("Brown Belt", "Sept. 22 @ 6:30")]),
    ("December", [("Green/Purple", "Dec. 9 @ 4:30"), ("Yellow–Blue", "Dec. 10 @ 4:30"), ("Teen/Adult", "Dec. 14 @ 6:30"), ("Brown Belt", "Dec. 15 @ 6:30")]),
]

TESTING_CURRICULUM = [
    (
        "Teen / Adult",
        [
            "Basics: Lunge Punch, Low Block, Kick → Lunge Punch, Front Kick, Flying Front Kick, Surikomi Front Kick",
            "Advanced Basics: Junzuki No Tsukomi, Keta Junzuki No Tsukomi",
            "Miscellaneous: Renrakuwaza Ipponme, Sanbon Jodan Uke 1",
            "Kata to your current belt level",
            "Striking: Lunge Punch, Reverse Punch, Elbow, Front Kick, Roundhouse Kick, Reverse Elbow",
        ],
    ),
    (
        "Brown Belt",
        [
            "Basics: Lunge Punch, Low Block, Spinning Back Kick, Roundhouse Kick, Surikomi Front Kick",
            "Advanced Basics: Junzuki No Tsukomi, Keta Junzuki No Tsukomi",
            "Miscellaneous: Renrakuwaza Ipponme, Sanbon (TBD)",
            "Kata: Shodan, Nidan, and Kushanku",
        ],
    ),
]

EVENTS_2026 = [
    ("May", "11", "Bring Your Mom to Class Day", ""),
    ("May", "23", "Parents Night Out", ""),
    ("June", "1–5", "Summer Camp — Week 1", ""),
    ("June", "8–12", "Summer Camp — Week 2", ""),
    ("June", "15–19", "Summer Camp — Week 3", ""),
    ("June", "22–26", "Summer Camp — Week 4", ""),
    ("June", "22", "Bring Your Dad to Class Day", ""),
    ("July", "25", "Parents Night Out", ""),
    ("August", "TBD", "Women’s Self Defense", "Date to be announced"),
    ("August", "22", "Ice Cream Social", ""),
    ("Aug 31 – Sep 1", "", "Bring a Friend to Class", ""),
    ("September", "26", "Parents Night Out", ""),
    ("October", "29", "Halloween Party", ""),
    ("November", "21", "Parents Night Out", ""),
    ("December", "TBD", "Holiday Party", "Date to be announced"),
]

BLOG_POSTS = [
    dict(
        slug="5-ways-martial-arts-builds-confidence-in-kids",
        title="5 Ways Martial Arts Builds Confidence in Kids",
        date="2026-01-14",
        tag="Kids & Parenting",
        banner="kids-silhouette.png",
        banner_alt="Silhouettes of young students practicing a stance in a sunlit dojo",
        excerpt="Confidence isn’t something you can hand a child — it’s built one small win at a time. Here’s how a structured martial arts program does exactly that.",
        body="""Every parent has heard some version of “martial arts builds confidence,” and it’s tempting to file it away as a marketing line. But the mechanism behind it is pretty concrete, and it shows up in specific, repeatable ways in our Preschool and Kids programs.

## 1. Small goals, delivered often
A belt system breaks a huge, abstract goal (“be good at karate”) into dozens of small, achievable ones. A stripe on a belt, a new kata, a passed stance check — kids get to feel the specific, physical proof of progress far more often than they would waiting for a report card.

## 2. Performing under (low-stakes) pressure
Reciting a kata in front of the class, or sparring in front of parents in the bleacher seats, is a small dose of performance pressure in a safe, supportive room. Kids who practice being looked at while they try something hard get more comfortable doing that everywhere else — the classroom, the stage, the field.

## 3. A vocabulary for self-control
Focus, discipline, and respect aren’t abstract virtues in a dojo — they’re words a 7-year-old hears and practices every single class, attached to concrete actions like bowing in, waiting their turn, and listening for a command. That vocabulary travels home and to school.

## 4. Real self-defense, not just a slogan
Confidence that stands up to a bully isn’t bravado — it’s knowing, physically, that you could protect yourself if you had to. That knowledge changes how a kid carries themselves, which is usually enough to defuse a situation before it starts.

## 5. A community that notices you
In a class of 15, an instructor learns your name, your goals, and your sticking points. That kind of attention, given consistently over months and years, is one of the most reliable confidence-builders there is — and it’s a big part of why so many SMAC families stick around long after their first belt.""",
    ),
    dict(
        slug="what-to-expect-your-first-class",
        title="What to Expect at Your First Class",
        date="2026-02-03",
        tag="New Students",
        banner="hero-kick.png",
        banner_alt="Martial artist executing a front kick, motion blur",
        excerpt="Walking into a dojo for the first time can feel intimidating. Here’s exactly what happens, from the moment you check in to your first bow-out.",
        body="""If you’ve never set foot in a martial arts school before, it’s completely normal to feel a little nervous about your first class. Here’s what actually happens, step by step.

## Before class
You’ll check in at the front desk and meet the instructor teaching your program. Bring comfortable workout clothes and a water bottle — we’ll get you set up with a loaner uniform if you don’t have one yet. Parents are welcome to watch from the bleacher seating on any of our three training floors for the entire class.

## The warm-up
Class opens with a formal bow-in, a tradition that marks the transition from the outside world into training. From there, expect a warm-up built around the basic movements of Wado Ryu karate: stances, blocks, and strikes, broken down slowly so a first-timer can follow along right next to students who have trained for years.

## The main class
Depending on the program, you’ll work through basics (kihon), a simple form (kata), and some partner drills. Nobody expects a first-time student to keep up perfectly — instructors are actively watching for exactly that, and will adjust pace and correct form one-on-one.

## Bow-out
Class ends the way it began: lined up by rank, with a formal bow. Most first-time students are surprised by how much they picked up in forty-five minutes, and by how normal it starts to feel almost immediately.

## After class
We’ll talk through what you thought, answer any questions, and help you figure out which program and schedule fits your family best. No pressure, no hard sell — just an honest conversation about whether SMAC is a good fit.""",
    ),
    dict(
        slug="belt-testing-101",
        title="Belt Testing 101: How Promotion Works at SMAC",
        date="2026-02-24",
        tag="Belt Ranks",
        banner="belt-knot.png",
        banner_alt="Close-up of hands tying a black belt",
        excerpt="White to black isn’t a straight line — it’s a ladder with real rungs. Here’s how our testing schedule and curriculum actually work.",
        body="""“How long until my kid gets their black belt?” is one of the most common questions we get, and the honest answer is: it depends on the student. But the structure behind that answer is very concrete, and it’s worth understanding.

## Testing happens four times a year
SMAC holds formal belt testing in March, June, September, and December (exact dates can shift for June, September, and December — check the current Schedule page). Each testing date is organized by rank group, so a Green/Purple belt tests on a different evening than a Teen/Adult or Brown Belt candidate.

## Every rank has a curriculum
Testing isn’t a formality — it’s a checklist. Teen/Adult testing, for example, covers a set list of basics (lunge punch, low block, front kick and its variations), advanced basics, a kata matched to the student’s current belt, and striking combinations. Brown Belt testing adds spinning back kick and roundhouse kick fundamentals and specific kata — Shodan, Nidan, and Kushanku. Instructors review the full curriculum for each test in class beforehand, so nobody walks in unprepared.

## Belt promotion boards
Several of our senior instructors, including Mary Tatum, sit on SMAC’s Belt Promotion Board, reviewing testing performance and signing off on advancement. It’s a second set of experienced eyes on every promotion, not just the judgment of a single instructor.

## Why the pace varies
An adult training two nights a week and a homeschooled teen training five will simply progress at different speeds — and that’s by design. We’d rather a student earn each belt honestly than rush a rank they can’t yet demonstrate. What stays consistent is the structure: four testing windows a year, a clear curriculum, and instructors who will tell you exactly what you need to work on before your next attempt.""",
    ),
    dict(
        slug="teens-trading-screens-for-the-dojo",
        title="Why Teens Are Trading Screen Time for the Dojo",
        date="2026-03-17",
        tag="Teens",
        banner="jujutsu-grapple.png",
        banner_alt="Two students grappling on the tatami mat, motion blur",
        excerpt="Between school, social media, and everything in between, teens are more sedentary and more online than ever. Here’s what a few hours a week on the mat can change.",
        body="""Teenagers today spend more time looking at a screen than any generation before them — and a lot of parents are looking for something that gets their teen moving, off their phone, and around other people without a fight at the dinner table. Martial arts consistently works for reasons that have very little to do with punching and kicking.

## It’s social in a way that doesn’t feel forced
Unlike a lot of team sports, there’s no bench. Every teen in a Teen Martial Arts or Teen Jujutsu class is training, drilling with a partner, or sparring — which means the social connection happens naturally, shoulder to shoulder, instead of through a screen.

## Grappling gives high-energy teens somewhere to put it
Our Teen Jujutsu program, taught under Hoteikan Jujutsu’s certified coaches, channels a teenager’s competitive energy into a highly technical, physically demanding skill — ground control, positioning, real self-defense — rather than letting it curdle into restlessness or conflict elsewhere.

## Belt testing gives them a goal that isn’t graded by someone else
Teenagers get a lot of external evaluation — grades, college prep, social media. A belt test is one of the few goals that’s entirely theirs: they set the pace, they put in the reps, and they either demonstrate the material or they don’t. That kind of ownership is rare, and teens respond to it.

## It’s a real, practical skill
Self-defense isn’t an abstraction for a teenager who’s starting to navigate more of the world independently — driving, part-time jobs, going out with friends. Knowing they can protect themselves is a different kind of confidence than being told to “be careful.”

If your teen has been resistant to “just go outside and do something,” a trial class is a low-pressure way to see if this is the something that sticks.""",
    ),
    dict(
        slug="meet-the-elite-competition-team",
        title="Meet the SMAC Elite Competition Team",
        date="2026-04-08",
        tag="Competition",
        banner="hero-kick.png",
        banner_alt="Martial artist executing a front kick, motion blur",
        excerpt="Led by Christian Stienstra, our Elite Competition Team trains students who want to take their kata and kumite beyond the dojo and onto the national stage.",
        body="""Not every student wants to compete — and that’s completely fine, most don’t. But for the ones who do, SMAC runs a dedicated Elite Competition Team for students ready to take their training beyond belt testing and onto the tournament floor.

## Led by a competitor, not just a coach
The team is headed by Christian Stienstra, an Elite Instructor who has trained at SMAC since 2014. Christian is a two-time Junior US Team Member, an ISKF National Team Member, a 7-time US Open medalist, and a 5-time National Kumite medalist — which means the athletes on our Elite team are learning tournament kata and kumite from someone who has stood on those exact mats himself, recently.

## A coaching staff with real credentials
Scott Harrow, SMAC Elite Competition Team Coach since 2013, is USANKF Kata and Kumite certified and SafeSport accredited. Between Christian and Scott — and the rest of our Elite Instructor team, several of whom have competed internationally for Team USA — competitors get coaching grounded in current rules, current judging standards, and real tournament experience.

## What it actually involves
Competition class runs several nights a week (see the current class Schedule for exact times), on top of regular belt-level training. It’s not a replacement for the core curriculum — it’s an addition, for students who’ve already built a strong foundation and want to sharpen it against outside competition.

## Is it right for your student?
If your student has been asking about tournaments, or an instructor has mentioned they might be ready, the best next step is a conversation with your instructor. The Elite team is an invitation, not a requirement — and it exists because some of our students genuinely love the sport side of martial arts as much as the traditional side.""",
    ),
    dict(
        slug="wado-ryu-vs-jujutsu",
        title="Wado Ryu vs. Jujutsu: What’s the Difference, and Do You Need Both?",
        date="2026-05-05",
        tag="Martial Arts 101",
        banner="facility-floor.png",
        banner_alt="An open martial arts training floor with mats and bleacher seating",
        excerpt="SMAC teaches both a striking art and a grappling art under one roof. Here’s what actually separates them — and why a lot of our students end up training both.",
        body="""New families often ask whether they should sign up for karate or Jujutsu, assuming they need to choose one. At SMAC, that’s less of an either/or than it sounds.

## Wado Ryu: distance and striking
Our core curriculum is Wado Ryu karate, taught under the Wado International Karate Federation (WIKF). Wado Ryu is a striking art built around body-shifting — using footwork and angles to avoid an attack while striking, rather than absorbing contact head-on. It’s the foundation of our Preschool through Adult Martial Arts programs, and the art most of our belt testing curriculum is built around.

## Hoteikan Jujutsu: control at close range
Once a confrontation closes to grappling range, striking distance stops mattering. That’s where Jujutsu comes in. All grappling instruction at SMAC runs under Hoteikan Jujutsu, led by Chief Instructor Sensei Dan Pensabene (6th degree black belt, San Do Ichi Ryu Jujutsu), with senior instructors Sensei Ken Wong and Sensei Kirk Householder. It’s taught on the same Olympic-style tatami mats used in judo competition, with an emphasis on ground control and practical self-defense over striking.

## Why a lot of students train both
A striking art and a grappling art cover different ranges of a real confrontation — which is exactly why so many serious martial artists eventually train both. Several of our own instructors, including Mary Tatum, hold rank in both Wado Ryu karate and Jujutsu-family arts. You don’t have to start there: most students begin with our core Martial Arts program and add Teen or Adult Jujutsu later, once they’re looking for the next challenge.

## So which should you start with?
If you’re not sure, start with the program that matches your age group’s core Martial Arts class — it’s the foundation everything else builds on. Jujutsu is there when you’re ready for it, not instead of it.""",
    ),
]

# ---------------------------------------------------------------------------
# Shared markup
# ---------------------------------------------------------------------------

def head(title, description, root):
    return f"""<meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description}" />
  <link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,650;9..144,750&family=IBM+Plex+Sans:wght@400;500;600;650&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{root}assets/css/styles.css" />
"""


def logo_mark():
    return """<svg class="brand-mark" width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <circle cx="20" cy="20" r="19" stroke="#a3271e" stroke-width="2"/>
        <path d="M11 24.5C11 24.5 15 15 20 15C25 15 29 24.5 29 24.5" stroke="#17150f" stroke-width="2" stroke-linecap="round"/>
        <path d="M14 24.5H26" stroke="#a3271e" stroke-width="2" stroke-linecap="round"/>
        <circle cx="20" cy="10.5" r="1.8" fill="#a3271e"/>
      </svg>"""


NAV_ITEMS = [
    ("Home", "index.html"),
    ("About Us", "about.html"),
    (None, None),  # programs dropdown handled separately
    ("Schedule", "schedule.html"),
    ("Upcoming Events", "events.html"),
    ("Blog", "blog.html"),
    ("Client Info & Media", "client-info-media.html"),
]


def nav(root, active):
    def link(label, href, key):
        cls = "nav-link" + (" is-active" if active == key else "")
        return f'<li><a class="{cls}" href="{root}{href}">{label}</a></li>'

    items = []
    items.append(link("Home", "index.html", "home"))
    items.append(link("About Us", "about.html", "about"))

    prog_links = "\n".join(
        f'<a href="{root}programs/{p["slug"]}.html">{p["name"]}</a>' for p in PROGRAMS
    )
    prog_cls = "nav-link" + (" is-active" if active == "programs" else "")
    items.append(f"""<li class="has-dropdown">
        <a class="{prog_cls}" href="{root}programs/">Programs</a>
        <div class="dropdown">{prog_links}</div>
      </li>""")

    items.append(link("Schedule", "schedule.html", "schedule"))
    items.append(link("Upcoming Events", "events.html", "events"))
    items.append(link("Blog", "blog.html", "blog"))
    items.append(link("Client Info &amp; Media", "client-info-media.html", "client"))

    return "\n      ".join(items)


def header(root, active):
    return f"""<a class="skip-link" href="#main">Skip to content</a>
  <div class="topbar">
    <div class="container">
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="{PHONE_HREF}">{PHONE}</a>
    </div>
  </div>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="{root}index.html">
        {logo_mark()}
        <span class="brand-text">
          <strong>SMAC</strong>
          <span>Scottsdale Martial Arts Center</span>
        </span>
      </a>
      <nav class="primary-nav" id="primary-nav">
        <ul>
          {nav(root, active)}
        </ul>
        <div class="container">
          <a class="btn btn-primary btn-block" href="{MEMBER_LOGIN}" target="_blank" rel="noopener">Member Login</a>
        </div>
      </nav>
      <div class="header-cta">
        <a class="btn btn-ghost btn-sm" href="{MEMBER_LOGIN}" target="_blank" rel="noopener">Member Login</a>
        <a class="btn btn-primary btn-sm" href="{root}index.html#trial">Free Trial</a>
        <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false" aria-controls="primary-nav">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>"""


def footer(root):
    prog_links = "\n            ".join(
        f'<li><a href="{root}programs/{p["slug"]}.html">{p["name"]}</a></li>' for p in PROGRAMS
    )
    social_icons = {
        "Facebook": '<path d="M13.5 9H15V6.5h-1.5c-1.66 0-3 1.34-3 3V11H9v2.5h1.5V19H13v-5.5h1.8l.3-2.5H13v-1.25c0-.41.34-.75.75-.75Z" fill="currentColor"/>',
        "Instagram": '<rect x="6" y="6" width="12" height="12" rx="3.5" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5"/><circle cx="15.7" cy="8.3" r="0.9" fill="currentColor"/>',
        "Google": '<path d="M18.5 12.2c0-.6-.05-1.1-.15-1.6H12v3h3.7c-.16.9-.65 1.6-1.4 2.1v1.8h2.2c1.3-1.2 2-3 2-5.3Z" fill="currentColor"/><path d="M12 19c1.9 0 3.4-.6 4.5-1.7l-2.2-1.8c-.6.4-1.4.7-2.3.7-1.8 0-3.3-1.2-3.8-2.8H5.9v1.8C7 17.7 9.3 19 12 19Z" fill="currentColor"/><path d="M8.2 13.4c-.15-.4-.2-.9-.2-1.4s.05-1 .2-1.4V8.8H5.9A7 7 0 0 0 5 12c0 1.1.3 2.2.9 3.2l2.3-1.8Z" fill="currentColor"/><path d="M12 7.8c1 0 1.9.35 2.6 1l2-2A6.9 6.9 0 0 0 12 5c-2.7 0-5 1.3-6.1 3.8l2.3 1.8c.5-1.6 2-2.8 3.8-2.8Z" fill="currentColor"/>',
        "Yelp": '<path d="M12 6c-.5 3-1 5-1.3 6 1-.3 3.2-1.1 5.8-1.8-.6-1.7-2.5-3.5-4.5-4.2Z" fill="currentColor"/><path d="M9.8 13.2C8.7 13 6.4 12.6 5 12.4c.4 1.9 1.8 3.8 3.6 4.6.3-1 .8-2.7 1.2-3.8Z" fill="currentColor"/><path d="M11.4 13.9c-.6.9-1.7 2.7-2.3 3.7 1.7.7 3.9.6 5.5-.4-.9-.8-2.3-2.2-3.2-3.3Z" fill="currentColor"/><path d="M13.4 12.6c.9.6 2.7 1.8 3.7 2.4.5-1.8.1-3.9-1-5.4-.8.8-1.9 2-2.7 3Z" fill="currentColor"/>',
    }
    social_links = "\n        ".join(
        f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}"><svg width="18" height="18" viewBox="0 0 24 24">{social_icons.get(name, "")}</svg></a>'
        for name, url in SOCIALS.items()
    )
    year_line = "Scottsdale Martial Arts Center provides martial arts classes to Scottsdale, Phoenix, Cave Creek, N Phoenix, Paradise Valley, North Scottsdale, Greyhawk &amp; McDowell Mountain communities."

    return f"""<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand" href="{root}index.html">
            {logo_mark()}
            <span class="brand-text">
              <strong>SMAC</strong>
              <span>Scottsdale Martial Arts Center</span>
            </span>
          </a>
          <p style="margin-top:1.1rem;">{year_line}</p>
          <div class="footer-social">
            {social_links}
          </div>
        </div>
        <div>
          <h5>Explore</h5>
          <ul>
            <li><a href="{root}index.html">Home</a></li>
            <li><a href="{root}about.html">About Us</a></li>
            <li><a href="{root}schedule.html">Schedule</a></li>
            <li><a href="{root}events.html">Upcoming Events</a></li>
            <li><a href="{root}blog.html">Blog</a></li>
            <li><a href="{MEMBER_LOGIN}" target="_blank" rel="noopener">Member Login</a></li>
          </ul>
        </div>
        <div>
          <h5>Programs</h5>
          <ul>
            {prog_links}
          </ul>
        </div>
        <div>
          <h5>Visit &amp; Contact</h5>
          <ul>
            <li><a href="{PHONE_HREF}">{PHONE}</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><span>{ADDRESS}</span></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 Scottsdale Martial Arts Center</span>
        <ul>
          <li><a href="{root}privacy.html">Privacy Policy</a></li>
          <li><a href="{root}terms.html">Terms of Service</a></li>
          <li><a href="{root}sitemap.xml">Site Map</a></li>
        </ul>
      </div>
    </div>
  </footer>"""


def page(title, description, root, active, body, body_class=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  {head(title, description, root)}
</head>
<body class="{body_class}">
  {header(root, active)}
  <main id="main">
{body}
  </main>
  {footer(root)}
  <script src="{root}assets/js/main.js"></script>
</body>
</html>
"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def para_html(text):
    return "\n        ".join(f"<p>{p}</p>" for p in text.split("\n\n") if p.strip())


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def build_home():
    root = ""
    program_cards = "\n      ".join(
        f"""<article class="program-card">
        <span class="tag">{p['tag']}</span>
        <h3>{p['name']}</h3>
        <p>{p['short']}</p>
        <a class="card-link" href="programs/{p['slug']}.html">Learn more</a>
      </article>"""
        for p in PROGRAMS
    )

    testimonial_cards = "\n      ".join(
        f'<blockquote class="quote-card"><p>{t}</p></blockquote>' for t in TESTIMONIALS
    )

    faq_items = "\n      ".join(
        f"""<details class="faq-item">
        <summary>{q}</summary>
        <p>{a}</p>
      </details>"""
        for q, a in FAQS
    )

    program_options = "\n            ".join(
        f'<option value="{p["name"]}">{p["name"]}</option>' for p in PROGRAMS
    )

    body = f"""
    <section class="hero">
      <div class="container">
        <div>
          <div class="hero-badges">
            <span class="pill">Est. 1986</span>
            <span class="pill">Wado Ryu Karate &amp; Hoteikan Jujutsu</span>
            <span class="pill">Scottsdale, AZ</span>
          </div>
          <h1>Scottsdale&rsquo;s best martial arts school</h1>
          <p class="lede">Find out why so many families in Scottsdale turn to Scottsdale Martial Arts Center for their
            training. Parents just like you have discovered how to maximize their child&rsquo;s potential and
            accelerate their development &mdash; and our members have seen improvements in as little as 7 days.</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#trial">Claim your free trial class</a>
            <a class="btn btn-ghost" href="schedule.html">View our schedule</a>
          </div>
          <p class="hero-fineprint">No pressure, no obligation &mdash; just come see the dojo for yourself.</p>
        </div>
        <div class="hero-card" id="trial">
          <span class="eyebrow">Exclusive online offer</span>
          <h3>Request more information</h3>
          <p>Tell us a bit about your family and we&rsquo;ll follow up to get you on the mat.</p>
          <form class="form-grid" id="lead-form" name="trial-request" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="bot-field">
            <input type="hidden" name="form-name" value="trial-request" />
            <p style="position:absolute; left:-9999px;" aria-hidden="true">
              <label>Leave this field blank: <input name="bot-field" tabindex="-1" autocomplete="off" /></label>
            </p>
            <div class="field">
              <label for="first_name">First name</label>
              <input id="first_name" name="first_name" type="text" required />
            </div>
            <div class="field">
              <label for="last_name">Last name</label>
              <input id="last_name" name="last_name" type="text" required />
            </div>
            <div class="field">
              <label for="email">Email address</label>
              <input id="email" name="email" type="email" required />
            </div>
            <div class="field">
              <label for="phone">Mobile number</label>
              <input id="phone" name="phone" type="tel" required />
            </div>
            <div class="field">
              <label for="program">Program</label>
              <select id="program" name="program">
                <option value="">Select a program</option>
            {program_options}
              </select>
            </div>
            <button class="btn btn-primary btn-block" type="submit">Get started</button>
            <p class="form-status" role="status"></p>
          </form>
          <p class="form-note">By opting in, you agree to receive periodic messages from Scottsdale Martial Arts
            Center. See our <a href="privacy.html">Privacy Policy</a>.</p>
        </div>
      </div>
    </section>

    <section class="section" id="about">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">Programs</span>
            <h2>A program for every age, from preschool to black belt</h2>
          </div>
          <p>Seven programs, one dojo &mdash; every student trains under the same instructors, on the same mats, toward
            the same belt system.</p>
        </div>
        <div class="grid grid-cols-4">
          {program_cards}
        </div>
      </div>
    </section>

    <section class="section section--ink">
      <div class="container">
        <div class="grid grid-cols-2" style="align-items:center; gap:3rem;">
          <div>
            <span class="eyebrow">Why SMAC</span>
            <h2>Why choose Scottsdale Martial Arts Center?</h2>
            <p>Since we opened in 1986, we&rsquo;ve been dedicated to changing people&rsquo;s lives one person at a
              time through martial arts, education, and coaching. We strive to provide a safe, comfortable, and
              welcoming atmosphere for every student and family member in Scottsdale &mdash; and we take pride in
              creating an environment where individuals achieve, develop, and succeed at their own personal goals.</p>
            <p>We strongly believe martial arts can be for everyone, regardless of age, gender, or experience level.
              Our programs teach the skills to protect yourself, backed by a realistic, practical approach we
              believe can help every member achieve greatness and live their best life.</p>
            <a class="btn btn-on-ink" href="about.html">Meet our instructors</a>
          </div>
          <div class="stat-row">
            <div class="stat-block"><span class="n">1986</span><span class="label">Est. &mdash; Scottsdale&rsquo;s oldest school</span></div>
            <div class="stat-block"><span class="n">6,000</span><span class="label">sq. ft. facility, 3 training floors</span></div>
            <div class="stat-block"><span class="n">7</span><span class="label">programs, preschool through adult</span></div>
            <div class="stat-block"><span class="n">4&times;</span><span class="label">belt testing dates per year</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">In their words</span>
            <h2>What SMAC families are saying</h2>
          </div>
        </div>
        <div class="grid grid-cols-3">
          {testimonial_cards}
        </div>
      </div>
    </section>

    <section class="section section--deep">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">Questions</span>
            <h2>Frequently asked questions</h2>
          </div>
        </div>
        <div style="max-width:760px;">
          {faq_items}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>Come see the dojo for yourself</h2>
            <p>{ADDRESS} &mdash; we&rsquo;d love to show you around.</p>
          </div>
          <div style="display:flex; gap:0.9rem; flex-wrap:wrap;">
            <a class="btn btn-primary" href="#trial">Get started</a>
            <a class="btn btn-ghost" href="{PHONE_HREF}" style="color:#fff5f1; border-color:#fff5f1;">Call {PHONE}</a>
          </div>
        </div>
      </div>
    </section>
"""
    write("index.html", page(
        "Home",
        "Scottsdale Martial Arts Center (SMAC): traditional Wado Ryu karate and Hoteikan Jujutsu for preschoolers through adults in Scottsdale, AZ since 1986.",
        root, "home", body,
    ))


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

def build_about():
    root = ""

    history_items = "\n        ".join(
        f"""<div class="timeline-item">
          <span class="year">{year}</span>
          <h4>{title}</h4>
          <p>{text}</p>
        </div>"""
        for year, title, text in HISTORY
    )

    facility_items = "\n        ".join(
        f"""<div class="feature-item">
          <span class="dot"></span>
          <p><strong>{name}.</strong> {text}</p>
        </div>"""
        for name, text in FACILITY_FEATURES
    )

    def bio_card(person):
        bullets_html = ""
        if person.get("bullets"):
            items = "\n            ".join(f"<li>{b}</li>" for b in person["bullets"])
            bullets_html = f'<ul>\n            {items}\n          </ul>'
        body_html = ""
        if person.get("body"):
            body_html = f"""<details>
            <summary>Read more</summary>
            {para_html(person['body'])}
          </details>"""
        record_html = ""
        if person.get("record"):
            rows = "\n              ".join(
                f"<li><strong>{yr}</strong> &mdash; {desc}</li>" for yr, desc in person["record"]
            )
            record_html = f"""<details>
            <summary>Full competition record</summary>
            <ul style="margin-top:0.7rem;">
              {rows}
            </ul>
          </details>"""
        return f"""<article class="bio-card">
          <h4>{person['name']}</h4>
          <span class="role">{person['role']}</span>
          <p style="font-size:0.9rem;">{person['summary']}</p>
          {bullets_html}
          {body_html}
          {record_html}
        </article>"""

    ray = INSTRUCTORS[0]
    other_instructors = INSTRUCTORS[1:]
    instructor_cards = "\n      ".join(bio_card(p) for p in other_instructors)

    safe_sport_types = ["Bullying", "Harassment", "Hazing", "Emotional Misconduct", "Physical Misconduct", "Sexual Misconduct, including Child Sexual Abuse"]
    safe_sport_list = "\n            ".join(f"<li>{t}</li>" for t in safe_sport_types)

    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="index.html">Home</a> / About Us</div>
        <span class="eyebrow">Since 1986</span>
        <h1>Who we are, and why you should train here</h1>
        <p class="lede">Scottsdale&rsquo;s oldest and largest martial arts school &mdash; built one student, one belt,
          one family at a time.</p>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="grid grid-cols-2" style="gap:3rem;">
          <div>
            <p>Since our opening in 1986, we have dedicated ourselves to changing people&rsquo;s lives one person at
              a time through martial arts training, education, and coaching. We strive to provide a safe,
              comfortable, and welcoming atmosphere for all students and family members. We take pride in creating
              an environment for individuals to achieve, develop, and succeed in their personal goals.</p>
            <p>We strongly believe martial arts can be for everyone, regardless of age, gender, or experience level.
              Throughout our programs, and behind our realistic and practical approach, students learn the necessary
              skill sets to protect themselves and develop the mental and philosophical mindset to engage our
              complex world successfully.</p>
          </div>
          <div class="bio-card">
            <h4>Safe Sport certified &amp; background checked</h4>
            <span class="role">All adult staff members are background checked</span>
            <p style="font-size:0.9rem;">SafeSport is the Olympic community&rsquo;s initiative to recognize, reduce,
              and respond to misconduct in sport, covering six primary types of misconduct:</p>
            <ul>
              {safe_sport_list}
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--ink">
      <div class="container">
        <span class="eyebrow">Owner &amp; head instructor</span>
        <div class="grid grid-cols-2" style="gap:3rem; align-items:start;">
          <div>
            <h2>Ray Hughes</h2>
            <p style="color:var(--text-on-ink-muted); font-family:var(--font-mono); font-size:0.85rem; margin-bottom:1.2rem;">
              President, Arizona Wado Karate &middot; WKF Official &middot; USA Karate Technical Committee</p>
            {para_html(ray['summary'])}
            {para_html(ray['body'])}
          </div>
          <div class="bio-card" style="background:var(--paper);">
            <h4>Career highlights</h4>
            <ul>
              {"".join(f'<li><strong>{yr}</strong> &mdash; {desc}</li>' for yr, desc in ray["record"][:5])}
            </ul>
            <details>
              <summary>Full competition record</summary>
              <ul style="margin-top:0.7rem;">
                {"".join(f'<li><strong>{yr}</strong> &mdash; {desc}</li>' for yr, desc in ray["record"])}
              </ul>
            </details>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">Our team</span>
            <h2>Instructors</h2>
          </div>
          <p>Every instructor at SMAC trains and competes themselves &mdash; many for decades, several on Team USA.</p>
        </div>
        <div class="grid grid-cols-3">
          {instructor_cards}
        </div>
      </div>
    </section>

    <section class="section section--deep">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">The dojo</span>
            <h2>Our facility</h2>
          </div>
          <p>A 6,000 sq. ft. facility on the southeast corner of 91st St. and Bell Rd., designed to maximize the
            potential of each student. Three separate training floors let us keep class sizes small and skill
            levels together.</p>
        </div>
        <div class="banner-img" style="margin-bottom:2rem;">
          <img src="assets/img/facility-floor.png" alt="An open martial arts training floor with mats and bleacher seating" loading="lazy" />
        </div>
        <div class="feature-list">
          {facility_items}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">Our story</span>
            <h2>School history</h2>
          </div>
        </div>
        <div class="timeline">
          {history_items}
        </div>
      </div>
    </section>

    <section class="section section--ink">
      <div class="container">
        <div class="grid grid-cols-3" style="gap:1.6rem;">
          <div class="bio-card" style="background:var(--ink-soft); border-color:rgba(255,255,255,0.15);">
            <h4 style="color:var(--text-on-ink);">Wado International Karate Federation</h4>
            <p style="color:var(--text-on-ink-muted); font-size:0.9rem;">We teach the martial art style of Wado Ryu
              karate, and are proud members of the Wado International Karate Federation (WIKF).</p>
          </div>
          <div class="bio-card" style="background:var(--ink-soft); border-color:rgba(255,255,255,0.15);">
            <h4 style="color:var(--text-on-ink);">Hoteikan Jujutsu</h4>
            <p style="color:var(--text-on-ink-muted); font-size:0.9rem;">All grappling training is under the
              instruction of Hoteikan Jujutsu. Chief Instructor Sensei Dan Pensabene holds a 6th degree black belt
              (Rokudan) in San Do Ichi Ryu Jujutsu, assisted by senior instructors Sensei Ken Wong (5th degree) and
              Sensei Kirk Householder (4th degree).</p>
            <p style="color:var(--text-on-ink-muted); font-size:0.85rem; margin-top:0.8rem;"><strong style="color:var(--text-on-ink);">Juniors</strong> &mdash; end of all kata (forms) days<br/>
              <strong style="color:var(--text-on-ink);">Teen/Adult</strong> &mdash; 1st Tuesday &amp; 3rd Monday, 6&ndash;7 PM, and every Saturday, 10&ndash;11 AM</p>
          </div>
          <div class="bio-card" style="background:var(--ink-soft); border-color:rgba(255,255,255,0.15);">
            <h4 style="color:var(--text-on-ink);">USA Karate Arizona ASO</h4>
            <p style="color:var(--text-on-ink-muted); font-size:0.9rem;">SMAC is a member of USA Karate Arizona, a
              group of like-minded traditional martial artists sharing one vision: to give every child in Arizona
              the opportunity to learn life skills through traditional martial arts &mdash; developing at-risk
              youth, running Arizona Karate Championships, funding athletes headed to national competition, and
              training world-class referees and coaches.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>Ready to meet the team?</h2>
            <p>Come tour the dojo and try a class &mdash; we&rsquo;ll match you to the right program.</p>
          </div>
          <a class="btn btn-primary" href="index.html#trial">Get started</a>
        </div>
      </div>
    </section>
"""
    write("about.html", page(
        "About Us",
        "The story of Scottsdale Martial Arts Center: our owner Ray Hughes, our Elite instructor team, our facility, and our 1986 roots.",
        root, "about", body,
    ))


# ---------------------------------------------------------------------------
# Programs
# ---------------------------------------------------------------------------

def build_programs_index():
    root = "../"
    cards = "\n      ".join(
        f"""<article class="program-card">
        <span class="tag">{p['tag']}</span>
        <h3>{p['name']}</h3>
        <p>{p['short']}</p>
        <a class="card-link" href="{p['slug']}.html">Learn more</a>
      </article>"""
        for p in PROGRAMS
    )
    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="{root}index.html">Home</a> / Programs</div>
        <span class="eyebrow">Every age, one dojo</span>
        <h1>Our programs</h1>
        <p class="lede">From preschool to black belt, every SMAC program trains under the same instructors, in the
          same building, toward the same belt system.</p>
      </div>
    </div>
    <section class="section">
      <div class="container">
        <div class="grid grid-cols-4">
          {cards}
        </div>
      </div>
    </section>
"""
    write("programs/index.html", page(
        "Programs",
        "Preschool, kids, teen, and adult martial arts, plus Teen and Adult Jujutsu and traditional weapons training at Scottsdale Martial Arts Center.",
        root, "programs", body,
    ))


def build_program_page(p, all_programs):
    root = "../"
    bullets = "\n          ".join(f"<li>{b}</li>" for b in p["bullets"])
    others = [x for x in all_programs if x["slug"] != p["slug"]]
    other_cards = "\n      ".join(
        f"""<article class="program-card">
        <span class="tag">{o['tag']}</span>
        <h3>{o['name']}</h3>
        <p>{o['short']}</p>
        <a class="card-link" href="{o['slug']}.html">Learn more</a>
      </article>"""
        for o in others[:3]
    )
    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="{root}index.html">Home</a> / <a href="index.html">Programs</a> / {p['name']}</div>
        <span class="eyebrow">{p['tag']} &middot; in Scottsdale</span>
        <h1>{p['name']}</h1>
        <p class="lede">{p['long']}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{root}index.html#trial">Try a free class</a>
          <a class="btn btn-ghost" href="{root}schedule.html">See class times</a>
        </div>
      </div>
    </div>

    <section class="section--tight">
      <div class="container">
        <div class="banner-img">
          <img src="{root}assets/img/{p['banner']}" alt="{p['banner_alt']}" loading="lazy" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="grid grid-cols-2" style="gap:3rem; align-items:start;">
          <div>
            <span class="eyebrow">What you&rsquo;ll gain</span>
            <h2>What this program builds</h2>
            <ul class="feature-list" style="list-style:none; padding:0;">
              {"".join(f'<div class="feature-item"><span class="dot"></span><p>{b}</p></div>' for b in p["bullets"])}
            </ul>
          </div>
          <div class="bio-card">
            <h4>Ready to visit?</h4>
            <p style="font-size:0.9rem;">Space in our training area is limited by class size, so we keep an
              exclusive online-only trial offer for new students. Fill out the form or give us a call &mdash;
              we&rsquo;d love to tell you more about the {p['name']} program.</p>
            <a class="btn btn-primary btn-block" href="{root}index.html#trial">Claim your trial class</a>
            <a class="btn btn-ghost btn-block" style="margin-top:0.7rem;" href="{PHONE_HREF}">Call {PHONE}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--deep">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">Keep exploring</span>
            <h2>Other SMAC programs</h2>
          </div>
          <a class="btn btn-ghost btn-sm" href="index.html">View all programs</a>
        </div>
        <div class="grid grid-cols-3">
          {other_cards}
        </div>
      </div>
    </section>
"""
    write(f"programs/{p['slug']}.html", page(
        p["name"],
        p["short"],
        root, "programs", body,
    ))


# ---------------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------------

def build_schedule():
    root = ""
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    rows = []
    max_slots = max(len(v) for v in WEEKLY_SCHEDULE.values())
    for day in days_order:
        slots = WEEKLY_SCHEDULE[day]
        cells = []
        for lvl, time in slots:
            cells.append(f'<span class="class-slot"><span class="lvl">{lvl}</span><span class="time">{time}</span></span>')
        if not slots:
            cells.append('<span class="class-slot is-empty">Closed</span>')
        rows.append(f'<tr><td class="day-cell">{day}</td><td>{"".join(cells)}</td></tr>')
    schedule_rows = "\n          ".join(rows)

    testing_blocks = "\n        ".join(
        f"""<div class="bio-card">
          <h4>{month}</h4>
          <ul>
            {"".join(f'<li><strong>{lvl}:</strong> {when}</li>' for lvl, when in dates)}
          </ul>
        </div>"""
        for month, dates in TESTING_DATES
    )

    curriculum_items = "\n      ".join(
        f"""<details class="curriculum-item">
        <summary>{name} testing curriculum</summary>
        <div class="curriculum-body">
          <ul>
            {"".join(f"<li>{line}</li>" for line in lines)}
          </ul>
        </div>
      </details>"""
        for name, lines in TESTING_CURRICULUM
    )

    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="index.html">Home</a> / Schedule</div>
        <span class="eyebrow">There&rsquo;s something for the entire family</span>
        <h1>Our class schedule</h1>
        <p class="lede">Seven days a week of Wado Ryu karate, Jujutsu, and weapons training &mdash; grouped by belt
          level so every student trains alongside their peers.</p>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="schedule-wrap">
          <table class="schedule">
            <thead>
              <tr><th>Day</th><th>Classes</th></tr>
            </thead>
            <tbody>
              {schedule_rows}
            </tbody>
          </table>
        </div>
        <p style="margin-top:1.2rem; font-size:0.85rem;">Times occasionally shift for holidays, testing, and special
          events &mdash; see <a href="events.html">Upcoming Events</a> or call {PHONE} to confirm.</p>
      </div>
    </section>

    <section class="section section--deep">
      <div class="container">
        <div class="grid grid-cols-2" style="gap:2.5rem; align-items:center; margin-bottom:2.5rem;">
          <div class="figure-img" style="aspect-ratio:4/3;">
            <img src="assets/img/belt-knot.png" alt="Close-up of hands tying a black belt" loading="lazy" />
          </div>
          <div>
            <span class="eyebrow">Belt testing</span>
            <h2>2026 testing schedule</h2>
            <p>Testing runs four times a year. June, September, and December dates may change &mdash; confirm with
              your instructor.</p>
          </div>
        </div>
        <div class="grid grid-cols-4">
          {testing_blocks}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">Prepare</span>
            <h2>Testing curriculum</h2>
          </div>
        </div>
        <div style="max-width:760px;">
          {curriculum_items}
        </div>
      </div>
    </section>
"""
    write("schedule.html", page(
        "Class Schedule",
        "The full weekly class schedule at Scottsdale Martial Arts Center, plus 2026 belt testing dates and testing curriculum.",
        root, "schedule", body,
    ))


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def build_events():
    root = ""
    month_order = []
    grouped = {}
    for month, day, title, note in EVENTS_2026:
        grouped.setdefault(month, []).append((day, title, note))
        if month not in month_order:
            month_order.append(month)

    sections = []
    for month in month_order:
        cards = "\n        ".join(
            f"""<div class="event-card">
          <div class="event-date"><span class="m">{month[:3].upper()}</span><span class="d">{day}</span></div>
          <div class="event-body">
            <h4>{title}</h4>
            {f'<p>{note}</p>' if note else ''}
          </div>
        </div>"""
            for day, title, note in grouped[month]
        )
        sections.append(f'<h3 class="month-heading">{month}</h3>\n      <div class="grid grid-cols-2">{cards}</div>')

    events_html = "\n      ".join(sections)

    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="index.html">Home</a> / Upcoming Events</div>
        <span class="eyebrow">2026 calendar</span>
        <h1>Upcoming events</h1>
        <p class="lede">Parents nights out, summer camp weeks, and family celebrations &mdash; all part of the SMAC
          community calendar.</p>
      </div>
    </div>
    <section class="section">
      <div class="container">
        {events_html}
      </div>
    </section>
    <section class="section section--deep">
      <div class="container">
        <div class="cta-band" style="background:var(--ink); color:var(--text-on-ink);">
          <div>
            <h2 style="color:var(--text-on-ink);">Don&rsquo;t miss an event</h2>
            <p style="color:var(--text-on-ink-muted);">Follow us on Facebook and Instagram for reminders and event photos.</p>
          </div>
          <div style="display:flex; gap:0.9rem; flex-wrap:wrap;">
            <a class="btn btn-on-ink" href="{SOCIALS['Facebook']}" target="_blank" rel="noopener">Facebook</a>
            <a class="btn btn-ghost" style="color:var(--text-on-ink); border-color:var(--text-on-ink);" href="{SOCIALS['Instagram']}" target="_blank" rel="noopener">Instagram</a>
          </div>
        </div>
      </div>
    </section>
"""
    write("events.html", page(
        "Upcoming Events",
        "See what's coming up at Scottsdale Martial Arts Center: Parents Night Out, Summer Camp, Halloween Party, and more.",
        root, "events", body,
    ))


# ---------------------------------------------------------------------------
# Blog / Client Info & Media / Privacy / Terms
# ---------------------------------------------------------------------------

MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def format_date(iso_date):
    y, m, d = iso_date.split("-")
    return f"{MONTH_NAMES[int(m) - 1]} {int(d)}, {y}"


def markdown_lite_to_html(text):
    """Turns '## Heading' lines and blank-line-separated paragraphs into HTML."""
    blocks = []
    for chunk in text.strip().split("\n\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.split("\n")
        if lines[0].startswith("## "):
            blocks.append(f"<h2>{lines[0][3:].strip()}</h2>")
            rest = "\n".join(lines[1:]).strip()
            if rest:
                blocks.append(f"<p>{rest}</p>")
        else:
            blocks.append(f"<p>{chunk}</p>")
    return "\n        ".join(blocks)


def build_blog():
    root = ""
    posts_sorted = sorted(BLOG_POSTS, key=lambda p: p["date"], reverse=True)
    cards = "\n      ".join(
        f"""<a class="blog-card" href="blog/{p['slug']}.html">
        <div class="blog-card-img"><img src="assets/img/{p['banner']}" alt="{p['banner_alt']}" loading="lazy" /></div>
        <div class="blog-card-body">
          <span class="blog-meta">{format_date(p['date'])} &middot; {p['tag']}</span>
          <h3>{p['title']}</h3>
          <p>{p['excerpt']}</p>
          <span class="card-link">Read the post</span>
        </div>
      </a>"""
        for p in posts_sorted
    )
    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="index.html">Home</a> / Blog</div>
        <span class="eyebrow">From the dojo</span>
        <h1>Blog</h1>
        <p class="lede">Notes on training, testing, and what to expect at SMAC &mdash; written by our team. For
          in-the-moment class photos and tournament results, follow us on
          <a href="{SOCIALS['Facebook']}" target="_blank" rel="noopener">Facebook</a> and
          <a href="{SOCIALS['Instagram']}" target="_blank" rel="noopener">Instagram</a>.</p>
      </div>
    </div>
    <section class="section">
      <div class="container">
        <div class="grid grid-cols-3">
          {cards}
        </div>
      </div>
    </section>
"""
    write("blog.html", page(
        "Blog",
        "News, tournament results, and updates from Scottsdale Martial Arts Center.",
        root, "blog", body,
    ))


def build_blog_post(post, all_posts):
    root = "../"
    others = [p for p in all_posts if p["slug"] != post["slug"]][:3]
    other_cards = "\n      ".join(
        f"""<a class="blog-card" href="{o['slug']}.html">
        <div class="blog-card-img"><img src="{root}assets/img/{o['banner']}" alt="{o['banner_alt']}" loading="lazy" /></div>
        <div class="blog-card-body">
          <span class="blog-meta">{format_date(o['date'])} &middot; {o['tag']}</span>
          <h3>{o['title']}</h3>
          <p>{o['excerpt']}</p>
          <span class="card-link">Read the post</span>
        </div>
      </a>"""
        for o in others
    )
    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="{root}index.html">Home</a> / <a href="{root}blog.html">Blog</a> / {post['title']}</div>
        <span class="eyebrow">{format_date(post['date'])} &middot; {post['tag']}</span>
        <h1>{post['title']}</h1>
        <p class="lede">{post['excerpt']}</p>
      </div>
    </div>
    <section class="section--tight">
      <div class="container">
        <div class="banner-img">
          <img src="{root}assets/img/{post['banner']}" alt="{post['banner_alt']}" loading="lazy" />
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="article-body">
          {markdown_lite_to_html(post['body'])}
        </div>
      </div>
    </section>
    <section class="section section--deep">
      <div class="container">
        <div class="head-row">
          <div>
            <span class="eyebrow">Keep reading</span>
            <h2>More from the blog</h2>
          </div>
          <a class="btn btn-ghost btn-sm" href="{root}blog.html">All posts</a>
        </div>
        <div class="grid grid-cols-3">
          {other_cards}
        </div>
      </div>
    </section>
"""
    write(f"blog/{post['slug']}.html", page(
        post["title"],
        post["excerpt"],
        root, "blog", body,
    ))


def build_client_media():
    root = ""
    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="index.html">Home</a> / Client Info &amp; Media</div>
        <span class="eyebrow">Current students &amp; families</span>
        <h1>Client info &amp; media</h1>
        <p class="lede">Looking for a waiver, photo/video release, uniform order form, or tournament packet? Our
          front desk keeps the current version of every client document on hand.</p>
      </div>
    </div>
    <section class="section">
      <div class="container">
        <div class="grid grid-cols-3">
          <div class="bio-card">
            <h4>Forms &amp; waivers</h4>
            <p style="font-size:0.9rem;">Membership agreements, medical/liability waivers, and photo &amp; video
              release forms are available at the front desk or by request.</p>
          </div>
          <div class="bio-card">
            <h4>Member portal</h4>
            <p style="font-size:0.9rem;">Manage your account, billing, and attendance through our member portal.</p>
            <a class="btn btn-ghost btn-block" href="{MEMBER_LOGIN}" target="_blank" rel="noopener">Member login</a>
          </div>
          <div class="bio-card">
            <h4>Photos &amp; video</h4>
            <p style="font-size:0.9rem;">Class and tournament photos are shared on our Facebook and Instagram.
              Need a specific tournament album or a copy of your student&rsquo;s testing video? Email us.</p>
            <a class="btn btn-ghost btn-block" href="mailto:{EMAIL}">Email the front desk</a>
          </div>
        </div>
      </div>
    </section>
"""
    write("client-info-media.html", page(
        "Client Info & Media",
        "Forms, waivers, media releases, and the member portal for current SMAC students and families.",
        root, "client", body,
    ))


def build_legal_stub(slug, title, active, intro):
    root = ""
    body = f"""
    <div class="page-header">
      <div class="container">
        <div class="breadcrumb"><a href="index.html">Home</a> / {title}</div>
        <h1>{title}</h1>
      </div>
    </div>
    <section class="section">
      <div class="container" style="max-width:760px;">
        <p>{intro}</p>
        <p>This page is a placeholder while our full {title.lower()} is finalized. For questions about your data,
          your membership agreement, or anything else, contact us directly:</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="{PHONE_HREF}">{PHONE}</a></p>
      </div>
    </section>
"""
    write(f"{slug}.html", page(title, f"{title} for Scottsdale Martial Arts Center.", root, active, body))


# ---------------------------------------------------------------------------
# Favicon + sitemap
# ---------------------------------------------------------------------------

def build_favicon():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
  <circle cx="20" cy="20" r="19" fill="#faf6ec" stroke="#a3271e" stroke-width="2"/>
  <path d="M11 24.5C11 24.5 15 15 20 15C25 15 29 24.5 29 24.5" stroke="#17150f" stroke-width="2.2" stroke-linecap="round" fill="none"/>
  <path d="M14 24.5H26" stroke="#a3271e" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="20" cy="10.5" r="1.9" fill="#a3271e"/>
</svg>"""
    write("assets/img/favicon.svg", svg)


def build_thanks():
    root = ""
    body = f"""
    <section class="section" style="min-height:50vh; display:flex; align-items:center;">
      <div class="container center">
        <span class="eyebrow" style="justify-content:center;">Thank you</span>
        <h1>We’ve got your message</h1>
        <p class="lede mx-auto">A member of the SMAC team will reach out soon. In the meantime, feel free to browse
          our <a href="programs/">programs</a> or check the <a href="schedule.html">class schedule</a>.</p>
        <a class="btn btn-primary" href="index.html">Back to home</a>
      </div>
    </section>
"""
    write("thanks.html", page(
        "Thank You",
        "Thanks for reaching out to Scottsdale Martial Arts Center — we'll be in touch soon.",
        root, "", body,
    ))


def build_sitemap():
    pages = ["", "about.html", "schedule.html", "events.html", "blog.html", "client-info-media.html", "privacy.html", "terms.html"]
    urls = "\n  ".join(f"<url><loc>https://www.smacus.com/{p}</loc></url>" for p in pages)
    prog_urls = "\n  ".join(f"<url><loc>https://www.smacus.com/programs/{p['slug']}.html</loc></url>" for p in PROGRAMS)
    blog_urls = "\n  ".join(f"<url><loc>https://www.smacus.com/blog/{p['slug']}.html</loc></url>" for p in BLOG_POSTS)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {urls}
  {prog_urls}
  {blog_urls}
</urlset>
"""
    write("sitemap.xml", xml)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    build_home()
    build_about()
    build_programs_index()
    for p in PROGRAMS:
        build_program_page(p, PROGRAMS)
    build_schedule()
    build_events()
    build_blog()
    for post in BLOG_POSTS:
        build_blog_post(post, BLOG_POSTS)
    build_client_media()
    build_legal_stub("privacy", "Privacy Policy", "privacy", "Scottsdale Martial Arts Center respects your privacy. We collect only the information needed to run our programs, communicate with members, and process billing, and we never sell your information to third parties.")
    build_legal_stub("terms", "Terms of Service", "terms", "By enrolling at or using services from Scottsdale Martial Arts Center, you agree to our membership terms, class policies, and code of conduct.")
    build_favicon()
    build_thanks()
    build_sitemap()


if __name__ == "__main__":
    main()
