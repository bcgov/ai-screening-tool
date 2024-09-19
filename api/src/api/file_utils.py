"""Batch Resume PDF Splitter

Splits a single PDF containing a batch of resumes into multiple PDF's.
"""

from io import BytesIO
import re
from typing import IO, Generator

from docx import Document
from PyPDF2 import PageObject, PdfReader, PdfWriter

begin_keyword = "Resume Profile"
end_keyword = "If you have any questions,"


def extract_texts_from_resume_batch(batch_pdf_file: IO) -> Generator[str, None, None]:
    for start_page_num, end_page_num in split_resumes(batch_pdf_file):
        with BytesIO() as single_pdf_file:
            pdf_reader = PdfReader(batch_pdf_file)
            pdf_writer = PdfWriter()

            for i in range(start_page_num, end_page_num + 1):
                pdf_writer.add_page(pdf_reader.pages[i])

            pdf_writer.write(single_pdf_file)

            yield extract_text_from_pdf(single_pdf_file)


def split_resumes(
    batch_pdf_file: IO,
) -> Generator[tuple[int, int], None, None]:
    total_num_of_begin = 0
    total_num_of_end = 0

    pdf = PdfReader(batch_pdf_file)

    found_resume = False

    start_page_num = -1
    end_page_num = -1

    for page_obj in pdf.pages:
        page_content = page_obj.extract_text()

        if re.search(begin_keyword, page_content):
            total_num_of_begin += 1
            start_page_num = PdfReader.get_page_number(self=pdf, page=page_obj)
            found_resume = False

        if re.search(end_keyword, page_content):
            total_num_of_end += 1
            end_page_num = PdfReader.get_page_number(self=pdf, page=page_obj)
            found_resume = True

        if found_resume:
            yield start_page_num, end_page_num

            found_resume = False

    if total_num_of_begin != total_num_of_end:
        raise ValueError(
            "The number of start line detected does not match the end line detected! Corrupted files were generated.\n"
            + "total_num_of_begin: "
            + str(total_num_of_begin)
            + "total_num_of_end: "
            + str(total_num_of_end)
        )


def extract_text_from_pdf(file: IO) -> str:
    return "\n".join(map(PageObject.extract_text, PdfReader(file).pages)) + "\n"


def extract_text_from_docx(file: IO) -> str:
    return "\n".join(p.text for p in Document(file).paragraphs)
