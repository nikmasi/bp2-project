import searchWithoutIndex
from searchWithIndex import *
from searchWithoutIndex import *


if __name__=='__main__':
    file_x = input('Unesite naziv fajla: ')
    file = './tabele/' + file_x
    path = './tabele/'
    first = path
    first_map = None
    bitmap = {}
    with open(file, 'r') as f:
        first += f.readline()[:-1]
        first_map = create_id_position_map2(first)
        for line in f:
            line = line.split(',')
            line[-1] = line[-1][:-1]

            d = create_dict(line[0])
            maps = create_id_position_map(path + line[0])

            bitmap[line[1]] = BitmapIndex(d, line[1], line[1], maps,path+line[0])

    col = column_name(file)
    condition_str = input("Unesite vrednosti (ime_kolone='vrednost' AND/OR ime_kolone='vrednost'): ")
    aggregate = input("Unesite agregatnu fju i kolonu (sum,Age): ").split(',')
    st = time.time()
    data, suma = readFile(first, condition_str, aggregate)
    for i in data:
        print(i)
    print(f"Rezultat agregatne fje: {suma}")
    en = time.time()
    print(f"Vreme je: {(en - st) * 1000} ms")
    condition = parse_condition(condition_str)

    st1 = time.time()
    da,co = search_with_index1(d, condition, "AND", first, first_map,bitmap)
    rez = aggregate_function(da, co.index(aggregate[1]), aggregate[0])
    print(f"Rezultat: {suma}")
    for i in da:
        print(i)
    en1 = time.time()

    print(f"Vreme je: {(en1 - st1) * 1000}")
    print(f"\n Vreme bez indeksa: {1000*(en-st)} ms \n Vreme sa indeksom: {1000*(en1-st1)} ms \n ")
