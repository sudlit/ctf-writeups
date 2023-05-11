import os

def to_integer(lst):
    if len(lst) == 2:
        return [int(lst[0]), lst[1]]
    return lst

def print_flag(flag):
    if flag:
        with open("flag.txt") as f:
            print(f.read())
    else:
        print("Nope")

def convert_input(string):
    print(to_integer(string.strip().split()))
    return to_integer(string.strip().split())

def check(lst):
    if len(lst) == 2 and lst[1] == "bananas":
        num = lst[0]
        return (num + 5) * 9 - 1 == 971
    return False

def main():
    print_flag(check(convert_input(input("How many bananas do I have?\n"))))

if __name__ == "__main__":
    main()

'''
mix decompile Elixir.Bananas.beam --to erlang
convert ex file to python code
find correct input
input is "103 bananas" and got flag
'''