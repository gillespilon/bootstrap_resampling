#! /usr/bin/env python3
"""
Analysis of Galton's height data.
"""

from pathlib import Path
import time

import datasense as ds


def main():
    start_time = time.perf_counter()
    histogram_female_children_heights = "galton_female_children_heights.svg"
    histogram_male_children_heights = "galton_male_children_heights.svg"
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
    print("============================")
    print()
    ds.dataframe_info(df=df_galton_families, file_in=galton_path)
    print("Analysis of female children")
    print("===========================")
    print()
    df_galton_female_children = df_galton_families[
        df_galton_families["child_sex"] == "F"
    ]
    print(type(df_galton_female_children).__name__)
    ds.dataframe_info(
        df=df_galton_female_children,
        file_in=galton_path
    )
    print("Analysis of male children")
    print("=========================")
    print()
    df_galton_male_children = df_galton_families[
        df_galton_families["child_sex"] == "M"
    ]
    ds.dataframe_info(
        df=df_galton_male_children,
        file_in=galton_path
    )
    print("Graphs of child heights")
    print("=======================")
    print()
    fig, ax = ds.plot_histogram(
        series=df_galton_female_children["child_height"],
        bin_range=(54, 80),
        bin_width=2
    )
    ax.set_title(label="Histogram of female children weights")
    ax.set_xlabel(xlabel="Height (in)")
    ax.set_ylabel(ylabel="Sample fraction")
    fig.savefig(fname=histogram_female_children_heights, format="svg")
    ds.html_figure(file_name=histogram_female_children_heights)
    fig, ax = ds.plot_histogram(
        series=df_galton_male_children["child_height"],
        bin_range=(54, 80),
        bin_width=2
    )
    ax.set_title(label="Histogram of male children weights")
    ax.set_xlabel(xlabel="Height (in)")
    ax.set_ylabel(ylabel="Sample fraction")
    fig.savefig(fname=histogram_male_children_heights, format="svg")
    ds.html_figure(file_name=histogram_male_children_heights)
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
