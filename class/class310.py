def linear_search(list1, element):
    found = False
    for i in list1:
        # print(i)
        if i==element:
            found =True

    if found ==True:
            print(element, "element found")
    else:
            print(element, "not found")


