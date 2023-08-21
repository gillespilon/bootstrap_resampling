#! /usr/bin/env python3
"""
Analysis of Galton's height data.
"""

from pathlib import Path
import time

import datasense as ds


def main():
    start_time = time.perf_counter()
    header_title = 'Galton height analysis using resampling'
    output_url = 'galton.html'
    header_id = 'galton'
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    ds.script_summary(
        script_path=Path(__file__),
        action='started at'
    )
    galton_path = Path("galton.csv")
    df_galton_families = ds.read_file(file_name=galton_path)
    print("Analysis of entire data file")
    print()
    ds.dataframe_info(df=df_galton_families, file_in=galton_path)
    print("Analysis of female children")
    print()
    df_galton_female_children = df_galton_families[
        df_galton_families["child_sex"] == "F"
    ]
    ds.dataframe_info(
        df=df_galton_female_children,
        file_in=galton_path
    )
    print("Analysis of male children")
    print()
    df_galton_male_children = df_galton_families[
        df_galton_families["child_sex"] == "M"
    ]
    ds.dataframe_info(
        df=df_galton_male_children,
        file_in=galton_path
    )
    stop_time = time.perf_counter()
    ds.script_summary(
        script_path=Path(__file__),
        action='finished at'
    )
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time
    )
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == "__main__":
    main()
