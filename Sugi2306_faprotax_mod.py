from scripts.FAPROTAX import FaprotaxRunner

# convert OTU table to functional table using FAPROTAX
runner = FaprotaxRunner()
result = runner.collapse_table(
    input_table=r"data\faprotax_input_mod.tsv",
    output_table=r"data\faprotax_output_mod.tsv",
    output_report=r"data\faprotax_report_mod.txt",
    # No header for the first column; use index-based row names
    column_names_in='none',
    verbose=True,
    additional_args=[
        # First column holds taxonomy row names
        '--row_names_are_in_column', '0',
        '--group_members_defined_as', 'words',
        '--valid_word_symbols', '_-',
        # case-insensitive matching to maximize genus hits
        # (do not pass --case_sensitive flag)
    ]
)