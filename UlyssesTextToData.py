import json
import re

chapter_names = ['telemachus',
        'nestor',
        'proteus',
        'calypso',
        'lotuseaters',
        'hades',
        'aeolus',
        'lestrygonians',
        'scyllacharybdis',
        'wanderingrocks',
        'sirens',
        'cyclops',
        'nausicaa',
        'oxenofthesun',
        'circe',
        'eumaeus',
        'ithaca',
        'penelope']

def std_chapter(n):
    if n>0 and n<19:
        txtfile = "txt/%02d%s.txt"%( n, chapter_names[n-1] )
        datfile = "data/%02d%s.dat"%( n, chapter_names[n-1] )

    # Load lines from file into list
    with open(txtfile,'r') as f:
        oldparagraphs = f.readlines()


    paragraphs = []
    newline = ""
    for oldparagraph in oldparagraphs:
        if(oldparagraph <> "\n"): 
            newline = newline + re.sub("\n"," ",oldparagraph)
        else:
            paragraphs.append(newline)
            newline = ""



    # Parse and output in json format 
    with open(datfile,'w') as o:
    
        print("Processing "+chapter_names[n-1])

        # One json object/"dictionary" per paragraph
        for i,paragraph in enumerate(paragraphs):
    
            # Turn the paragraph into a list of sentences
            sentences = paragraph.strip().split(". ")

            sentences = [s for s in sentences if len(s) > 1]

            if(len(sentences) > 0):

                #import pdb; pdb.set_trace()
    
                # If the last character of the line is just a letter,
                # add a period at the end.
                for (i,s) in enumerate(sentences):
                    last_letter = s[len(s)-1]
                    if( last_letter.isalpha() ):
                        # Add the period back to the end
                        sentences[i] = sentences[i] + "."

                # Construct dictionary
                d = {}
                d['parid'] = i
                d['par'] = sentences
    
                # Dump dictionary to output file
                json.dump(d, o)
                o.write("\n")

    print("Done processing "+chapter_names[n-1])
    print("Input: "+txtfile)
    print("Output: "+datfile)
    print("\n")






def ch18():
    n=18
    txtfile = "txt/%02d%s.txt"%( n, chapter_names[n-1] )
    datfile = "data/%02d%s.dat"%( n, chapter_names[n-1] )

    # Load lines from file into list
    with open(txtfile,'r') as f:
        oldparagraphs = f.readlines()

    paragraphs = []
    newline = ""
    for oldparagraph in oldparagraphs:
        if(oldparagraph <> "\n"): 
            newline = newline + re.sub("\n"," ",oldparagraph)
        else:
            paragraphs.append(newline)
            newline = ""


    # Parse and output in json format 
    with open(datfile,'w') as o:
    
        print("Processing "+chapter_names[n-1])

        # One json object/"dictionary" per paragraph
        for i,paragraph in enumerate(paragraphs):
    
            # Turn the paragraph into a list of sentences
            fragments = paragraph.strip().split("I ")
            fragments = ["I "+j for j in fragments]
            
            # Construct dictionary
            d = {}
            d['parid'] = i
            d['par'] = fragments
    
            # Dump dictionary to output file
            json.dump(d, o)
            o.write("\n")

    print("Done processing "+chapter_names[n-1])
    print("Input: "+txtfile)
    print("Output: "+datfile)
    print("\n")





if __name__=="__main__":
    for i in range(18):
        if( (i+1) is 18 ):
            ch18()
        else:
            std_chapter(i+1)
