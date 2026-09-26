from pypdf import PdfReader
import io

from utils.s3_client import list_files, read_bytes


class PDFRetriever:

    def search(
        self,
        keyword
    ):

        results = []

        pdf_folder = "data/pdfs"

        for file in list_files(pdf_folder, suffix=".pdf"):

            try:

                reader = PdfReader(
                    io.BytesIO(read_bytes(f"{pdf_folder}/{file}"))
                )

                content = ""

                for page in reader.pages:

                    content += (
                        page.extract_text()
                        or ""
                    )

                if keyword.lower() in \
                   content.lower():

                    results.append({

                        "file": file,

                        "match": keyword,

                        "snippet":
                        content[:500]

                    })

            except Exception as e:

                print(
                    f"Error {file}: {e}"
                )

        return results