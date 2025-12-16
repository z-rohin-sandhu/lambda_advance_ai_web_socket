import sys
import os

print(f"[bootstrap] Initializing module: file={__file__}")
base_dir = os.path.dirname(os.path.abspath(__file__))
print(f"[bootstrap] Adding to sys.path: {base_dir}")
sys.path.append(base_dir)

print("[bootstrap] Importing src.handler.lambda_handler")
from src.handler import lambda_handler
print("[bootstrap] Import complete: lambda_handler ready")
