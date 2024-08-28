import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import csv
import json
import pandas as pd
import sqlite3

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper Pro")
        self.root.configure(bg="#eaedfa")  # Set the background color

        # GUI Components
        self.url_label = tk.Label(root, text="Website URL:", bg="#eaedfa")
        self.url_entry = tk.Entry(root, width=50)
        self.method_label = tk.Label(root, text="Scraping Method:", bg="#eaedfa")
        self.method_var = tk.StringVar(value="BeautifulSoup")
        self.method_menu = tk.OptionMenu(root, self.method_var, "BeautifulSoup", "Selenium")
        self.output_label = tk.Label(root, text="Output Format:", bg="#eaedfa")
        self.output_var = tk.StringVar(value="CSV")
        self.output_menu = tk.OptionMenu(root, self.output_var, "CSV", "Excel", "SQL", "JSON")
        self.scrape_button = tk.Button(root, text="Scrape Data", command=self.scrape_data)

        # Nested tags frame
        self.nested_tags_frame = tk.Frame(root, bg="#eaedfa")
        self.nested_tags_label = tk.Label(self.nested_tags_frame, text="Nested Tags:", bg="#eaedfa")
        self.p_var = tk.IntVar(value=1)
        self.h1_var = tk.IntVar(value=0)
        self.h2_var = tk.IntVar(value=0)
        self.div_var = tk.IntVar(value=0)
        self.a_var = tk.IntVar(value=0)
        self.class_var = tk.IntVar(value=0)
        self.id_var = tk.IntVar(value=0)
        self.td_var = tk.IntVar(value=0)
        self.tr_var = tk.IntVar(value=0)

        self.p_check = tk.Checkbutton(self.nested_tags_frame, text="Paragraphs (<p>)", variable=self.p_var, bg="#eaedfa")
        self.h1_check = tk.Checkbutton(self.nested_tags_frame, text="Headings 1 (<h1>)", variable=self.h1_var, bg="#eaedfa")
        self.h2_check = tk.Checkbutton(self.nested_tags_frame, text="Headings 2 (<h2>)", variable=self.h2_var, bg="#eaedfa")
        self.div_check = tk.Checkbutton(self.nested_tags_frame, text="Divisions (<div>)", variable=self.div_var, bg="#eaedfa")
        self.a_check = tk.Checkbutton(self.nested_tags_frame, text="Links (<a>)", variable=self.a_var, bg="#eaedfa")
        self.class_check = tk.Checkbutton(self.nested_tags_frame, text="Classes", variable=self.class_var, bg="#eaedfa")
        self.id_check = tk.Checkbutton(self.nested_tags_frame, text="IDs", variable=self.id_var, bg="#eaedfa")
        self.td_check = tk.Checkbutton(self.nested_tags_frame, text="Table Data (<td>)", variable=self.td_var, bg="#eaedfa")
        self.tr_check = tk.Checkbutton(self.nested_tags_frame, text="Table Rows (<tr>)", variable=self.tr_var, bg="#eaedfa")

        # Custom scraping with Selenium
        self.custom_label = tk.Label(root, text="Find Elements:", bg="#eaedfa")
        self.custom_method_var = tk.StringVar(value="find_elements_by_class_name")
        self.custom_method_menu = tk.OptionMenu(root, self.custom_method_var, 
                                                "find_elements_by_class_name",
                                                "find_elements_by_css_selector",
                                                "find_elements_by_id",
                                                "find_elements_by_link_text",
                                                "find_elements_by_name",
                                                "find_elements_by_partial_link_text",
                                                "find_elements_by_tag_name",
                                                "find_elements_by_xpath",
                                                "find_elements")
        
        self.instructions_label = tk.Label(root, text="Input an Expression:", bg="#eaedfa")
        self.custom_expr_entry = tk.Entry(root, width=50)

        # Layout
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.url_entry.grid(row=0, column=1, padx=12, pady=10, sticky='w')
        self.method_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.method_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.output_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.output_menu.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.nested_tags_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.nested_tags_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        self.p_check.grid(row=0, column=1, padx=5, sticky='w')
        self.h1_check.grid(row=0, column=2, padx=5, sticky='w')
        self.h2_check.grid(row=0, column=3, padx=5, sticky='w')
        self.div_check.grid(row=1, column=1, padx=5, sticky='w')
        self.a_check.grid(row=1, column=2, padx=5, sticky='w')
        self.class_check.grid(row=1, column=3, padx=5, sticky='w')
        self.id_check.grid(row=2, column=1, padx=5, sticky='w')
        self.td_check.grid(row=2, column=2, padx=5, sticky='w')
        self.tr_check.grid(row=2, column=3, padx=5, sticky='w')

        self.custom_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.custom_method_menu.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        self.instructions_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='w')
        self.custom_expr_entry.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='w')

        self.scrape_button.grid(row=7, column=0, columnspan=4, pady=20)

    def scrape_data(self):
        url = self.url_entry.get()
        method = self.method_var.get()
        output_format = self.output_var.get()

        # Define which tags to scrape
        selected_tags = []
        if self.p_var.get() == 1:
            selected_tags.append('p')
        if self.h1_var.get() == 1:
            selected_tags.append('h1')
        if self.h2_var.get() == 1:
            selected_tags.append('h2')
        if self.div_var.get() == 1:
            selected_tags.append('div')
        if self.a_var.get() == 1:
            selected_tags.append('a')
        if self.class_var.get() == 1:
            selected_tags.append('class')
        if self.id_var.get() == 1:
            selected_tags.append('id')
        if self.td_var.get() == 1:
            selected_tags.append('td')
        if self.tr_var.get() == 1:
            selected_tags.append('tr')

        custom_method = self.custom_method_var.get()
        custom_expr = self.custom_expr_entry.get()

        if method == "BeautifulSoup":
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            extracted_data = []

            for tag in selected_tags:
                if tag in ['class', 'id']:
                    elements = soup.find_all(attrs={tag: True})
                else:
                    elements = soup.find_all(tag)
                for element in elements:
                    extracted_data.append(element.get_text())

        elif method == "Selenium":
            chrome_options = Options()
            chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            service = Service(executable_path="C:\\webdrivers\\chromedriver.exe")  # Path to the updated ChromeDriver
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            extracted_data = []

            if custom_expr:
                # Use the custom expression entered by the user
                elements = getattr(driver, custom_method)(custom_expr)
                for element in elements:
                    extracted_data.append(element.text)
            else:
                # Use the standard tag-based selection
                for tag in selected_tags:
                    if tag in ['class', 'id']:
                        elements = soup.find_all(attrs={tag: True})
                    else:
                        elements = soup.find_all(tag)
                    for element in elements:
                        extracted_data.append(element.get_text())

            driver.quit()

        self.save_data(extracted_data, output_format)

    def save_data(self, data, output_format):
        if output_format == "CSV":
            with open(filedialog.asksaveasfilename(defaultextension=".csv"), 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow([row])

        elif output_format == "Excel":
            df = pd.DataFrame(data, columns=["Data"])
            df.to_excel(filedialog.asksaveasfilename(defaultextension=".xlsx"), index=False)

        elif output_format == "SQL":
            conn = sqlite3.connect(filedialog.asksaveasfilename(defaultextension=".db"))
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS ScrapedData (Data TEXT)")
            for row in data:
                cursor.execute("INSERT INTO ScrapedData (Data) VALUES (?)", (row,))
            conn.commit()
            conn.close()

        elif output_format == "JSON":
            with open(filedialog.asksaveasfilename(defaultextension=".json"), 'w', encoding='utf-8') as file:
                json.dump(data, file)

        messagebox.showinfo("Success", "Data saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    WebScraperApp(root)
    root.mainloop()