import os
import sys

# Add the parent directory to sys.path to ensure test modules can import the main package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
