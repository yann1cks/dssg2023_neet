import pandas as pd

from src.merge_utils import merge_priority_dfs
from src.file_utils import tmp_path
from src.log_utils import get_logger
from src.data_utils import load_csv
from src.constants import NA_VALS, UNKNOWN_CODES, SchoolInfoColumns


def annotate_ks4(input_path, school_info_path, output_path):
    # Set up logging
    logger = get_logger(name=__name__)

    # Load KS4 dataset
    ks4_df = load_csv(
        input_path,
        drop_empty=False,
        drop_single_valued=False,
        drop_duplicates=False,
        read_as_str=True,
        na_vals=NA_VALS,
        use_na=True,
        logger=logger,
    )

    # Load school info dataset
    school_df = load_csv(
        school_info_path,
        drop_empty=False,
        drop_single_valued=False,
        drop_missing_upns=False,
        drop_duplicates=False,
        read_as_str=True,
        na_vals=NA_VALS,
        use_na=True,
        logger=logger,
    )

    # Merge establishment information into KS4 dataset
    logger.info("Merging establishment information into KS4 dataset")
    ks4_df = merge_priority_dfs(
        [school_df, ks4_df],
        #on=SchoolInfoColumns.la_establishment_number,
        on = ks4_df["LAEstab (anon)"],
        how="right",
        unknown_vals=UNKNOWN_CODES,
        na_vals=NA_VALS,
    )

    # # Select the year from the 'EntryDate' column
    # logger.info("Selecting the year from the 'EntryDate' column")
    # ks4_df["Year"] = pd.to_datetime(ks4_df["EntryDate"], errors="coerce").dt.year

    # Save annotated data to output file
    output_csv = tmp_path(output_path)
    logger.info(f"Saving annotated data to {output_csv}")
    ks4_df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    input_csv = "/home/aims/Documents/NEET PROJECT/NEET-TRIAL/data/KS4/ks4_original_csv/ks4_original_sep15.csv"
    school_info_csv = "/home/aims/Documents/NEET PROJECT/NEET-TRIAL/data/KS4/secondary_schools_original1.csv"
    output_csv = "/home/aims/Documents/NEET PROJECT/NEET-TRIAL/data/KS4/output/ouput.csv"

    annotate_ks4(input_csv, school_info_csv, output_csv)

