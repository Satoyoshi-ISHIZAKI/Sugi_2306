"""
Wrapper functions for FAPROTAX collapse_table.py

Python interface for easy use of FAPROTAX functional annotation tool
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, List

# Load FAPROTAX path from config file
try:
    from scripts.config import FAPROTAX_DIR
except ImportError:
    # Default value if config.py is not found
    FAPROTAX_DIR = None
    print("Warning: scripts/config.py not found.")
    print("Please copy scripts/config.example.py to scripts/config.py and")
    print("set FAPROTAX_DIR.")


class FaprotaxRunner:
    """Class for executing FAPROTAX collapse_table.py"""
    
    def __init__(self, faprotax_dir: str = None):
        """
        Parameters:
        -----------
        faprotax_dir : str
            Path to the directory where FAPROTAX is installed
            If None, read from config.py
        """
        if faprotax_dir is None:
            if FAPROTAX_DIR is None:
                raise ValueError(
                    "FAPROTAX_DIR is not configured.\n"
                    "Either specify directly with FaprotaxRunner(faprotax_dir='path'), or\n"
                    "set FAPROTAX_DIR in scripts/config.py."
                )
            faprotax_dir = FAPROTAX_DIR
        self.faprotax_dir = Path(faprotax_dir)
        self.collapse_table_script = self.faprotax_dir / "collapse_table.py"
        self.database_file = self.faprotax_dir / "FAPROTAX.txt"
        
        if not self.collapse_table_script.exists():
            raise FileNotFoundError(f"collapse_table.py not found: {self.collapse_table_script}")
    
    def collapse_table(self,
                      input_table: str,
                      output_table: str,
                      output_report: Optional[str] = None,
                      groups_file: Optional[str] = None,
                      group_leftovers_as: str = 'other',
                      normalize: str = 'columns_after_collapsing',
                      column_names_in: str = 'first_data_line',
                      verbose: bool = True,
                      additional_args: Optional[List[str]] = None) -> subprocess.CompletedProcess:
        """
        Convert OTU table to functional groups
        
        Parameters:
        -----------
        input_table : str
            Path to input OTU table (.tsv, .csv, .biom, etc.)
        output_table : str
            Path to output functional table
        output_report : str, optional
            Path to report file
        groups_file : str, optional
            Group definition file (default is FAPROTAX.txt)
        group_leftovers_as : str
            How to handle unassigned OTUs (default: 'other')
        normalize : str
            Normalization method (default: 'columns_after_collapsing')
        column_names_in : str
            Location of column names (default: 'first_data_line')
        verbose : bool
            Display verbose output
        additional_args : List[str], optional
            Additional command line arguments
        
        Returns:
        --------
        subprocess.CompletedProcess
            Execution result
        
        Example:
        -------
        runner = FaprotaxRunner()
        result = runner.collapse_table(
            input_table='otu_table.tsv',
            output_table='functional_table.tsv',
            output_report='report.txt'
        )
        """
        if groups_file is None:
            groups_file = str(self.database_file)
        
        # Build command
        # Add -X utf8 option to force Python to use UTF-8 encoding
        cmd = [
            sys.executable,  # Use current Python interpreter
            '-X', 'utf8',     # Force UTF-8 mode to avoid encoding issues
            str(self.collapse_table_script),
            '-i', input_table,
            '-o', output_table,
            '-g', groups_file,
            '--group_leftovers_as', group_leftovers_as,
            '--normalize_collapsed', normalize,
            '--column_names_are_in', column_names_in
        ]
        
        if output_report:
            cmd.extend(['-r', output_report])
        
        if verbose:
            cmd.append('-v')
        
        if additional_args:
            cmd.extend(additional_args)
        
        # Execute
        print(f"Running: {' '.join(cmd)}")
        
        # Set environment variable to force UTF-8 encoding
        import os
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'  # Force Python to use UTF-8
        
        # Adjust encoding for Windows environment
        # Use errors='replace' to avoid decode errors
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',   # Use UTF-8
            errors='replace',   # Replace decode errors with ?
            env=env             # Pass environment with PYTHONUTF8
        )
        
        if result.returncode == 0:
            print(f"✓ Success: Created {output_table}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"✗ Error occurred:")
            print(result.stderr)
        
        return result


def run_faprotax_simple(input_file: str, 
                       output_file: str, 
                       report_file: Optional[str] = None) -> bool:
    """
    Run FAPROTAX with simplest interface
    
    Parameters:
    -----------
    input_file : str
        Path to input OTU table
    output_file : str
        Path to output file
    report_file : str, optional
        Path to report output file
    
    Returns:
    --------
    bool
        Whether execution was successful
    
    Example:
    -------
    run_faprotax_simple('my_otu_table.tsv', 'functional_output.tsv', 'report.txt')
    """
    try:
        runner = FaprotaxRunner()
        result = runner.collapse_table(
            input_table=input_file,
            output_table=output_file,
            output_report=report_file
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False


# Usage examples
if __name__ == '__main__':
    # Example 1: Detailed execution using class
    print("=== Example 1: Detailed configuration ===")
    runner = FaprotaxRunner()
    
    # Change to appropriate file paths when actually using
    # result = runner.collapse_table(
    #     input_table='data/otu_table.tsv',
    #     output_table='output/functional_table.tsv',
    #     output_report='output/report.txt',
    #     verbose=True
    # )
    
    # Example 2: Simple execution
    print("\n=== Example 2: Simple execution ===")
    # success = run_faprotax_simple(
    #     'data/otu_table.tsv',
    #     'output/functional_table.tsv',
    #     'output/report.txt'
    # )
    
    print("\nUsage:")
    print("1. Use FaprotaxRunner class for detailed configuration")
    print("2. Use run_faprotax_simple() function for simple execution")
    print("\nPrepare input files and enable the commented lines above.")
# Use functions in collapse_table
# Example: collapse_table.main() or call specific functions