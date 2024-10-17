#!/usr/bin/python3
import sys
import os.path
""" function that converts markdown to html """
def markup2html():
    if len(sys.argv) < 2:
        eprint("Usage: ./markdown2html.py README.md README.html")
        exit(1)

    if os.path.isfile(sys.argv[1]) == False:
        eprint("Missing {}".format(sys.argv[1]))
        exit(1)

    print("")
    exit(0)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def parse():
    """ dashBool at 0 represents that no ul list is open"""
    dashBool = 0
    odashBool = 0
    pdashBool = 0

    f = open(sys.argv[1], "r")
    for line in f:
        """ 
        if a list has been opened, dash bool is 1
        if the next line isnt a list item, dashbool remains at 2
        if it is it gets set to 1 again
        """
        if (dashBool == 1):
            dashBool = 2
        if (odashBool == 1):
            odashBool = 2
        if (pdashBool == 1):
            pdashBool = 2

        """ line that will be returned """
        finalLine = line

        if line[0] == "#":
            finalLine = mark2header(line)

        elif line[0] == "-":
            finalLine = mark2list(line, dashBool)
            dashBool = 1
        elif line[0] == "*":
            finalLine = mark2olist(line, odashBool)
            odashBool = 1
        elif line[0] != "" and line[0] != " " and line[0] != "\n":
            finalLine = mark2par(line, pdashBool)
            pdashBool = 1

        if os.path.isfile(sys.argv[2]) == False:
            print("file created\n")
            x = open(sys.argv[2], "x")
            x.close

        w = open(sys.argv[2], "a")

        if (dashBool == 2):
            w.write("</ul>\n")
            dashBool = 0
        if (odashBool == 2):
            w.write("</ol>\n")
            odashBool = 0
        if (pdashBool == 2):
            w.write("</p>\n")
            pdashBool = 0
        w.write("{}\n".format(finalLine))
        w.close()

    w = open(sys.argv[2], "a")
    if (dashBool == 1):
        w.write("</ul>\n")
        dashBool = 0
    if (odashBool == 1):
        w.write("</ol>\n")
        odashBool = 0
    if (pdashBool == 1):
        w.write("</p>\n")
        pdashBool = 0
    w.close()
    f.close()

    f = open(sys.argv[2], "r")
    for line in f:
        print(line)
    f.close()

def mark2header(line):
    count = 0
    for char in line:
        if char == "#":
            count += 1
            continue
        elif char == " ":
            head = "<h{}>".format(count)
            tail = "<h{}/>".format(count)
            finalLine = "{}{}{}".format(head, line[(count+1):].rstrip(), tail)
            return (finalLine)
            break
        else:
            break

def mark2list(line, dashbool):
    if (dashbool == 0):
        head = "<ul>\n"
    else:
        head = ""
    body = "<li>{}</li>".format(line[2:].rstrip())
    return "{}{}".format(head, body)

def mark2olist(line, dashbool):
    if (dashbool == 0):
        head = "<ol>\n"
    else:
        head = ""
    body = "<li>{}</li>".format(line[2:].rstrip())
    return "{}{}".format(head, body)

def mark2par(line, dashbool):
    templine = []
    if (dashbool == 0):
        head = "<p>\n"
    elif (dashbool == 2):
        head = "<br />\n"
    else:
        head = ""
    body = "{}".format(line.rstrip())
    return "{}{}".format(head, body)

parse()
