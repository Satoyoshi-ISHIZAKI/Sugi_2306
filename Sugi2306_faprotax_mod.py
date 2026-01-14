from scripts.FAPROTAX import FaprotaxRunner

# convert OTU table to functional table using FAPROTAX
runner = FaprotaxRunner()
result = runner.collapse_table(
    input_table=r"data\faprotax_input_mod.tsv",
    output_table=r"data\mod\faprotax_output_mod.tsv",
    output_report=r"data\mod\faprotax_report_mod.txt",
    # No header for the first column; use index-based row names
    column_names_in='none',
    verbose=True,
    additional_args=[
        '--out_sub_tables_dir', r"data\mod\sub_tables_mod.tsv",
        '--out_groups2records_table', r"data\mod\groups2otus_mod.tsv",
        '--out_group_overlaps', r"data\mod\group_overlaps_mod.tsv",
        '--normalize_collapsed', 'none',
        # First column holds taxonomy row names
        '--row_names_are_in_column', '0',
        '--group_members_defined_as', 'words',
        '--valid_word_symbols', '_-',
        # case-insensitive matching to maximize genus hits
        # (do not pass --case_sensitive flag)
    ]
)