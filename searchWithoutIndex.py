import time
import re
def parse_condition(condition_str):
    """
    (column, value, operator)
    Example: "Car Make='Honda' OR Car Make='Suzuki'" ->('Car Make', 'Honda', 'OR'), ('Car Make', 'Suzuki', '')]
    """
    condition_pattern = re.compile(r"(\w+\s*\w*=\s*'\w+')\s*(AND|OR)?")
    matches = condition_pattern.findall(condition_str)
    parsed_conditions = []
    for match in matches:
        column_value, operator = match
        column, value = column_value.split('=')
        column = column.strip()
        value = value.strip().strip("'")
        parsed_conditions.append((column, value, operator))
    return parsed_conditions
def evaluate_conditions(person_dict, conditions):
    """
    AND and OR
    """
    result = None
    current_operator = None

    for column, value, operator in conditions:
        condition_met = person_dict.get(column) == value

        if result is None:
            result = condition_met
        elif current_operator == 'AND':
            result = result and condition_met
        elif current_operator == 'OR':
            result = result or condition_met

        current_operator = operator if operator else current_operator

    return result

def readFile(file_path, condition_str, aggregate=None):
    data_list = []
    aggregate_func = aggregate[0].lower()
    aggregate_column = aggregate[1]
    values = []

    conditions = parse_condition(condition_str)
    print(conditions)

    with open(file_path, 'r') as f:
        keysa = f.readline().strip().split(',')

        for line in f:
            l = line.strip().split(',')
            person_dict = dict(zip(keysa, l))

            if evaluate_conditions(person_dict, conditions):
                value = int(person_dict[aggregate_column])
                values.append(value)
                data_list.append(person_dict)

    if aggregate_func == 'sum':
        result = sum(values)
    elif aggregate_func == 'min':
        result = min(values)
    elif aggregate_func == 'max':
        result = max(values)
    elif aggregate_func == 'count':
        result = len(values)
    elif aggregate_func == 'avg':
        result = sum(values) / len(values) if values else 0
    else:
        result = None

    return data_list, result

def column_name(file_path):
    with open(file_path, 'r') as f:
        keysa = f.readline().strip().split(',')
        dict1 = {key: '' for key in keysa}
    return dict1

if __name__ == '__main__':
    file_x = input('Unesite naziv fajla: ')
    file = './tabele/' + file_x

    col = column_name(file)
    condition_str = input("Unesite vrednosti (ime_kolone='vrednost' AND/OR ime_kolone='vrednost'): ")
    aggregate = input("Unesite agregatnu fju i kolonu (sum,Age): ").split(',')

    st = time.time()
    data, suma = readFile(file, condition_str, aggregate)
    for i in data:
        print(i)
    print(f"Rezultat agregatne fje: {suma}")
    en = time.time()
    print(f"Vreme je: {(en - st) * 1000} ms")