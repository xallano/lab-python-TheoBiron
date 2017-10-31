with open("C:/Users/Théo/Downloads/jfkrelease-2017-dce65d0ec70a54d5744de17d280f3ad2.csv") as f:

    for line in f:
        array = line.split(';')
        print(array)
        print(len(array))