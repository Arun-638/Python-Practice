#you are given a published google doc link, which contains a secret message. The message is hidden in the text, and you need to decode it to find out what it says.
#your task is to  wrtie a fucntion that takes in the URL for such a Google doc as an arguement,retrieves and parses the data in the document and prints the grid of characters. when printed in a fixed-width font,the character in the grid will form a graphic showing a seqeuence of uppercase letters,which is the secret message.
#the document specifies the unicode characters in the grid,along with the x and y coordinates for each character.
#The minimum possible value of these coordinates is 0. there is no maximum value for the coordinates, but the grid will be large enough to contain all the characters specified in the document.
#Any positions in the grid that do not have a specified character should be filled with a space character (' ').
#note that the coordinates (0,0) will always correspond to the same corner of the grid in the example,so make sure to understand in which direction the x and y coordinates increase when constructing the grid.
# there are 3 columns x-coordinate,character,y-coordinate in the table ith records the x and y coordinates and the unicode character for a specific position in the grid. The x-coordinate increases from left to right, and the y-coordinate increases from top to bottom.
import requests
from bs4 import BeautifulSoup

def decode_message(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    data = {}
    for row in rows[1:]:
        cols = row.find_all("td")
        x = int(cols[0].text)
        ch = cols[1].text.strip()
        y = int(cols[2].text)
        data[(x, y)] = ch
    max_x = 0
    max_y = 0
    for x, y in data:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in data:
                line += data[(x, y)]
            else:
                line += " "
        print(line)
url = input("Enter the URL: ")
decode_message(url)