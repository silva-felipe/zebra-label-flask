from pypdf import PdfWriter
import pdb

def merge_pdf(batch_files_pdf, now):
    batch_files_pdf = batch_files_pdf[0]

    """
    Merge a list of PDF file paths into a single PDF file.

    Args:
    - batch_files_pdf (list): List of paths to PDF files.
    - now (int): Timestamp used to name the output file.

    Output:
    - Saves the merged PDF file to the `zebras_pdf` directory.
    """
    merger = PdfWriter()
    for file_path in batch_files_pdf:
        # Ensure the file_path is a valid string or path object
        merger.append(file_path)

    output_path = f"zebras_pdf/{now}_zebra_labels.pdf"
    merger.write(output_path)
    merger.close()
    return output_path