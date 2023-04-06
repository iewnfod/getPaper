import bs4

with open("./subjects.htm", "r") as f:
    soup = bs4.BeautifulSoup(f.read(), "html.parser")
divs = soup.find_all("div")[1:]
SUBJECTS = {}
for i in divs:
    s = i.string
    print(s)
    k, v = s.split(" - ")
    SUBJECTS.update({k:v})


if __name__ == "__main__":
    print(SUBJECTS)
