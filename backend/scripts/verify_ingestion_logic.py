"""
Verification script for Ingestion Logic.
Runs the pipeline on a tiny dataset to ensure no configuration errors (like OpenAI API key missing).
"""
import os
import sys

# Add backend directory to path so we can import project1_rag
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from project1_rag.ingest import IngestionPipeline

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEST_DATA_DIR = os.path.join(BASE_DIR, "data", "dummy_test")
    
    print("--- STARTING LIGHTWEIGHT VERIFICATION ---")
    print(f"Target: {TEST_DATA_DIR}")
    
    # Use a separate collection for testing
    pipeline = IngestionPipeline(data_dir=TEST_DATA_DIR, collection_name="test_verification")
    
    try:
        pipeline.run()
        print("\n✅ VERIFICATION SUCCESSFUL: Pipeline ran without errors.")
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        raise e

if __name__ == "__main__":
    main()

