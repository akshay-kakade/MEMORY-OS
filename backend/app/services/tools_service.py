import fitz  # PyMuPDF
from tavily import TavilyClient
from app.core.config import settings
import io

class ToolsService:
    def __init__(self):
        self.tavily = None
        if settings.TAVILY_API_KEY:
            self.tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search_web(self, query: str):
        if not self.tavily:
            return "Web search is not configured (TAVILY_API_KEY missing)."
        
        search_result = self.tavily.search(query=query, search_depth="advanced")
        context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in search_result['results']])
        return context

    def extract_text_from_pdf(self, pdf_bytes: bytes):
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

tools_service = ToolsService()
