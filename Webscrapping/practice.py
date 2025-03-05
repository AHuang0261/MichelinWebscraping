from bs4 import BeautifulSoup

with open('Webscrapping\home.html', 'r') as file:
    content = file.read()
    soup = BeautifulSoup(content, 'lxml')
    course_tag = soup.find_all('div', class_ = 'card')
    for course in course_tag:
        name = course.h5.text
        price = course.a.text.split()[-1]
        print(f"{name} costs {price}")
