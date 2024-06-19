import time
from BitmapIndex import create_dict,BitmapIndex
import mmap
from searchWithoutIndex import parse_condition

def column_name(file_path):
    with open(file_path,'r') as f:
        keysa=f.readline().split(',')
        keysa[-1] = keysa[-1][:-1]
        dict = {}
        for v in keysa:
            x = v.split('=')
            dict[x[0]] = ''
    return dict
def aggregate_function(table, column, function):
    values=[]
    for row in table:
        x=row.split(',')
        if(x[column][-1]=="\r"):
            x[column]=x[column][:-1]
        values.append(int(x[column]))

    if function == 'min':
        return min(values)
    elif function == 'max':
        return max(values)
    elif function == 'avg':
        return sum(values) / len(values)
    elif function == 'sum':
        return sum(values)
    elif function == 'count':
        return len(values)
def bitwise_and(bitmap1, bitmap2):
    return [b1 & b2 for b1, b2 in zip(bitmap1, bitmap2)]

def bitwise_and2(bitmap1, bitmap2):
    return [i for i, (b1, b2) in enumerate(zip(bitmap1, bitmap2)) if b1 & b2]
def bitwise_or(bitmap1, bitmap2):
    return [b1 | b2 for b1, b2 in zip(bitmap1, bitmap2)]
def create_id_position_map(file_path):
    id_position_map = {}
    with open(file_path, 'r') as f:
        # Preskoči header
        header = f.readline()
        position = f.tell()

        while True:
            line = f.readline()
            if not line:
                break
            row_data = line.strip().split(',')

            row_id = int(row_data[-1])
            id_position_map[row_id] = position
            position = f.tell()

    return id_position_map
def create_id_position_map2(file_path):
    id_position_map = {}
    with open(file_path, 'r') as f:
        # Preskoči header
        header = f.readline()
        position = f.tell()

        while True:
            line = f.readline()
            if not line:
                break
            row_data = line.strip().split(',')

            row_id = row_data[0]
            id_position_map[row_id] = position
            position = f.tell()

    return id_position_map

def search_with_index2(table,conditions,operation,file_path,maps,bitmap):
    result = None
    current_operator = None

    for column, value, operator in conditions:
        if result is None:
            result = bitmap[column].get_bitmap(value)
            maps=bitmap[column].maps
        elif current_operator == 'AND':
            result = bitwise_and(result,bitmap[column].get_bitmap(value))
        elif current_operator == 'OR':
            result = bitwise_or(result,bitmap[column].get_bitmap(value))

        current_operator = operator if operator else current_operator

    data = []

    result_indices = [i for i, bit in enumerate(result) if bit == 1]
    with open(file_path, 'r+b') as f:

        mmapped_file = mmap.mmap(f.fileno(), 0)

        #print(maps)
        for index in result_indices:
            if str(index + 1) in maps:
                mmapped_file.seek(maps[str(index + 1)])

                line = mmapped_file.readline().decode('utf-8')[:-1]
                data.append(line)
            else:
                print(f"Warning: Index {index + 1} not found in maps")

    return data

def search_with_index1(table,conditions,operation,file_path,maps,bitmap):
    result = None
    current_operator = None
    maps={}

    for column, value, operator in conditions:
        if result is None:
            result = bitmap[column].get_bitmap(value)
            maps[bitmap[column].path]=bitmap[column].maps
        elif current_operator == 'AND':
            result = bitwise_and(result,bitmap[column].get_bitmap(value))
            maps[bitmap[column].path]=bitmap[column].maps
        elif current_operator == 'OR':
            result = bitwise_or(result,bitmap[column].get_bitmap(value))
            maps[bitmap[column].path]=bitmap[column].maps

        current_operator = operator if operator else current_operator

    data = []

    result_indices = [i for i, bit in enumerate(result) if bit == 1]
    for n, ma in maps.items():

        with open(n, 'r+b') as f:

            mmapped_file = mmap.mmap(f.fileno(), 0)
            colons =mmapped_file.readline().decode('utf-8').split(',')

            #print(maps)
            for index in result_indices:

                    if index + 1 in ma:
                        mmapped_file.seek(ma[index + 1])

                        line = mmapped_file.readline().decode('utf-8')[:-1]
                        data.append(line)
                    else:
                        print(f"Warning: Index {index + 1} not found in maps")

    return data,colons

if __name__=='__main__':
    file_x = input('Unesite naziv fajla: ')
    file = './tabele/' + file_x
    path='./tabele/'
    first=path
    first_map=None
    bitmap={}
    with open(file,'r') as f:
        first+=f.readline()[:-1]
        first_map=create_id_position_map2(first)
        for line in f:
            line=line.split(',')
            line[-1]=line[-1][:-1]
            print(line)

            d = create_dict(line[0])
            maps = create_id_position_map(path+line[0])
            #print(d)

            bitmap[line[1]]=BitmapIndex(d, line[1],line[1],maps,path+line[0])
    print(bitmap)

    condition_str = input("Unesite vrednosti (ime_kolone='vrednost' AND/OR ime_kolone='vrednost'): ")
    condition=parse_condition(condition_str)
    st1 = time.time()
    da,co = search_with_index1(d, condition, "AND", path+'carsCarMake.txt',first_map,bitmap)

    en1 = time.time()
    for i in da:
        print(i)
    print(f"Vreme je: {(en1 - st1) * 1000}")


