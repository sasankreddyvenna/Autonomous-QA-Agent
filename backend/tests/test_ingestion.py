# backend/tests/test_ingestion.py
# Simple smoke tests (these are placeholders — adapt to your CI)
def test_imports():
    import services.document_ingestion.pdf_parser
    import services.document_ingestion.html_parser
    import services.embeddings.embedder
    assert True
