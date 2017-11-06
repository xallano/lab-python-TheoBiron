import time

with open("C:/Users/Théo/Downloads/jfkrelease-2017-dce65d0ec70a54d5744de17d280f3ad2.csv") as f:
    max = 0
    min = 0
    count = 0
    tot = 0
    count_no_page = 0
    doc_type = {}
    agencies = {}
    date = ''
    year = 0
    month = 0
    day = 0
    oldest_date = time.strptime('12/30/1999', "%m/%d/%Y")
    newest_date = time.strptime('01/01/1900', "%m/%d/%Y")
    dates = {}

    for line in f:
        array = line.split(';')

        # Question 1
        print(array)
        print("Number of fields", len(array))


        # Question 2
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

        # Question 3 : doc types
        new_doc_type = array[6]
        if new_doc_type != "Doc Type":
            if new_doc_type not in doc_type:
                doc_type[new_doc_type] = 1
            else:
                doc_type[new_doc_type] += 1


        # Question 3 : agencies
        agency = array[4]
        if agency != "Agency":
            if agency not in agencies:
                agencies[agency] = 1
            else:
                agencies[agency] += 1


        # Question 4 : dates
        if array[5] != 'Doc Date':
            try:
                date = time.strptime(array[5], '%m/%d/%Y')

            except:
                pass

            if newest_date < date:
                newest_date = date
            if oldest_date > date:
                oldest_date = date

            if date not in dates:
                dates[date] = 1
            else:
                dates[date] += 1



    print("\nMax:", max)
    print("Min:", min)
    print("Mean:", tot/count)
    print("Document with no pages:", count_no_page, "\n")
    print("Number of types:", len(doc_type))
    print(doc_type, "\n")
    print("Number of agencies:", len(agencies))
    print(agencies, "\n")
    print("Oldest date:", oldest_date[0],'/', oldest_date[1],'/', oldest_date[2])
    print("Newest date:", newest_date[0],'/', newest_date[1],'/', newest_date[2])
    print("Number of documents per year:", dates)