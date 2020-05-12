def append_to_file(oasis_link):
    file = open("oasis_farm_list.txt", "a")
    file.write(oasis_link)
    file.write("\n")
    file.close()


def read_oasis_from_file(farm_index):
    with open("oasis_farm_list.txt", "r") as file:
        a = [line.strip() for index, line in enumerate(file.readlines()) if index == farm_index]
        print(a)
        return a[0]


def read_all_oasis_from_file():
    with open("oasis_farm_list.txt", "r") as file:
        a = [line.strip() for line in file.readlines()]
        print(a)
        return a
