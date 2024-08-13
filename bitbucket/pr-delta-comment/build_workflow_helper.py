from your_script_name import extract_content

filename = "example.txt"
content = extract_content(filename)
if content is not None:
    print(content)

def post_comment():
    # Define method one logic
    print("Method One executed")

def delta_summary():
    filename = "example.txt"
    content = extract_content(filename)
    if content is not None:
        print(content)

def main(option):
    if option == 'comment':
        post_comment()
    elif option == 'delta':
        delta_summary()
    else:
        print("Invalid option")

if __name__ == "__main__":
    option = input("Enter option (1 or 2): ")
    main(option)