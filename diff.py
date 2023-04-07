import difflib

def matchFilter(input_string, product_string):
    weight = 0


    product_string = product_string.replace(',','')
    
    
    split_input = input_string.split()
    split_product = product_string.split()
    

    for i in range(len(split_input)):
        for j in range(len(split_product)):

            if split_input[i] in split_product[j]:
                print(f'{split_input[i]} yes')
                weight += 1

    print(weight)
    print(len(split_input))
    result = weight/len(split_input)
    return result

        