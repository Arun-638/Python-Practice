import os

def convert_c_to_txt():
    current_dir = os.getcwd()

    for file_name in os.listdir(current_dir):
        if file_name.endswith(".c"):
            c_path = os.path.join(current_dir, file_name)

            txt_name = file_name.replace(".c", ".txt")
            txt_path = os.path.join(current_dir, txt_name)

            with open(c_path, "r", encoding="utf-8") as c_file:
                content = c_file.read()

            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(content)

            print(f"Converted {file_name} to {txt_name}")

convert_c_to_txt()