### Census preparation without dvc pipeline
import pandas as pd
import argparse
from src.constants import UNKNOWN_CODES, NA_VALS, CensusDataColumns
from src import merge_utils as mu
from src import file_utils as f
from src import log_utils as l
from src import data_utils as d
from src import py_utils as py

def merged_census_validation(df):
    assert not d.isna(df[CensusDataColumns.data_date], na_vals=NA_VALS).any(), \
        f"Some data dates are missing. Please check the input census file and ensure there are no entries with value {NA_VALS} in the data_date column. Then check the merge_data script for any bugs."
    try:
        pd.to_datetime(df[CensusDataColumns.data_date], errors="raise")
    except ValueError as e:
        print(
            f"There was an error in parsing the data_date column. Please check the entries for any malformed dates. This may be a bug in the merge_data script."
        )
        raise e
    fsme_values = set(df[CensusDataColumns.fsme_on_census_day].str.lower().unique())
    fsme_values_expected = {"false", "true"}
    assert (
        fsme_values == fsme_values_expected
    ), f"fsme_on_census_day has extra values {fsme_values - fsme_values_expected} when lower-cased. Only  values {fsme_values_expected} are allowed. Please correct."


def annotate_school_census(input_file, school_info_file, output_file, debug=False):
    logger = l.get_logger(name=f.get_canonical_filename(__file__), debug=debug)

    df = d.load_csv(
        input_file,
        drop_empty=False,
        drop_single_valued=False,
        drop_duplicates=False,
        read_as_str=True,
        na_vals=NA_VALS,
        use_na=True,
        logger=logger,
    )
    logger.info("Doing some validation on the incoming merged census df")
    merged_census_validation(df)

    school_df = d.load_csv(
        school_info_file,
        drop_empty=False,
        drop_single_valued=False,
        drop_missing_upns=False,
        drop_duplicates=False,
        read_as_str=True,
        na_vals=NA_VALS,
        use_na=True,
        logger=logger,
    )

    logger.info(f"Initial row count {len(df)}")
    logger.info(f"Initial column count {len(df.columns)}")

    logger.info(f"Merging establishment information into census")
    df = mu.merge_priority_dfs(
        [school_df, df],  # The school df is the higher priority information
        on=CensusDataColumns.establishment_number,
        how="right",
        unknown_vals=UNKNOWN_CODES,
        na_vals=NA_VALS,
    )
    logger.info(f"Adding column for end_year of school term")
    df[CensusDataColumns.census_period_end] = pd.to_datetime(
        df[CensusDataColumns.data_date], errors="raise"
    )
    df[CensusDataColumns.year] = (
        df[CensusDataColumns.census_period_end]
        .apply(lambda x: x.year)
        .astype(pd.Int16Dtype())
    )
    logger.info(f"Removing + at the end of ages")
    df[CensusDataColumns.age] = (
        df[CensusDataColumns.age]
        .apply(lambda x: py.remove_suffix(x, "+"))
        .astype(pd.Int16Dtype())
    )

    logger.info(
        f"Converting census column {CensusDataColumns.fsme_on_census_day} to a binary column"
    )
    # There shouldn't be any na values
    logger