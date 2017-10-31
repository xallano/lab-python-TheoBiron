with open("C:/Users/Théo/Downloads/jfkrelease-2017-dce65d0ec70a54d5744de17d280f3ad2.csv") as f:
    max = 0
    min = 0
    count = 0
    tot = 0
    count_no_page = 0
    for line in f:
        array = line.split(';')
        print(array)
        try:
            page_nb = int(array[11])
            if max < page_nb:
                max = page_nb
            if min > page_nb:
                min = page_nb
            tot += page_nb
            count += 1
        except:
            count_no_page += 1

        print("Number of fields", len(array))

    print("Max:", max)
    print("Min:", min)
    print("Mean:", tot/count)
    print("Document with no pages:", count_no_page)