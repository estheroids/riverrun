import json
import random
import re
import textwrap
import subprocess
import io

from olipy.markov import MarkovGenerator


DASH = u"\u2014"
has_dash = re.compile(DASH)

episode_names = [ "Telemachus",
        "Nestor",
        "Proteus",
        "Calypso",
        "LotusEaters",
        "Hades",
        "Aeolus",
        "Lestrygonians",
        "ScyllaCharybdis",
        "WanderingRocks",
        "Sirens",
        "Cyclops",
        "Nausicaa",
        "OxenOfTheSun",
        "Circe",
        "Eumaeus",
        "Ithaca",
        "Penelope"]


text_files = []
for i,e in enumerate(episode_names):
    text_files.append("txt/%02d%s.txt"%(i+1,e.lower()))




money = []



for ii,text_file in enumerate(text_files):

    if(ii>5):
        break

    money.append(u"\n\n")
    money.append(u" [ %02d %s ]"%(ii+1, episode_names[ii]) )
    money.append(u"\n\n")


    #############################################
    # Fixed markov generator

    with io.open(text_file, 'r', encoding="utf-8") as f:
        generator = MarkovGenerator.loadlines(f, order=2, max=800)


    how_many_paragraphs = int(round(random.random()*150))
    how_many_sentences = 10

    for iip in range(how_many_paragraphs):

        par = ""

        for iis in range(how_many_sentences):

            sentence = list(generator.assemble())

            letter_and_a_line = re.compile(r'^ {0,}[a-zA-Z]\n$')
            comma_and_a_space = re.compile(r'[a-zA-Z] {1,},')
            excl_and_a_space = re.compile(r' !')

            # Examine each word in the new sentence
            for cs,s in enumerate(sentence):

                # Insert newline when there is a dialogue symbol
                if( has_dash.search(s) ):
                    d = has_dash.sub("\n"+DASH,s)
                    sentence[cs] = d
                    sentence[-1] = s[-1]+"\n"

                # Replace single-letter oops words \n with just \n 
                if( letter_and_a_line.search(s) ):
                    del sentence[cs]

                # Fix "stuff ," spacing
                if( comma_and_a_space.search(s) ):
                    sentence[cs] = re.sub(" {1,},", ",", s)

                # Fix "stuff !" spacing
                if( excl_and_a_space.search(s) ):
                    sentence[cs] = re.sub(" !", "!", s)

            # Capitalize first word of sentence
            # (if contains dash, capitalize second word):
            i = 0
            if( has_dash.search(sentence[0]) ):
                i = 1
            try:
                sentence[i] = sentence[i].capitalize()
            except:
                pass


            # Add period to end of sentence:
            last_word = sentence[-1]
            last_letter = last_word[-1]
            if(last_letter<>"." and last_letter<>"?" 
                    and last_letter<>":" and last_letter<>","
                    and last_letter<>"!" and last_letter<>"\n"):
                sentence[-1] = sentence[-1] + "."




            # Turn the Markov-generated paragraph into a string
            par += " " 
            par += " ".join(sentence)
            par = par.strip()

        # Add the string to the money list (what goes in the file)
        money.append(par)
        money.append(u"\n")


for m in money:
    m = m.strip() + "\n" 

#for m in money:
#    print "------"
#    print type(m)
#    print [m]
#    print "------"

with io.open('markov_novel.txt','w', encoding='utf-8') as f:
    f.writelines(money)

