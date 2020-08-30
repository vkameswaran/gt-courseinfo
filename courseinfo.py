#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests
from sys import argv

# Validate input
if len(argv) < 2:
    print("Usage: courseinfo <CRN>+\n")
    exit(1)

# Create variables
TERM = "202008"
crns = argv[1:]
all_classes = []

# Scrape OSCAR
print()
for crn in crns:
    # Get the info from OSCAR
    url = "https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=" + TERM + "&crn_in=" + str(crn)
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    # Locate the info and extract format
    info = soup.select("td.dddefault")[0].text.split("Registration Availability")[0].replace("\n\n", "\n").replace("\n\n", "\n").strip()
    lines = info.split("\n")
    instr_method = [i for i in lines if "Instructional Method" in i][0]
    # Simplify course name
    full_name = soup.select("th.ddlabel")[0].text
    course = full_name.split(" - ")[2]
    section = full_name.split(" - ")[3]
    # Add course to list
    all_classes.append(((course + "  \t" + section), instr_method))

# Sort and format output
s1 = sorted(all_classes, key=lambda x: x[0])
s2 = sorted(s1, key=lambda x: x[1])
print("\n".join([i[0] + "\t" + i[1] for i in s2]))
print()
