import time

def create_dict(file):
    file_path ='./tabele/'+   file
    data_list = []

    with open(file_path, 'r') as f:
        # Učitavanje prvog reda kao nazivi ključeva
        keys = f.readline().strip().split(',')

        # Učitavanje preostalih redova kao vrednosti
        for line in f:
            values = line.strip().split(',')
            # Kreiranje rečnika za svaki red
            row_dict = {keys[i]: values[i] for i in range(len(keys))}
            data_list.append(row_dict)

    return data_list
class BitmapIndex:
    def __init__(self, table, column,name,maps,path):
        self.path=path
        self.name=name
        self.table = table
        self.maps=maps
        self.column = column
        self.index = {}
        self.create_bitmap_index()

    def create_bitmap_index(self):
        unique_values = set(row[self.column] for row in self.table)
        for value in unique_values:
            bitmap = [1 if row[self.column] == value else 0 for row in self.table]
            self.index[value] = bitmap

    def create_bitmap_index2(self):
        unique_values = set(row[self.column] for row in self.table)
        for value in unique_values:
            bitmap = ''.join(['1' if row[self.column] == value else '0' for row in self.table])
            self.index[value] = bitmap

    def get_bitmap(self, value):
        return self.index.get(value, [0] * len(self.table))



if __name__=='__main__':
    table=create_dict('cars.txt')
    #print(table)
    kolona=str(input('Unesi ime kolone: '))
    tt1=time.time()
    bm=BitmapIndex(table, kolona)
    tt2=time.time()
    print(tt2-tt1)
