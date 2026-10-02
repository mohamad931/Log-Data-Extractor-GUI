import re
import logging
import os
import customtkinter as cs

logging.basicConfig(filename='pro.log', level=logging.DEBUG,
                    format = '%(asctime)s:%(levelname)s: Line %(lineno)d :%(message)s')

def extract_from_file(filepath, output_path='results.txt'):
    unique_numbers = set()
    unique_emails = set()

    logging.info('the programme started ')

    numbers = re.compile(r'09\d{8}')
    emails = re.compile(r'[a-zA-Z0-9.-]+@[a-zA-Z-]+\.\w+')


    try:
        logging.info(f'start reading the file...{filepath}')
        with open(filepath, 'r', encoding='utf-8') as fr:

            for line in fr:

                for number in numbers.finditer(line):
                    unique_numbers.add(number.group())

                for email in emails.finditer(line):
                    unique_emails.add(email.group())

            logging.info(f'start writing in the results file...{filepath}')
            with open(output_path, 'w', encoding='utf-8') as fw:

                fw.write('* Emails : \n')
                for email in sorted(unique_emails):
                    fw.write(email + "\n")
                    #fw.write("\n")

                fw.write('* Numbers : \n')
                for number in sorted(unique_numbers):
                    fw.write(number + "\n")
                    #fw.write("\n")
                fw.write(f"extract {len(unique_numbers)} Number.\n")
                fw.write(f"extract {len(unique_emails)} email.")

            logging.info('the programme end successfully')
            return True,f"Success! Extracted {len(unique_numbers)} numbers and {len(unique_emails)} emails.\nResults in new results.txt file in your file director"

    except FileNotFoundError:
        logging.error("this file you entered not found")
        return False,"file not found"
    except PermissionError:
        logging.error("you don't have Permission to this file")
        return False,"you don't have permission"
    except UnicodeDecodeError:
        logging.error("error in decode the file")
        return False,"error in decode the file"


def main():

    cs.set_appearance_mode("system")
    cs.set_default_color_theme("dark-blue")

    root = cs.CTk()
    root.geometry("700x500")

    frame = cs.CTkFrame(master=root)
    frame.pack(pady=40, padx=60, fill="both", expand=True)

    label = cs.CTkLabel(master=frame, text="Log Data Extractor", font=("Roboto", 24, "bold"))
    label.pack(pady=20, padx=18)

    entry1 = cs.CTkEntry(master=frame, placeholder_text="Enter file path here", width=400)
    entry1.pack(pady=15, padx=18)


    def browse_file():

        file_selected = cs.filedialog.askopenfilename()
        if file_selected:
            entry1.delete(0, 'end')
            entry1.insert(0, file_selected)


    browse_btn = cs.CTkButton(master=frame, text='Browse File', command=browse_file, border_width=1)
    browse_btn.pack(pady=5)

    status_label = cs.CTkLabel(master=frame, text="", font=("Roboto", 14))


    def start_extraction():

        filepath = entry1.get().strip().strip('"')
        if not filepath:
            status_label.configure(text="Please enter a file path first!", text_color="orange")
            return

        if os.path.exists(filepath):
            success, message = extract_from_file(filepath)
            if success:
                status_label.configure(text=message, text_color="green")
            else:
                status_label.configure(text=message, text_color="red")
        else:
            status_label.configure(text="File does not exist, chek the path!", text_color="red")

    button = cs.CTkButton(master=frame, text="Extract", command=start_extraction)
    button.pack(pady=15, padx=18)
    status_label.pack(pady=15, padx=18)

    root.mainloop()

if __name__ == '__main__':
    main()
