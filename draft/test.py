with open('draft\colleges.txt') as result:
        uniqlines = set(result.readlines())
        with open('draft/rmdup.txt', 'w') as rmdup:
            rmdup.writelines(set(uniqlines))