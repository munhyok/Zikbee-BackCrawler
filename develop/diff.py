import difflib

def matchFilter(input_string, product_string):
    weight = 0
    input_string = "니베아 리프레싱 페이셜 토너"
    product_string = "NIVEA 리프레싱 페이셜 토너 200ml"

    answer_string = answer_string.replace(',','')
    
    
    split_input = input_string.split()
    split_product = product_string.split()
    print(split_input)

    for i in range(len(split_input)):
        for j in range(len(split_product)):

            if split_input[i] in split_product[j]:
                print(f'{split_input[i]} yes')
                weight += 1

    print(weight)
    print(len(split_input))

    return weight/len(split_input)

        