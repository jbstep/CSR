#! python3

import pyperclip, re, PyPDF2, os, pyshorteners, send2trash

# Where CSR's are stored
mypath = 'D:\\Dropbox\\sandbox\\CSR\\work\\'

# Get filenames
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


# Switch from Lastname, Firstname to Firstname Lastname
def swapName(name):
    lfname = name.split(',')
    fname = str(lfname[1])
    fname = fname.lstrip()
    lname = str(lfname[0])
    flname = fname + ' ' + lname
    return flname


# Open the PDF file and grab contents
def openPDF(i):
    infoPath = mypath + str(onlyfiles[i])
    infoPath = str(infoPath)
    pdfFileObj = open(infoPath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    result = pageObj.extractText()
    return result


# Scrape PDF -- not working :/
def scrapePDF(i1, i2):
    string = str('reg'.group(0))
    string = string[i1:i2]
    return string


# Assign contents to variables for scraping
text = openPDF(1)
csrText = openPDF(0)


# Client Name
nameReg = re.search(r'(XXX-XX-\d{4})(.*)?(Alabama)', text)
if nameReg == None:
    name = 'None'
    flname = ''
else:
    name = str(nameReg.group(0))
    name2 = str(nameReg.group(0))
    name2Reg = re.search(r'(XXX-XX-\d{4})(.*)?(\d\d)', name)
    name = str(name2Reg.group())
    name = name[11:-7]
    flname = swapName(name)

# Counselor Name
counselorReg = re.search(r'(\d\d\-)(.*)(Alabama)', text)
if counselorReg == None:
    counselor = 'None'
    flcounselor = ''
else:
    counselor = str(counselorReg.group(0))
    counselor = counselor[7:-7]
    flcounselor = swapName(counselor)

# Street Name
streetReg = re.search(r'(Address:2)(.*)(E-Mail)', text)
street = str(streetReg.group(0))
street = street[18:-6]

# City, State, and Zip
cityReg = re.search(r'((Phone:Voice:TDD:Fax:)(.*)(AL)([0-9]{5}))', text)
city = str(cityReg.group(0))
city = city[20:-7]
zip = str(cityReg.group())
zip = zip[-5:]

# Phone Numbers
phoneReg = re.search(r'''(
    (\d{3}|\(\d{3}\))?              # area code
    (\s|-|\.)?                      # separator
    (\d{3})                         # first 3 digits
    (\s|-|\.)                       # separator
    (\d{4})                         # last 4 digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))?  # extension
    )''', text, re.VERBOSE)

phone = str(phoneReg.group())

secPhoneReg = re.search(r'((\(\d{3}\))(\s\d{3}\-\d{4})(NoNoNoNo))', text)
if secPhoneReg == None:
    secPhone = 'None'
else:
    secPhone = str(secPhoneReg.group())
    secPhone = secPhone[:-8]

# Email
emailReg = re.search(r'(NoNoNoNo)(.*)(Directions)', text)
if emailReg == None:
    email = 'None'
else:
    email = str(emailReg.group())
    email = email[8:-10]

# Directions
directionsReg = re.search(r'((Home:)(.*)(3. Char))', text)
if directionsReg == None:
    directions = 'None'
else:
    directions = str(directionsReg.group())
    directions = directions[5:-7]

# Grab comments:
commentsReg = re.search(r'((Comments)(.*)(4\.))', csrText)
if commentsReg == None:
    comments = 'None'
else:
    comments = str(commentsReg.group())
    comments = comments[9:-2]

fullAddress = street + ', ' + city + ', AL ' + zip
urlAddress = fullAddress.replace(" ", "_")


# Shorten map search url
from pyshorteners import Shortener

url = str('http://www.google.com/maps/search/' + urlAddress)
shortener = Shortener('Tinyurl')
urlAddress = str(shortener.short(url))


# Stitch it all together and stick subject of email at end
entry = str(
    'Client Name: ' + flname + '\n' + 'Counselor: ' + flcounselor + '\n' + 'Address: ' + fullAddress + '\n' + 'Map: ' + urlAddress + '\n' + 'Primary Phone: ' + phone + '\n' + 'Secondary phone: ' + secPhone + '\n' + 'Email: ' + email + '\n' + '\n' + 'Directions to home: ' + '\n' + directions + '\n' + '\n' + 'Comments: ' + '\n' + comments + '\n\n' + flname + ' - ' + city)

print(entry)
pyperclip.copy(entry)

'''
won't delete second file (personal info)

# Empty directory when finished
for folderName, subfolders, filenames in os.walk(mypath):
    for filename in filenames:
        send2trash.send2trash(os.path.join(folderName, filename))

'''
