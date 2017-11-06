with open("C:/Users/Théo/Downloads/jfkrelease-2017-dce65d0ec70a54d5744de17d280f3ad2.csv") as f:
    max = 0
    min = 0
    count = 0
    tot = 0
    count_no_page = 0
    doc_type = {}
    agencies = {}

    for line in f:
        array = line.split(';')
        print(array)
        print("Number of fields", len(array))

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

        new_doc_type = array[6]
        if new_doc_type != "Doc Type":
            if new_doc_type not in doc_type:
                doc_type[new_doc_type] = 1
            else:
                doc_type[new_doc_type] += 1

        agency = array[4]
        if agency != "Agency":
            if agency not in agencies:
                agencies[agency] = 1
            else:
                agencies[agency] += 1

    print("Max:", max)
    print("Min:", min)
    print("Mean:", tot/count)
    print("Document with no pages:", count_no_page)
    print("Number of types:", len(doc_type))
    print(doc_type)
    print("Number of agencies:", len(agencies))
    print(agencies)