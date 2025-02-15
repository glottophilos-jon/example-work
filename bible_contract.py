from urllib import request
import json
import platform
import os
import signal
import sys

# determine platform for file gens later
plattype = platform.system()
extensions = [".txt",".tex"]

# set up skeleton for API requests
def runrequest(requesturl):
    myheaders = {'User-Agent':'Mozilla/5.0'}
    req = request.Request(requesturl, headers=myheaders)
    res = request.urlopen(req)
    return res

# handler for Ctrl+C SIGINT kill, allows graceful death
def signal_handler(sig, frame):
    print('\nOperation canceled!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# creating a Passage class to define behaviors and attributes of each Bible passage
class Passage:
    # get the ball rolling
    def __init__(self):
        self.version = self.getversion()
        self.book = self.getbook()
        print("What verse would you like to access?")
        self.initialverse = self.getfullverse()
        checkforsecond = input("Would you like to input a second verse to get the whole passage? y/n ")
        self.secondverse = None
        if checkforsecond in {"y", "Y", "yes", "Yes"}:
            secondvalid = False
            while secondvalid == False:
                self.secondverse = self.getfullverse()
                if self.secondverse[0] > self.initialverse[0]:
                    secondvalid = True
                elif self.secondverse[0] == self.initialverse[0] and self.secondverse[1] > self.initialverse[1]:
                    secondvalid = True
                else:
                    print("The second verse must follow the first verse.")
        self.text = self.settext()

    # set up behavior for grabbing the Bible version
    def getversion(self):
        verreq = "https://api.getbible.net/v2/translations.json"
        try:
            verres = runrequest(verreq)
        except Exception as e:
            print("There was an error accessing the Bible API, please try again later.\n", str(e))
            exit()
        
        try:
            vers = json.load(verres)
        except Exception as e:
            print("There was an error getting the version list, please confirm that the API URL is up to date.\n", str(e))
            exit()
        validver = False
        while validver == False:
            version = input("What version of the Bible would you like to use? ")
            if version in vers:
                print("Great! Your version has been set to:", vers[version]["translation"])
                validver = True
            else:
                print("That is not a valid version.")
                checkvers = False
                while checkvers == False:
                    seevers = input("Would you like to see a list of the available versions? y/n ")
                    if seevers in {"y", "Y", "yes", "Yes"}:
                        for name in vers:
                            print(name, "-", vers[name]["translation"])
                            checkvers = True
                    elif seevers in {"n", "N", "no", "No"}:
                        checkvers = True
                    else:
                        print("Invalid input.")
        return version

    # set up behavior for grabbing the right book
    def getbook(self):
        bookreq = "https://api.getbible.net/v2/kjv/books.json"
        try:
            bookres = runrequest(bookreq)
        except Exception as e:
            print("There was an error accessing the Bible API, please try again later.\n", str(e))
            exit()
        try:
            books = json.load(bookres)
        except Exception as e:
            print("There was an error accessing the selected version, please ensure that the API URL is correct.\n", str(e))
            exit()
        validbook = False
        while validbook == False:
            book = input("What book would you like to access? ")
            bookfound = False
            for entry in books:
                entryname = books[entry]["name"]
                if entryname.lower() == book.lower():
                    bookname = entryname
                    bookfound = True
                    bookno = books[entry]["nr"]
                    requesturl = "https://api.getbible.net/v2/" + self.version + "/" + str(bookno) + "/1.json"
                    try:
                        runrequest(requesturl)
                        validbook = True
                    except Exception as e:
                        print("The book you are trying to select does not exist in the current version.")
            if bookfound == False:
                print("Invalid book name.")
        return bookno, bookname

    # set up behavior for getting verses, this can be reused
    def getfullverse(self):
        validverse = False
        while validverse == False:
            fullverse = input("Please enter in the format chapter:verse ").split(':')
            if len(fullverse) == 2 and fullverse[0].isnumeric() and fullverse[1].isnumeric():
                chapter = int(fullverse[0])
                verse = int(fullverse[1]) - 1
                requesturl = "https://api.getbible.net/v2/" + self.version + "/" + str(self.book[0]) + "/" + str(chapter) + ".json"
                try:
                    checkres = runrequest(requesturl)
                    checkjson = json.load(checkres)
                    versedata = checkjson["verses"][verse]
                    validverse = True
                except Exception as e:
                    print("The verse you have selected does not exist, or the API URL is out of date.")
            else:
                print("Invalid chapter and verse format.")

        return chapter, verse

    # grab the actual text of the selected version, book, chapters, and verses
    def settext(self):
        # handle single verse
        if self.secondverse == None:
            requesturl = "https://api.getbible.net/v2/" + self.version + "/" + str(self.book[0]) + "/" + str(self.initialverse[0]) + ".json"
            res = runrequest(requesturl)
            jsondata = json.load(res)

            text = jsondata["verses"][self.initialverse[1]]["text"]
        else:
            # handle multiple verses
            firstchapter = self.initialverse[0]
            lastchapter = self.secondverse[0]
            firstverse = self.initialverse[1] + 1
            lastverse = self.secondverse[1] + 1

            # multiple verses, one chapter
            if firstchapter == lastchapter:
                requesturl = "https://api.getbible.net/v2/" + self.version + "/" + str(self.book[0]) + "/" + str(firstchapter) + ".json"
                res = runrequest(requesturl)
                jsondata = json.load(res)

                text = []
                for verse in jsondata["verses"]:
                    if verse["verse"] >= firstverse and verse["verse"] <= lastverse:
                        text.append(verse["text"])
            else:
                # multiple verses, multiple chapters
                requesturl = "https://api.getbible.net/v2/" + self.version + "/" + str(self.book[0]) + "/" + str(firstchapter) + ".json"
                res = runrequest(requesturl)
                jsondata = json.load(res)

                text = []
                for verse in jsondata["verses"]:
                    if verse["verse"] >= firstverse:
                        text.append(verse["text"])
                firstchapter += 1

                while firstchapter <= lastchapter:
                    requesturl = "https://api.getbible.net/v2/" + self.version + "/" + str(self.book[0]) + "/" + str(firstchapter) + ".json"
                    res = runrequest(requesturl)
                    jsondata = json.load(res)

                    if jsondata["chapter"] == lastchapter:
                        for verse in jsondata["verses"]:
                            if verse["verse"] <= lastverse:
                                text.append(verse["text"])
                        firstchapter += 1
                    else:
                        for verse in jsondata["verses"]:
                            text.append(verse["text"])
                        firstchapter += 1

        return text

    # set up behavior for generating LaTeX file with skeleton for modified version of expex
    def tolatex(self):
        windowsfilename = "Desktop\\" + headline.replace(":", "_") + extensions[1]
        otherfilename = "Desktop/" + headline.replace(":", "_") + extensions[1]
        if plattype == 'Windows':
            outputfile = open(windowsfilename, "w", encoding="utf-8")
        else:
            otherbase = os.path.expanduser('~')
            otherfilename = os.path.join(otherbase, otherfilename)
            outputfile = open(otherfilename, "w", encoding="utf-8")
        if isinstance(self.text, str):
            words = self.text.split()
            for word in words:
                outputfile.write(word)
                outputfile.write("[\\te{}/\\te{}]{}\n")
            outputfile.close()
        else:
            for line in self.text:
                words = line.split()
                for word in words:
                    # this handles an initial attempt at verse numbering, you will need to review it manually
                    if words.index(word) == 0:
                        latex = word + "[\\te{}/\\te{}]{y}\n"
                    else:
                        latex = word + "[\\te{}/\\te{}]{}\n"
                    outputfile.write(latex)
            outputfile.close()

newpass = Passage()

# run some default behavior, start with defining the first few lines of the default output file
if newpass.secondverse == None:
    headline = newpass.book[1] + " " + str(newpass.initialverse[0]) + ":" + str(newpass.initialverse[1] + 1)
else:
    headline = newpass.book[1] + " " + str(newpass.initialverse[0]) + ":" + str(newpass.initialverse[1] + 1) + "-" + str(newpass.secondverse[0]) + ":" + str(newpass.secondverse[1] + 1)

wordcount = 0
if isinstance(newpass.text, str):
    wordcount = len(newpass.text.split())
else:
    for line in newpass.text:
        words = line.split()
        wordcount += len(words)

# open up default output file and write to it
windowsfilename = "Desktop\\" + headline.replace(":", "_") + extensions[0]
otherfilename = "Desktop/" + headline.replace(":", "_") + extensions[0]

if plattype == 'Windows':
    finalname = windowsfilename
    outputfile = open(windowsfilename,"w", encoding="utf-8")
else:
    otherbase = os.path.expanduser('~')
    otherfilename = os.path.join(otherbase, otherfilename)
    finalname = otherfilename
    outputfile = open(otherfilename,"w", encoding="utf-8")
outputfile.write(headline)
secondline = "\nWordcount is: " + str(wordcount) + "\n\n"
outputfile.write(secondline)
if isinstance(newpass.text, str):
    outputfile.write(newpass.text)
else:
    for line in newpass.text:
        newline = line + "\n"
        outputfile.write(newline)
outputfile.close()

print("File written successfully! Check the output in ",finalname)

# check if the user wants to generate a LaTeX file and write one if they want
validlatex = False
while validlatex == False:
    latexcheck = input("Would you like to output the verses in LaTeX code for interlinear translation? y/n ")
    if latexcheck in {"y", "Y", "yes", "Yes"}:
        newpass.tolatex()
        validlatex = True
    elif latexcheck in {"n", "N", "no", "No"}:
        validlatex = True
    else:
        print("Invalid input.")
