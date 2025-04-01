import math
data = []

def main():
    print("gathering data...")
    with open("Restaurant_Info.txt", 'r', encoding='utf-8') as file:
        for line in file: 
            info = line.split(';')
            info[-1] = info[-1].strip()
            data.append(info)
    file.close()

    print("Enter lattitude and longitude:")
    center = input()
    center = center.split(',')
    center = [float(i) for i in center]
    
    print("Enter max distance (km):")
    distance = float(input())

    print("Enter max price(1-4):")
    price = int(input())

    locate(center, distance, price)
    
def locate(center, distance, price):
    count = 0
    for place in data:
        temp = place[3].split(',')
        if temp[0] == " N/A": continue
        coords = [float(i) for i in temp]
        if len(place[1].strip()) <= price and calc_distance(center, coords) < distance:
            print(place)
            count+=1
    if count == 0: print("None within specified parameters")

def calc_distance(c1, c2):
    d_lat = c1[0] - c2[0]
    d_lon = math.cos(c1[0] * math.pi / 180) * (c1[1] - c2[1])
    return math.sqrt(d_lat**2 + d_lon**2) * 111.3171

if __name__ == "__main__":
    main()
