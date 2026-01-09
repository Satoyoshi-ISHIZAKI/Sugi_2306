from scripts.FAPROTAX import FaprotaxRunner

# convert OTU table to functional table using FAPROTAX
runner = FaprotaxRunner()
result = runner.collapse_table(
    input_table=r"data\faprotax_input.tsv",
    output_table=r"data\faprotax_output.tsv",
    output_report=r"data\faprotax_report.txt",
    column_names_in='first_data_line',
    verbose=True,
    additional_args=[
        '--row_names_are_in_column', 'taxonomy',
        '--omit_columns', '0',  # Skip the first column (row numbers)
        '--group_members_defined_as', 'words',
        '--case_sensitive'
    ]
)