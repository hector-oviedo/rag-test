"""
Configuration settings for the RAG engine.
"""

# Context Cleaning
# Set to True to strip HTML tags from retrieved nodes before passing to LLM.
# Set to False to pass raw content (useful if LLM handles HTML well or for debugging).
CLEAN_HTML_CONTEXT = True
