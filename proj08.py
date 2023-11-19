###########################################################
#  Computer Project #8
#
#    define functions
#       1. open file
#       2. read names
#       3. read friends
#       4. create friends dict
#       5. find common friends 
#       6. find max friends 
#       7. find max common friends 
#       8. find second friends 
#       9. find max second friends 
#    define main
#       Only had to handle option 4 in the main:
#           Prompt for a name and print the name’s friends. 
#           If the name is not valid, re-prompt until it is a valid name.
###########################################################
MENU = '''
 Menu : 
    1: Popular people (with the most friends). 
    2: Non-friends with the most friends in common.
    3: People with the most second-order friends. 
    4: Input member name, to print the friends  
    5: Quit                       '''
    
def open_file(s):
    '''
    Open the promted file.
    s: string to incorporate into prompt.
    Return: file_pointer.
    '''
    file_pointer = input("\nInput a {} file: ".format(s))
    while True:
        try:
            file_pointer = open(file_pointer, "r")
            return file_pointer
        except FileNotFoundError:
            print("\nError in opening file.")
            file_pointer = input("\nInput a {} file: ".format(s))
            
def read_names(fp):
    ''' 
    Reads the names.txt file using the file pointer.
    fp: file pointer.
    Returns: list of lists of strings.
    '''
    master_list = []
    for line in fp:
        name = line.strip('\n')
        master_list.append(name)
    return master_list

def read_friends(fp,names_lst):
    ''' 
    Reads the friends.csv file using the file pointer.
    fp: file pointer.
    names_lst: list of strings.
    Returns: list of lists of strings.
    '''
    master_list = []
    for line in fp: 
        line = line.strip()
        line = line.split(',')
        new_list = []
        for var in line:
            if var != '':
                var = int(var)
                name = names_lst[var]
                new_list.append(name)
        master_list.append(new_list)
    return master_list

def create_friends_dict(names_lst,friends_lst):
    '''
    Takes the two lists created in the read_names function and the read_friends function and builds a dictionary.
    names_lst: list of strings.
    friends_lst: list of lists of strings.
    Returns: dictionary.
    '''
    return dict(zip(names_lst,friends_lst))
  
def find_common_friends(name1, name2, friends_dict):
    '''
    Takes two names (strings) and the friends_dict (returned by the create_friends_dict) and returns a set of friends that the two names have in common.
    name1: string.
    name2: string.
    friends_dict: dictionary.
    Returns: set of strings.
    '''
    if name1 in friends_dict:
        name1 = set(friends_dict[name1])
    if name2 in friends_dict:
            name2 = set(friends_dict[name2])
    return (name1 & name2)

def find_max_friends(names_lst, friends_lst):
    '''
    Takes a list of names and the corresponding list of friends and determines who has the most friends.
    names_lst: list of strings.
    friends_lst: list of list of strings.
    Returns: list of strings, int.
    '''
    max_frd = 0 

    for length in friends_lst:
        friends_len = len(length)
        if max_frd <= friends_len:
            max_frd = friends_len

    max_frds = []
    for i, var in enumerate(friends_lst):
        if len(var) == max_frd:
            max_frds.append(names_lst[i])
    my_tuple = (sorted(max_frds), max_frd)
    return my_tuple

def find_max_common_friends(friends_dict):
    '''
    Takes the friends dictionary and finds which pairs of people have the most friends in common.
    friends_dict: dictionary.
    Returns: list of tuples of strings, int.
    '''
    new_dict = {}
    master_list = []
    for name1, value1 in friends_dict.items():
        for name2, value2 in friends_dict.items():
            if name1 in value2 and name2 in value1:
                continue
            if (name2, name1) in new_dict:
                continue 
            if name1 == name2:
                continue 
            common_friends = find_common_friends(name1, name2, friends_dict)
            my_tuple = (name1, name2)
            new_dict[my_tuple] = common_friends
    
    max_num = -1       
    for val in new_dict.values():
        number = len(val)
        if number > max_num:
            max_num = number

    for key, value in new_dict.items():
        if max_num == len(value):
            master_list.append(key)
    return master_list, max_num
    
def find_second_friends(friends_dict):
    '''
    Consider second-order friendships, that is, friends of friends. For each person in the network find the friends of their friends, but don’t include the person’s first order friends or themselves.
    friends_dict: dictionary.
    Returns: dictionary with key a string and value as a set.
    '''
    new_dict = {}
    for key, value in friends_dict.items(): 
        new_dict[key] = set()
        for val in value:
            for frnd in friends_dict[val]:
                new_dict[key].add(frnd)
        new_dict[key].remove(key)
        new_dict[key] -= set(value)

    return new_dict

def find_max_second_friends(seconds_dict):
    '''
    Finding max second-order friends, takes a list of names and the corresponding list of friends and determines who has the most second order friends.
    seconds_dict: dictionary.
    Returns: list of strings, int.
    '''
    master_list = []
    max_num = -1       
    for val in seconds_dict.values():
        number = len(val)
        if number > max_num:
            max_num = number

    for key, value in seconds_dict.items():
        if max_num == len(value):
            master_list.append(key)
    return master_list, max_num

def main():
    print("\nFriend Network\n")
    fp = open_file("names")
    names_lst = read_names(fp)
    fp = open_file("friends")
    friends_lst = read_friends(fp,names_lst)
    friends_dict = create_friends_dict(names_lst,friends_lst)

    print(MENU)
    choice = input("\nChoose an option: ")
    while choice not in "12345":
        print("Error in choice. Try again.")
        choice = input("Choose an option: ")
        
    while choice != '5':

        if choice == "1":
            max_friends, max_val = find_max_friends(names_lst, friends_lst)
            print("\nThe maximum number of friends:", max_val)
            print("People with most friends:")
            for name in max_friends:
                print(name)
                
        elif choice == "2":
            max_names, max_val = find_max_common_friends(friends_dict)
            print("\nThe maximum number of commmon friends:", max_val)
            print("Pairs of non-friends with the most friends in common:")
            for name in max_names:
                print(name)
                
        elif choice == "3":
            seconds_dict = find_second_friends(friends_dict)
            max_seconds, max_val = find_max_second_friends(seconds_dict)
            print("\nThe maximum number of second-order friends:", max_val)
            print("People with the most second_order friends:")
            for name in max_seconds:
                print(name)
                
        elif choice == "4":
            name = input("\nEnter a name: ")
            while True:
                if name in friends_dict: #prompt for a name and print the name’s friends
                    print("\nFriends of {}:".format(name))
                    for val in friends_dict[name]:
                        print(val)
                    break 
                else: #name is not a valid name (not in the list of names), re-prompt until it is a valid name
                    print("\nThe name {} is not in the list.".format(name))
                    name = input("\nEnter a name: ")

        else: 
            print("Shouldn't get here.")
            
        choice = input("\nChoose an option: ")
        while choice not in "12345":
            print("Error in choice. Try again.")
            choice = input("Choose an option: ")

if __name__ == "__main__":
    main()
