import fitz  # PyMuPDF
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract

# Ensure pytesseract is installed and properly configured
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary

# Function to convert PDF to JPEG images
def pdf_to_jpeg(pdf_path, output_folder):
    try:
        # Get the PDF file name without extension
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # Create a new folder for each PDF file in the output directory
        pdf_output_folder = os.path.join(output_folder, pdf_name)
        if not os.path.exists(pdf_output_folder):
            os.makedirs(pdf_output_folder)
        
        # Open the PDF
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap(dpi=300)
            output_path = os.path.join(pdf_output_folder, f'{pdf_name}_page_{page_number + 1}.jpeg')
            pix.save(output_path)
            print(f"Saved: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to convert JPEG images to text and save to a TXT file
def jpegs_to_txt(images_folder, output_txt_path):
    try:
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            # Get all JPEG files in the folder
            image_files = [f for f in os.listdir(images_folder) if f.endswith('.jpeg') or f.endswith('.jpg')]
            image_files.sort()
            
            for img in image_files:
                img_path = os.path.join(images_folder, img)
                # Use Tesseract to extract text from the image
                text = pytesseract.image_to_string(Image.open(img_path))
                 # Write the extracted text to the TXT file
                txt_file.write(f"Text from {img}:\n")
                txt_file.write(text)
                txt_file.write("\n\n")
            print(f"TXT file saved: {output_txt_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to convert all folders in a given directory to TXT files automatically with text extraction
def convert_all_folders_to_txts(parent_folder):
    try:
        # Iterate through all folders in the parent directory
        for folder_name in os.listdir(parent_folder):
            folder_path = os.path.join(parent_folder, folder_name)
            if os.path.isdir(folder_path):
                # Create a TXT file from all JPEG images in the folder
                output_txt_path = os.path.join(folder_path, f'{folder_name}.txt')
                jpegs_to_txt(folder_path, output_txt_path)
        messagebox.showinfo("Success", "All JPEG folders converted to TXT files successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to combine all TXT files into one large TXT file
def combine_txt_files(parent_folder):
    try:
        combined_txt_path = os.path.join(parent_folder, 'combined_output.txt')
        with open(combined_txt_path, 'w', encoding='utf-8') as combined_file:
            for folder_name in os.listdir(parent_folder):
                folder_path = os.path.join(parent_folder, folder_name)
                if os.path.isdir(folder_path):
                    for txt_file_name in os.listdir(folder_path):
                        if txt_file_name.endswith('.txt'):
                            txt_file_path = os.path.join(folder_path, txt_file_name)
                            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                                combined_file.write(txt_file.read())
                                combined_file.write("\n\n")
        messagebox.showinfo("Success", "All TXT files combined into one large TXT file successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Main function to create the GUI
def main():
    # Create the main window
    root = tk.Tk()
    root.title("PDF to JPEG Converter and JPEG to TXT Converter")
    root.geometry("400x550")
    
    # Function to select the PDF folder
    def select_pdf_folder():
        pdf_folder.set(filedialog.askdirectory())
    
    # Function to select the PDF file
    def select_pdf():
        pdf_path.set(filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")]))
    
    # Function to select the output folder
    def select_output_folder():
        output_folder.set(filedialog.askdirectory())
    
    # Function to select the parent folder containing JPEG folders
    def select_parent_folder():
        parent_folder.set(filedialog.askdirectory())
    
    # Function to start the PDF to JPEG conversion process
    def start_pdf_to_jpeg_conversion():
        if pdf_folder.get():
            for file in os.listdir(pdf_folder.get()):
                if file.endswith(".pdf"):
                    pdf_to_jpeg(os.path.join(pdf_folder.get(), file), output_folder.get())
            messagebox.showinfo("Success", "All PDF to JPEG conversions completed successfully.")
        elif pdf_path.get() and output_folder.get():
            pdf_to_jpeg(pdf_path.get(), output_folder.get())
            messagebox.showinfo("Success", "PDF to JPEG conversion completed successfully.")
        else:
            messagebox.showwarning("Warning", "Please select either a PDF folder, a PDF file, and an output folder.")
    
    # Function to start the process of converting all JPEG folders to TXT files
    def start_convert_all_folders_to_txts():
        if parent_folder.get():
            convert_all_folders_to_txts(parent_folder.get())
        else:
            messagebox.showwarning("Warning", "Please select a folder containing JPEG folders.")
    
    # Function to start combining all TXT files into one
    def start_combine_txt_files():
        if parent_folder.get():
            combine_txt_files(parent_folder.get())
        else:
            messagebox.showwarning("Warning", "Please select a folder containing TXT files.")
    
    # Variables to store file paths
    pdf_path = tk.StringVar()
    output_folder = tk.StringVar()
    pdf_folder = tk.StringVar()
    parent_folder = tk.StringVar()
    
    # PDF to JPEG section
    tk.Label(root, text="PDF to JPEG Conversion").pack(pady=5)
    tk.Button(root, text="Select PDF File", command=select_pdf).pack(pady=5)
    tk.Entry(root, textvariable=pdf_path, width=50).pack()
    tk.Button(root, text="Select PDF Folder", command=select_pdf_folder).pack(pady=5)
    tk.Entry(root, textvariable=pdf_folder, width=50).pack()
    tk.Button(root, text="Select Output Folder", command=select_output_folder).pack(pady=5)
    tk.Entry(root, textvariable=output_folder, width=50).pack()
    tk.Button(root, text="Convert PDF to JPEG", command=start_pdf_to_jpeg_conversion).pack(pady=20)
    
    # JPEG to TXT section
    tk.Label(root, text="Convert All JPEG Folders to TXT").pack(pady=10)
    tk.Button(root, text="Select Parent Folder of JPEG Folders", command=select_parent_folder).pack(pady=5)
    tk.Entry(root, textvariable=parent_folder, width=50).pack()
    tk.Button(root, text="Convert All Folders to TXT", command=start_convert_all_folders_to_txts).pack(pady=20)
    
    # Combine TXT files section
    tk.Label(root, text="Combine All TXT Files into One").pack(pady=10)
    tk.Button(root, text="Combine All TXT Files", command=start_combine_txt_files).pack(pady=10)
    
    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()