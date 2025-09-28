"""
Tests for file management modules.
"""

import pytest
from pathlib import Path
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_management.csv_to_excel import csv_to_excel
from file_management.excel_to_csv import excel_to_csv
from file_management.csv_to_json import csv_to_json
from file_management.json_to_csv import json_to_csv
from file_management.merge_pdf import merge_pdf


class TestCSVToExcel:
    """Test CSV to Excel conversion."""
    
    def test_csv_to_excel_success(self, sample_csv, temp_dir):
        """Test successful CSV to Excel conversion."""
        output_file = temp_dir / "converted.xlsx"
        csv_to_excel(sample_csv, output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.xlsx'
        
        # Verify the Excel file can be read
        df = pd.read_excel(output_file)
        assert len(df) > 0
    
    def test_csv_to_excel_default_output(self, sample_csv):
        """Test CSV to Excel conversion with default output path."""
        csv_to_excel(sample_csv)
        
        expected_output = sample_csv.with_suffix('.xlsx')
        assert expected_output.exists()
    
    def test_csv_to_excel_invalid_input(self, invalid_file):
        """Test CSV to Excel conversion with invalid input."""
        with pytest.raises(Exception):  # Should raise an exception
            csv_to_excel(invalid_file)


class TestExcelToCSV:
    """Test Excel to CSV conversion."""
    
    def test_excel_to_csv_success(self, sample_excel, temp_dir):
        """Test successful Excel to CSV conversion."""
        output_file = temp_dir / "converted.csv"
        excel_to_csv(sample_excel, output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.csv'
        
        # Verify the CSV file can be read
        df = pd.read_csv(output_file)
        assert len(df) > 0
    
    def test_excel_to_csv_default_output(self, sample_excel):
        """Test Excel to CSV conversion with default output path."""
        excel_to_csv(sample_excel)
        
        expected_output = sample_excel.with_suffix('.csv')
        assert expected_output.exists()


class TestCSVToJSON:
    """Test CSV to JSON conversion."""
    
    def test_csv_to_json_success(self, sample_csv, temp_dir):
        """Test successful CSV to JSON conversion."""
        output_file = temp_dir / "converted.json"
        csv_to_json(sample_csv, output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.json'
        
        # Verify the JSON file can be read
        import json
        with open(output_file, 'r') as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_csv_to_json_default_output(self, sample_csv):
        """Test CSV to JSON conversion with default output path."""
        csv_to_json(sample_csv)
        
        expected_output = sample_csv.with_suffix('.json')
        assert expected_output.exists()


class TestJSONToCSV:
    """Test JSON to CSV conversion."""
    
    def test_json_to_csv_success(self, sample_json, temp_dir):
        """Test successful JSON to CSV conversion."""
        output_file = temp_dir / "converted.csv"
        json_to_csv(sample_json, output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.csv'
        
        # Verify the CSV file can be read
        df = pd.read_csv(output_file)
        assert len(df) > 0
    
    def test_json_to_csv_default_output(self, sample_json):
        """Test JSON to CSV conversion with default output path."""
        json_to_csv(sample_json)
        
        expected_output = sample_json.with_suffix('.csv')
        assert expected_output.exists()


class TestMergePDF:
    """Test PDF merging functionality."""
    
    def test_merge_pdf_success(self, sample_pdf, temp_dir):
        """Test successful PDF merging."""
        # Create a copy of the sample PDF for merging
        pdf_copy = temp_dir / "copy.pdf"
        pdf_copy.write_bytes(sample_pdf.read_bytes())
        
        output_file = temp_dir / "merged.pdf"
        merge_pdf([sample_pdf, pdf_copy], output_file)
        
        assert output_file.exists()
        assert output_file.suffix.lower() == '.pdf'
    
    def test_merge_pdf_default_output(self, sample_pdf, temp_dir):
        """Test PDF merging with default output path."""
        # Create a copy of the sample PDF for merging
        pdf_copy = temp_dir / "copy.pdf"
        pdf_copy.write_bytes(sample_pdf.read_bytes())
        
        merge_pdf([sample_pdf, pdf_copy])
        
        # Check that a merged file was created (with timestamp in name)
        merged_files = list(temp_dir.glob("*merged.pdf"))
        assert len(merged_files) > 0
    
    def test_merge_pdf_invalid_input(self, invalid_file):
        """Test PDF merging with invalid input."""
        with pytest.raises(Exception):  # Should raise an exception
            merge_pdf([invalid_file])
