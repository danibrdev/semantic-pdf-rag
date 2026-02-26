from pypdf import PdfReader
from domain.ports.pdf_loader_port import PDFLoaderPort


class PDFLoader(PDFLoaderPort):

    def load(self, path: str) -> str:
        reader = PdfReader(path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

        return text