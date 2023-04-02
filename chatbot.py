import telegram
import json
import tarotgpt
import random
import time
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

## Tarot card informations
tarot_topic = ["연애", "인간관계", "직업", "재물", "건강", "성장", "영성", "가족"]
deck =[
    {"name": "The Fool", "url": "the_fool",
         "desc": "Freedom from conventions and norms. Something or someone unique and exceptional. Options kept open. Giving up control, spontaneity. Uncertainty, attention to the here and now. Going on a trip.",
         "message": "keep on the move",
         "rdesc": "Difficulty in choosing and committing oneself to something stable. Restlessness. Lack of purpose. Getting lost. Foolish behavior. Eccentricity, lack of acceptance by the social environment. Difficulty in planning ahead.",
         "sequence": 0,
         "cardtype": "major"},

        {"name": "The Magician", "url": "the_magician",
         "desc": "The start of something. Beginner’s luck. Having various tools and means at our disposal. Use of supernatural forces. Creating reality with mind power. Training and acquisition of practical skills. Improvisation. Display or show for other people.",
         "message": "create a new reality",
         "rdesc": "Trickery, sleight of hand, cheating. Showing off, pretending. Lack of self-awareness about body, sexuality, or basic motives. Near miss due to inexperience or inaccuracy.",
         "sequence": 1,
         "cardtype": "major"},

        {"name": "The Popess", "url": "the_popess",
         "desc": "Wisdom combining intellect and intuition. A spiritual mother. A woman hiding her strengths in a world of men. Modesty. Secrets, something hidden, mystery. Getting a hint of something which remains largely unknown. Impossible to give a definite answer now.",
         "message": "know how to set boundaries",
         "rdesc": "Need to hide our true nature behind the conventions of normal society. Conservative approach to sex and the body. Emotional blockage.",
         "sequence": 2,
         "cardtype": "major"},

        {"name": "The Empress", "url": "the_empress",
         "desc": "Abundance, growth, productivity. Natural or human touch within an artificial framework. Emotional intelligence. Protection and care. Motherhood. A powerful female figure. Strong feminine identity.",
         "message": "act from the guts",
         "rdesc": "Impulsive behavior, someone difficult to reason with. Over-protectiveness, excessive involvement in the life of others. Problems with a strong mother figure.",
         "sequence": 3,
         "cardtype": "major"},

        {"name": "The Emperor", "url": "the_emperor",
         "desc": "Practical and material achievements. Matters relating to the workplace or source of income. Authority and control, a commanding position. A protective father figure, patron or sponsor. Assertiveness. Military affairs.",
         "message": "show leadership and responsibility",
         "rdesc": "Belligerence, violence, trying to solve things by brute force. Dictatorship. Possibility of sexual abuse. Difficulty in coping with a dominant father figure. Denial and hiding of inner weaknesses.",
         "sequence": 4,
         "cardtype": "major"},

        {"name": "The Pope", "url": "the_pope",
         "desc": "Teacher, instructor, or counselor. Education and knowledge, academic expertise. Organized religion, conventional medicine or psychology. Spiritual father. Consultation or treatment by a specialist. Marriage.",
         "message": "respect knowledge and education",
         "rdesc": "Excessive adhesion to conventions and outdated norms. Bureaucracy, an oppressive establishment. Hypocrisy, discrimination. Divorce.",
         "sequence": 5,
         "cardtype": "major"},

        {"name": "The Lover", "url": "the_lover",
         "desc": "Love, amorous relationship. Emotional entanglement. Need to make a choice, or to disengage oneself from past influences. Inclinations of the heart correspond to the will of heaven. Small steps actually taken are the visible signs of inner desire.",
         "message": "follow the path of the heart.",
         "rdesc": "Complex relationship between several people, e.g., a romantic triangle or a tension between mother and wife. Hesitation, quandary. Confusion as to one’s own feeling and will.",
         "sequence": 6,
         "cardtype": "major"},

        {"name": "The Chariot", "url": "the_chariot",
         "desc": "Victory or an achievement putting the querent in a strong and protected position. Ambition, energy, motivation to move forward. Public honor. Power and high status.",
         "message": "dare and win",
         "rdesc": "Inner weakness hidden behind external show-off. Arrogance, vanity. Over-protectiveness, emotional closure. Confusion about one’s goals. Losing the simple touch with people and reality.",
         "sequence": 7,
         "cardtype": "major"},

        {"name": "Justice", "url": "justice",
         "desc": "Law and order, legal and court issues. A fair and balanced judgment. A developed conscience. Rationality, reasoning by clear rules and common norms. Touch of grace and humanity beyond the objective considerations.",
         "message": "act with reason and by the accepted norms",
         "rdesc": "Petty accountability, a critical and judgmental attitude, guilt feelings. Repressive control of self and of others. Negative ideas blocking change and advance.",
         "sequence": 8,
         "cardtype": "major"},

        {"name": "The Hermit", "url": "the_hermit",
         "rdesc": "A closed and reclusive attitude. Isolation, loneliness. Fixed ideas. Excessive caution and suspicion, a critical approach looking for defects. Hidden and denied desires.",
         "message": "look for the essence of things",
         "desc": "A quest for truth or for spiritual understanding. Concentrating on a clear purpose. Caution, careful examination. Self-privation for the sake of a meaningful cause. Loyalty to principles, strong faith.",
         "sequence": 9,
         "cardtype": "major"},

        {"name": "Wheel of Fortune", "url": "the_wheel_of_fortune",
         "desc": "Change in circumstances and position. A rise after a fall. Gambling, putting faith in capricious luck. Life cycles, closure of circles. Adapting to the routine of everyday life. A hint to previous incarnations.",
         "message": "accept life’s ups and downs",
         "rdesc": "A decline after a period of rising. Danger lurks at the summit. Moving in a closed circle. Capricious mood changes. Feeling powerless to affect one’s situation.",
         "sequence": 10,
         "cardtype": "major"},

        {"name": "Strength", "url": "strength",
         "desc": "Power and courage to face challenges. Controlled expression of creative urges, drives and desires. Mobilization of inner resources towards a common goal. Taking risks.",
         "message": "take control of yourself",
         "rdesc": "The need to keep things under control leads to constant tensions. A risk of losing one’s grip. Internal conflicts and unrealistic assessment of one’s own forces may lead to failure.",
         "sequence": 11,
         "cardtype": "major"},

        {"name": "The Hanged Man", "url": "the_hanged_man",
         "desc": "Seeing things from a unique point of view. Enduring difficulties for a worthy cause. A period of deep self examination. Passivity, acceptance of reality even if it is the opposite of what one expects.",
         "message": "look at things from the opposite perspective",
         "rdesc": "Isolation. Emotional stance of a victim. Inability to act. Denying one’s own unique qualities, striving to be “normal” at all costs. Living in one’s private and imaginary reality.",
         "sequence": 12,
         "cardtype": "major"},

        {"name": "Death", "url": "death",
         "desc": "The end of something whose time has come. Cutting off past influences or attachment to dominant figures. Giving up the superfluous and keeping only the essential. Disintegration of the old makes room for the new.",
         "message": "give up what is over",
         "rdesc": "Difficulty in coping with loss or change. Temporary difficulties, a trying challenge. Disintegration. Realisation of a painful truth. Does not predict future death, but may reflect anxiety about dying or mourning over a loss which has already happened.",
         "sequence": 13,
         "cardtype": "major"},

        {"name": "Temperance", "url": "temperance",
         "desc": "Reconciliation, compromise, relaxation of tensions. Integration of opposites. Ability to do the seemingly impossible. A slow process of distillation and improvement. Patience, perseverance. Self-improvement.",
         "message": "find the golden mean",
         "rdesc": "Going back and forth without making real progress. Losing patience with a lengthy process. Emotion-al preoccupation with oneself, pushing away others who might come to help.",
         "sequence": 14,
         "cardtype": "major"},

        {"name": "The Devil", "url": "the_devil",
         "desc": "A burst of creativity. Paradoxes and contradictions. Irony and mocking of common norms. Acting from desires, passions and impulses. Moving on from a past family trauma.",
         "message": "express passion and desire.",
         "rdesc": "Temptation, attraction to the dark and forbidden. Exploitation, egotism, domination. Compulsive self-gratification. Senseless behavior has its price. Difficulty in detaching oneself from an unhealthy bond.",
         "sequence": 15,
         "cardtype": "major"},

        {"name": "The Tower", "url": "the_tower",
         "desc": "Breaking up of solid structures. Getting free from confinement. Sudden breakthrough after long preparations. Sparkling sexual encounter. Success lies in simplicity and modesty.",
         "message": "return to the solid ground of reality",
         "rdesc": "Shock, collapse of projects or trusted structures. A fall from an apparently solid and secure position. Chaos, confusion, difficulty in understanding what is going on. Vanity and pride lead to failure.",
         "sequence": 16,
         "cardtype": "major"},

        {"name": "The Star", "url": "the_star",
         "desc": "Openness, simplicity, return to nature. Purity, honesty. Showing yourself “as you are,” accepting one’s body and desires. Generosity. Luck from heaven. Intuitive feeling of guidance or energy coming from a higher plane.",
         "message": "flow from a pure source",
         "rdesc": "Naive optimism and wishful-thinking. Exposing oneself to danger or abuse. Difficulty in setting proper boundaries. Squandering, wastefulness.",
         "sequence": 17,
         "cardtype": "major"},

        {"name": "The Moon", "url": "the_moon",
         "desc": "Deep emotions, perhaps related to a mother or feminine figure. A different experience of reality. Longing for the unreachable. Finding one’s hidden strengths. Occupation with the remote past. A hidden treasure.",
         "message": "don’t be afraid to go deep down",
         "rdesc": "Vague and disturbing feelings. Emotional difficulties, a period of depression. Danger lurking under the surface. Retreat, the road ahead is hard to find.",
         "sequence": 18,
         "cardtype": "major"},

        {"name": "The Sun", "url": "the_sun",
         "desc": "Light and warmth, abundance, blessings. Pleasant feeling, emotional or physical healing. Partnership, trust, sharing, brotherhood. Human touch. An ideal father figure. Matters relating to children. Setting limits in a moderate and non-oppressive way.",
         "message": "find suitable partners",
         "rdesc": "Living in a limited space, difficulty to face reality “in the open.” Immaturity, dependence on others. Someone or something too intense and energetic to feel comfortable with. An absent father.",
         "sequence": 19,
         "cardtype": "major"},

        {"name": "Judgement", "url": "judgement",
         "desc": "Revelation, enlightenment, a new understanding. A turning point in a therapy process. Healing of a family relationship. Disclosure, secrets revealed, publicity. Birth of a baby or of a new thing.",
         "message": "awaken to spiritual reality",
         "rdesc": "Revelation of something that should have been kept hidden. Lack of privacy. Unpleasant realization. Problems related to child-parent relations. Too much noise and drama.",
         "sequence": 20,
         "cardtype": "major"},

        {"name": "The World", "url": "the_world",
         "desc": "Completion of a process. Balanced activity and achievements in various domains. Contact with far places. Harmony and correspondence between different planes. Pregnancy, something new is about to be born. The Dance of Life.",
         "message": "everything is perfect as it is",
         "rdesc": "Life in a bubble, difficulty in sharing your world with others. Disconnection of inner feelings from external life. Preoccupation with oneself, idealized self-image, inability to move forward.",
         "sequence": 21,
         "cardtype": "major"},

        {"name": "Ace of Coins", "url": "ace_of_coins",
         "desc": "A good start in material things. Financial and physical stability. A practical perspective. A significant sum of money. Utilitarian approach. Greed. Something basic and unsophisticated.",
         "rdesc": "(similar to upright) A good start in material things. Financial and physical stability. A practical perspective. A significant sum of money. Utilitarian approach. Greed. Something basic and unsophisticated.",
         "sequence": 22,
         "cardtype": "ace"},

        {"name": "Two of Coins", "url": "two_of_coins",
         "desc": "Duality. Two options or two elements. Collaborating while keeping distance. A winding road, advancing in complex ways. Recognition and acknowledgment.",
         "rdesc": "(similar to upright) Duality. Two options or two elements. Collaborating while keeping distance. A winding road, advancing in complex ways. Recognition and acknowledgment.",
         "sequence": 23,
         "cardtype": "minor"},

        {"name": "Three of Coins", "url": "three_of_coins",
         "desc": "Product. A partnership or an alliance bears fruit. First results of a project. Good prospects.",
         "rdesc": "Disappointment, a partnership or a project does not bear the expected fruits.",
         "sequence": 24,
         "cardtype": "minor"},

        {"name": "Four of Coins", "url": "four_of_coins",
         "desc": "Stability. Solid material assets. Tradition, reputation and honor. Time-tested reliability. Established social institutions.",
         "rdesc": "Conservatism, clinging to old and outdated patterns.",
         "sequence": 25,
         "cardtype": "minor"},

        {"name": "Five of Coins", "url": "five_of_coins",
         "desc": "Disruption. Something new appears and destabilizes existing structures. A new element gets attention, but also awakens resistance.",
         "rdesc": "(similar to upright) Disruption. Something new appears and destabilizes existing structures. A new element gets atten-tion, but also awakens resistance.",
         "sequence": 26,
         "cardtype": "minor"},

        {"name": "Six of Coins", "url": "six_of_coins",
         "desc": "Expansion. Abundance of resources and possible ways to advance. A positive outlook, success. A good balance between stability and movement.",
         "rdesc": "(similar to upright) Expansion. Abundance of resources and possible ways to advance. A positive outlook, success. A good balance between stability and movement.",
         "sequence": 27,
         "cardtype": "minor"},

        {"name": "Seven of Coins", "url": "seven_of_coins",
         "desc": "Acceptance. Something new is well received. Help and protection. Integrating into a system without losing one’s individuality.",
         "rdesc": "Lack of independence, need to rely on help and acceptance from others.",
         "sequence": 28,
         "cardtype": "minor"},

        {"name": "Eight of Coins", "url": "eight_of_coins",
         "desc": "Uniformity. A mechanical structure. Practical considerations prove efficient, but lack a human touch. Routine work. A slow and patient advance.",
         "rdesc": "(similar to upright) Uniformity. A mechanical structure. Practical considerations prove efficient, but lack a human touch. Routine work. A slow and patient advance.",
         "sequence": 29,
         "cardtype": "minor"},

        {"name": "Nine of Coins", "url": "nine_of_coins",
         "desc": "Motivation. Carving a niche for oneself in an existing system. Ambition. Endurance and independent thinking bear long-term fruits.",
         "rdesc": "(similar to upright) Motivation. Carving a niche for oneself in an existing system. Ambition. Endurance and independent thinking bear long-term fruits.",
         "sequence": 30,
         "cardtype": "minor"},

        {"name": "Ten of Coins", "url": "ten_of_coins",
         "desc": "Abundance. Intensive activity in practical affairs. Material success and achievements. Some may be getting more than others.",
         "rdesc": "(similar to upright) Abundance. Intensive activity in practical affairs. Material success and achievements. Some may be getting more than others.",
         "sequence": 31,
         "cardtype": "minor"},

        {"name": "Page of Coins", "url": "page_of_coins",
         "desc": "A practical endeavor. Untapped potentials are within reach. Tangible success at the beginning. A solid material base for further advancement.",
         "rdesc": "Hesitation, lack of clear purpose. Thinking in terms of past achievements misses present opportunities.",
         "sequence": 32,
         "cardtype": "court"},

        {"name": "Knight of Coins", "url": "knight_of_coins",
         "desc": "Advancement in a practical direction. A productive expression of creativity. A clear goal in sight.",
         "rdesc": "Constant pursuit of money, without reaching material stability. Passions and desires may interfere with practical plans.",
         "sequence": 33,
         "cardtype": "court"},

        {"name": "Queen of Coins", "url": "queen_of_coins",
         "desc": "Tangible assets, material and personal stability, a sober and realistic vision. Looking at things from a practical and pragmatic perspective.",
         "rdesc": "Conservatism, resistance to change, aiming only to preserve the existing assets. Looking at things only from the material perspective.",
         "sequence": 34,
         "cardtype": "court"},

        {"name": "King of Coins", "url": "king_of_coins",
         "desc": "Confidence and security, a cautious but optimistic vision. Looking for new achievements while holding existing assets secure.",
         "rdesc": "Dissatisfaction with what one already has. Disregard of the good things in the present situation. A limited outlook.",
         "sequence": 35,
         "cardtype": "court"},

        {"name": "Ace of Clubs", "url": "ace_of_clubs",
         "desc": "Creative momentum. Active sexuality. Strong impulses, energy and drive. Life force. Beginning of growth. Dispersing one’s efforts in different directions.",
         "rdesc": "Lack of energy, restriction, repressed sexuality, a creative block.",
         "sequence": 36,
         "cardtype": "ace"},

        {"name": "Two of Clubs", "url": "two_of_clubs",
         "desc": "Crossroads. Several options or ways to choose from. Every course offers benefits. A brief encounter with someone going his own way. Blocking an opponent’s line of advance.",
         "rdesc": "(similar to upright) Crossroads. Several options or ways to choose from. Every course offers benefits. A brief encounter with someone going his own way. Blocking an opponent’s line of advance.",
         "sequence": 37,
         "cardtype": "minor"},

        {"name": "Three of Clubs", "url": "three_of_clubs",
         "desc": "Direction. Moving forward after a moment of hesitation. Finding a middle path between two courses of action. Gaining an advantage by keeping neutrality between two conflicting sides.",
         "rdesc": "(similar to upright) Direction. Moving forward after a moment of hesitation. Finding a middle path between two courses of action. Gaining an advantage by keeping neutrality between two conflicting sides.",
         "sequence": 38,
         "cardtype": "minor"},

        {"name": "Four of Clubs", "url": "four_of_clubs",
         "desc": "Stalemate. A temporary stop in order to prepare for future advancement. Tensions at present, but good prospects in the long run. Making a move now is in nobody’s interest.",
         "rdesc": "(similar to upright) Stalemate. A temporary stop in order to prepare for future advancement. Tensions at present, but good prospects in the long run. Making a move now is in nobody’s interest.",
         "sequence": 39,
         "cardtype": "minor"},

        {"name": "Five of Clubs", "url": "five_of_clubs",
         "desc": "Overcoming. Getting over a weak opposition. Breakdown of an equilibrium. Focusing on the main objective. An initiative to make a winning move.",
         "rdesc": "With the covering part of the central wand below – walking into a complex situation, losing one’s edge.",
         "sequence": 40,
         "cardtype": "minor"},

        {"name": "Six of Clubs", "url": "six_of_clubs",
         "desc": "Collaboration. A strong alliance between two parties with different goals but common present interests. A taste for luxury made possible by favorable conditions.",
         "rdesc": "With the decorated flower at the bottom – excessive pursuit of luxury. Need to break up an alliance of opponents.",
         "sequence": 41,
         "cardtype": "minor"},

        {"name": "Seven of Clubs", "url": "seven_of_clubs",
         "desc": "Struggle. Someone putting up a fight against many opponents. Obstinacy, endurance, keeping one’s position in a conflict situation. A difficult combat with an uncertain outcome.",
         "rdesc": "(similar to upright) Struggle. Someone putting up a fight against many opponents. Obstinacy, endurance, keeping one’s position in a conflict situation. A difficult combat with an uncertain outcome.",
         "sequence": 42,
         "cardtype": "minor"},

        {"name": "Eight of Clubs", "url": "eight_of_clubs",
         "desc": "Regulation. It is possible to advance only by following the rules. Occupation with short-term goals while losing the long-term perspective. A roadblock.",
         "rdesc": "(similar to upright) Regulation. It is possible to advance only by following the rules. Occupation with short-term goals while losing the long-term perspective. A roadblock.",
         "sequence": 43,
         "cardtype": "minor"},

        {"name": "Nine of Clubs", "url": "nine_of_clubs",
         "desc": "Interruption. Difficulties and oppositions too hard to overcome. Giving up one’s projects to avoid conflict. Starting anew after a challenging period.",
         "rdesc": "(similar to upright) Interruption. Difficulties and oppositions too hard to overcome. Giving up one’s projects to avoid conflict. Starting anew after a challenging period.",
         "sequence": 44,
         "cardtype": "minor"},

        {"name": "Ten of Clubs", "url": "ten_of_clubs",
         "desc": "Loyalty. A partnership or an alliance endures hardships and succeeds in getting over them. Pure intentions and perseverance lead to success. Honoring one’s principles in spite of difficulties.",
         "rdesc": "(similar to upright) Loyalty. A partnership or an alliance endures hardships and succeeds in getting over them. Pure intentions and perseverance lead to success. Honoring one’s principles in spite of difficulties.",
         "sequence": 45,
         "cardtype": "minor"},

        {"name": "Page of Clubs", "url": "page_of_clubs",
         "desc": "A creative potential which still needs processing. Keeping a safe distance from events and waiting for the right moment.",
         "rdesc": "A task too heavy for the querent’s strength. Difficulty in controlling desires and urges. Immature approach to sexuality.",
         "sequence": 46,
         "cardtype": "court"},

        {"name": "Knight of Clubs", "url": "knight_of_clubs",
         "desc": "A change of direction, following one’s urges and passions. A temporary stop, but there is still energy and a desire to advance.",
         "rdesc": "Preoccupation with the satisfaction of one’s own desires. Problem in defining long-term goals. Submitting to temptation.",
         "sequence": 47,
         "cardtype": "court"},

        {"name": "Queen of Clubs", "url": "queen_of_clubs",
         "desc": "A feminine figure with a strong personality. Things connected with food and eating. Speaking softly while holding a big stick. A secure, well-defended position.",
         "rdesc": "Intimidation, menace. Using sexuality as a means of control. Problems with a strong mother figure. Fear of feminine power.",
         "sequence": 48,
         "cardtype": "court"},

        {"name": "King of Clubs", "url": "king_of_clubs",
         "desc": "A mature attitude to urges and desires. Controlled creativity. Prodding oneself to make a move forward. Investing present assets in future projects.",
         "rdesc": "Plans to move forward are frustrated by self-defeating acts. Hesitation, conflicts, tendency to make things too heavy and complex.",
         "sequence": 49,
         "cardtype": "court"},

        {"name": "Ace of Cups", "url": "ace_of_cups",
         "desc": "The beginning of a love relationship. Expression of warm feelings. Romantic longing for something extraordinary. Emotional and spiritual growth.",
         "rdesc": "Emotional dryness, feeling oneself empty. Avoidance of intimacy, negative feelings, heartbreak.",
         "sequence": 50,
         "cardtype": "ace"},

        {"name": "Two of Cups", "url": "two_of_cups",
         "desc": "Partnership. A romantic relationship or a close personal alliance. Interpersonal dynamics based on social norms. Passion in a love relationship, which may turn against itself.",
         "rdesc": "A crisis in a couple relationship, disappointment with someone close to you.",
         "sequence": 51,
         "cardtype": "minor"},

        {"name": "Three of Cups", "url": "three_of_cups",
         "desc": "Birth. Something new brings joy and happiness. Caring for a child. Issues of child-parent relations. A common project motivated by feelings and not only by interests.",
         "rdesc": "Problems in relations with one’s parents, or with one’s child. A strong alliance of two persons leaves a third one outside.",
         "sequence": 52,
         "cardtype": "minor"},

        {"name": "Four of Cups", "url": "four_of_cups",
         "desc": "Family. A collective of people (family, community etc.) with a history and a sense of belonging. Commitment to a group, at the price of giving up personal interests.",
         "rdesc": "Problems and discord in the family or in a long-lasting community. A fixed social structure which doesn’t allow for adaptation or flexibility.",
         "sequence": 53,
         "cardtype": "minor"},

        {"name": "Five of Cups", "url": "five_of_cups",
         "desc": "Links. Popularity, relations with many people. Becoming the center of attention in a group. Relying on connections with other people to advance oneself or to overcome difficulties.",
         "rdesc": "Excessive preoccupation with social activity. Losing oneself in multiple superficial connections. Cultivating virtual instead of real contacts.",
         "sequence": 54,
         "cardtype": "minor"},

        {"name": "Six of Cups", "url": "six_of_cups",
         "desc": "Continuity. A long-term relationship. Repetition between different generations in the family. A stable personal alliance.",
         "rdesc": "Monotony, tedious repetition. Falling time and again into the same emotional traps.",
         "sequence": 55,
         "cardtype": "minor"},

        {"name": "Seven of Cups", "url": "seven_of_cups",
         "desc": "Individuality. A single person finding his place in a group. Contact with people in high positions. Exceptional qualities are appreciated.",
         "rdesc": "Problems of integration in a group or an organization. Being part of a collective, but feeling isolated and estranged.",
         "sequence": 56,
         "cardtype": "minor"},

        {"name": "Eight of Cups", "url": "eight_of_cups",
         "desc": "Involvement. Developing personal relationships within a group. A favorable human-relations environment. A feast or a family event.",
         "rdesc": "Interference of the environment in a couple’s relationships. Pressures from one’s family in romantic or personal matters.",
         "sequence": 57,
         "cardtype": "minor"},

        {"name": "Nine of Cups", "url": "nine_of_cups",
         "desc": "Collectivity. A group or organization working harmoniously with everyone finding his proper place. Accepting one’s role in a social environment. Happiness, wishes coming true.",
         "rdesc": "A confusing social situation, difficulty in situating oneself within a complex environment.",
         "sequence": 58,
         "cardtype": "minor"},

        {"name": "Ten of Cups", "url": "ten_of_cups",
         "desc": "Leadership. A person with special qualities receives appreciation and high status. Assuming responsibility for others. Maintaining a superior position.",
         "rdesc": "A fallen leader, loss of popularity. Disappointment because of ingratitude by people one has helped.",
         "sequence": 59,
         "cardtype": "minor"},

        {"name": "Page of Cups", "url": "page_of_cups",
         "desc": "First and unsure steps in a romantic endeavor. Shyness. Sincere intentions. Trying to figure out one’s feelings.",
         "rdesc": "Over-absorption in one’s personal feelings, losing contact with others. Sloppiness in practical affairs.",
         "sequence": 60,
         "cardtype": "court"},

        {"name": "Knight of Cups", "url": "knight_of_cups",
         "desc": "A romantic gesture, offering one’s heart, courting. Openness, sincerity, a simple heart. A potential lover may appear.",
         "rdesc": "Superficial and unstable feelings. An over-optimistic but unrealistic attitude. An overt display of shallow or insincere feelings. ",
         "sequence": 61,
         "cardtype": "court"},

        {"name": "Queen of Cups", "url": "queen_of_cups",
         "desc": "A rich inner world which is kept hidden. Guarding one’s privacy or valuable assets. Strong feelings held under control.",
         "rdesc": "Closure, defensiveness. Distrust of others due to negative past experiences. Hiding one’s emotions under guise of rational criticism.",
         "sequence": 62,
         "cardtype": "court"},

        {"name": "King of Cups", "url": "king_of_cups",
         "desc": "Emotional maturity, optimism, ability to overcome past injuries and look ahead. Openness to new things, but with prudence and caution. Closing one’s ear to voices from the past.",
         "rdesc": "Difficulty in overcoming an emotional blow. A pessimistic outlook caused by negative past experiences. ",
         "sequence": 63,
         "cardtype": "court"},

        {"name": "Ace of Swords", "url": "ace_of_swords",
         "desc": "A planned initiative. Rational and logical thinking, sharpness of mind. A conclusive decision. Readi-ness to fight. Ambition, competitiveness. A victory with stable achievements.",
         "rdesc": "Negative and unproductive thoughts. Misconceptions, delusions. Self-defeat. Injury.",
         "sequence": 64,
         "cardtype": "ace"},

        {"name": "Two of Swords", "url": "two_of_swords",
         "desc": "Boundaries. Limits that protect and define something which is in development. Making full use of the present situation. Preparations for future advancement. A clear view encompassing the overall situation.",
         "rdesc": "(similar to upright) Boundaries. Limits that protect and define something which is in development. Making full use of the present situation. Preparations for future advancement. A clear view encompassing the overall situation.",
         "sequence": 65,
         "cardtype": "minor"},

        {"name": "Three of Swords", "url": "three_of_swords",
         "desc": "Victory. Overcoming a weak opposition. Cutting through a quandary and going forward in a clear direction. A third party intervenes and wins over two weakened opponents.",
         "rdesc": "A failure, defeat from a weaker opponent. An unsuccessful attempt to make a decisive move.",
         "sequence": 66,
         "cardtype": "minor"},

        {"name": "Four of Swords", "url": "four_of_swords",
         "desc": "Restriction. A limited space for development and maneuver. Trying to push against constraints. Potentials to grow once the present limitations become less solid.",
         "rdesc": "Confinement and blocking, lack of motivation or energy to break out of a limited situation.",
         "sequence": 67,
         "cardtype": "minor"},

        {"name": "Five of Swords", "url": "five_of_swords",
         "desc": "Breakthrough. A forward thrust overcoming the existing limits. Keeping up spirits in a tight situation. Doing things in one’s own way.",
         "rdesc": "A failed initiative to change the situation. Stubbornness leading nowhere. Oppressing factors cannot be removed now.",
         "sequence": 68,
         "cardtype": "minor"},

        {"name": "Six of Swords", "url": "six_of_swords",
         "desc": "Adaptation. Accepting limitations and adapting oneself to them. Respecting the present order. Com-promising in order to make the best of the existing situation.",
         "rdesc": "Resignation, surrender, giving up the ambition to change things for the better. Lack of fighting spirit.",
         "sequence": 69,
         "cardtype": "minor"},

        {"name": "Seven of Swords", "url": "seven_of_swords",
         "desc": "Sharpness. A focused and determined attitude. Concentrating on a clear goal and doing what it takes to reach it. Winning a fight with the odds evenly balanced.",
         "rdesc": "A narrow and over-concentrated vision. Investing one’s efforts and resources in a lost cause.",
         "sequence": 70,
         "cardtype": "minor"},

        {"name": "Eight of Swords", "url": "eight_of_swords",
         "desc": "Defenses. Putting up shields and blocks. Psychological defense mechanisms. A need to be in total control. A well-guarded treasure. Entering another’s domain with permission.",
         "rdesc": "(similar to upright) Defenses. Putting up shields and blocks. Psychological defense mechanisms. A need to be in total control. A well-guarded treasure. Entering another’s domain with permission.",
         "sequence": 71,
         "cardtype": "minor"},

        {"name": "Nine of Swords", "url": "nine_of_swords",
         "desc": "Courage. Winning a fight against a superior force. Pure intentions. Putting imperfect means to good use.",
         "rdesc": "Losing against a stronger opponent. Sloppiness, imperfect preparations for a challenge.",
         "sequence": 72,
         "cardtype": "minor"},

        {"name": "Ten of Swords", "url": "ten_of_swords",
         "desc": "Exhaustion. A complex situation with many conflicting interests. A long battle without a clear out-come. Need to find an ally who will attack the problem from a different direction.",
         "rdesc": "Immobility. Impossible to move now. Feeling attacked from different sides. A painful and humiliating defeat.",
         "sequence": 73,
         "cardtype": "minor"},

        {"name": "Page of Swords", "url": "page_of_swords",
         "desc": "Preparation for a future challenge. Looking for a compromise between reason and strong desires. Hesitating to use one’s power.",
         "rdesc": "Confusion, negative and inhibiting thoughts, self-defeat. Sloppy use of one’s own tools may cause damage.",
         "sequence": 74,
         "cardtype": "court"},

        {"name": "Knight of Swords", "url": "knight_of_swords",
         "desc": "Energy and resources to advance, still looking for the right direction. Hovering above practical constraints. Determination and perseverance.",
         "rdesc": "Trying to force one’s misguided views, insisting on a wrong direction. Losing touch with the ground.",
         "sequence": 75,
         "cardtype": "court"},

        {"name": "Queen of Swords", "url": "queen_of_swords",
         "desc": "A secure and protected position. Defending one’s territory. Preparation of something that shouldn’t be exposed yet.",
         "rdesc": "Defensiveness and rigidity. Suspicion and fixed ideas block advancement and preclude new connections.",
         "sequence": 76,
         "cardtype": "court"},

        {"name": "King of Swords", "url": "king_of_swords",
         "desc": "A determination to break from the past, a strong will. Feeling equipped to deal with uncertainty. Wisdom and intellectual maturity.",
         "rdesc": "A divided heart, a need to cut off from something to which one is still attached. Over-calculating in a vain attempt to overcome uncertainty.",
         "sequence": 77,
         "cardtype": "court"}

    ]

def pick_card():
    num = random.randint(0, len(deck) - 1)
    card = deck[num]['name']

    return card

## Telegram
token = '[YOUR TELEGRAM BOT KEY]'
bot = telegram.Bot(token=token)

# get user info
file_path = "./user_info.json"
user = {}

with open(file_path, 'r', encoding = 'UTF8') as json_file:
    user = json.load(json_file)

print('start conversation')

# 업데이터
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

#사용자 정보 저장
def user_json_save():
    with open(file_path, 'w', encoding = 'UTF8') as outfile:
        json.dump(user, outfile, indent=4)

#사용자 데이터 유무 확인
def check_user(user_id, user_name):
    if str(user_id) in user.keys():
        print(user_id, "is in user list")
        return True
    else:
        print(user_id, "is not in user list. Create new user")
        user[str(user_id)] = {'name' : f'{user_name}', 'tarot_topic' : '재물'}
        print("user ID {user_id} is created".format(user_id=user_id))

        user_json_save()

        return True    

# message reply function
def get_message(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    check_user(user_id, user_name)

    tarot_topic = user[str(user_id)]['tarot_topic']
    sel_card = pick_card()
    respond = tarotgpt.tarot_ask(update.message.text, tarot_topic, sel_card)

    update.message.reply_text(f"질문하신 주제에 대해 타로카드를 뽑습니다.")
    time.sleep(1)
    update.message.reply_text(f"선택된 카드는 {sel_card}입니다")
    update.message.reply_text(respond)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def topic_command(update, context):
    print('topic command')
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    check_user(user_id, user_name)

    chat_user = user[str(user_id)]
    chat_name = chat_user['name']
    chat_topic = chat_user['tarot_topic']
    
    topic_select_list = []
    for topic in tarot_topic:
        topic_select_list.append(InlineKeyboardButton(topic, callback_data=topic))
    topic_select_list.append(InlineKeyboardButton("cancel", callback_data="cancel"))
    
    topic_select_markup = InlineKeyboardMarkup(build_menu(topic_select_list, len(topic_select_list) - 1)) # make markup
    update.message.reply_text(f"안녕하세요 {chat_name}님! 현재 설정된 리딩 주제는 {chat_topic}입니다!!\n주제를 변경하고 싶다면, 변경하고 싶은 주제를 선택해주세요.", reply_markup=topic_select_markup)

def help_command(update, context):
    print('help')
    
    update.message.reply_text('안녕하세요. TarotGPT입니다.\n 리딩을 원하는 내용을 채팅 형태로 작성해주세요.\n 주제를 변경하고 싶으세면 /topic으로 주제를 변경하실 수 있습니다. \n 기본 설정된 주제는 "재물"입니다. 설정된 주제와 질문에 차이가 있으면 리딩이 정확하지 않을 수 있습니다.')

def callback_query(update, context):
    data_selected = update.callback_query.data
    user_id = update.callback_query.message.chat.id
    print("callback : ", data_selected, "user_id : ", user_id)

    if data_selected.find("cancel") != -1 :
        context.bot.edit_message_text(text="Cancelled",
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id)
        return
    elif data_selected in tarot_topic:
        print(user[str(user_id)]['tarot_topic'])
        user[str(user_id)]['tarot_topic'] = data_selected
        context.bot.edit_message_text(text="선택하신 주제가 {topic}으로 변경되었습니다.".format(topic = update.callback_query.data),
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id)
        print(user)
        user_json_save()


def main():
    topic_handler = CommandHandler('topic', topic_command)
    dispatcher.add_handler(topic_handler)

    start_handler = CommandHandler('help', help_command)
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(CallbackQueryHandler(callback_query))

    echo_handler = MessageHandler(Filters.text, get_message)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
