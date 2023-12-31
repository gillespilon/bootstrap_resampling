#! /usr/bin/env python3
"""
Analysis of Galton's height data.
"""

from pathlib import Path
import time
import math

import scipy.stats as stats
import datasense as ds
import pandas as pd


def main():
    start_time = time.perf_counter()
    histogram_female_children_heights = "galton_female_children_heights.svg"
    histogram_male_children_heights = "galton_male_children_heights.svg"
    header_title = 'Galton height analysis using resampling'
    histogram_children_heights_differences =\
        "galton_children_heights_differences.svg"
    percentiles = [.025, .25, .5, .75, .975]
    output_url = 'galton.html'
    header_id = 'galton'
    replicates = 1000
    fraction = 1
    alpha = 0.05
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
    print(df_galton_families["child_height"].describe(percentiles=percentiles))
    print()
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
    print(
        df_galton_female_children["child_height"].describe(
            percentiles=percentiles
        )
    )
    print()
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
    print(
        df_galton_male_children["child_height"].describe(
            percentiles=percentiles
        )
    )
    print()
    print("Graphs of child heights")
    print("=======================")
    print()
    fig, ax = ds.plot_histogram(
        series=df_galton_female_children["child_height"],
        bin_range=(54, 80),
        bin_width=2,
        percentiles=[0.025, 0.975]
    )
    ax.set_title(label="Histogram of female children weights")
    ax.set_xlabel(xlabel="Height (in)")
    ax.set_ylabel(ylabel="Sample fraction")
    fig.savefig(fname=histogram_female_children_heights, format="svg")
    ds.html_figure(file_name=histogram_female_children_heights)
    fig, ax = ds.plot_histogram(
        series=df_galton_male_children["child_height"],
        bin_range=(54, 80),
        bin_width=2,
        percentiles=[0.025, 0.975]
    )
    ax.set_title(label="Histogram of male children weights")
    ax.set_xlabel(xlabel="Height (in)")
    ax.set_ylabel(ylabel="Sample fraction")
    fig.savefig(fname=histogram_male_children_heights, format="svg")
    ds.html_figure(file_name=histogram_male_children_heights)
    print("Graph of child height differences")
    print("=================================")
    print()
    sample_differences = []
    male_children_averages = []
    female_children_averages = []
    for i in range(replicates):
        sample = df_galton_families.sample(
            frac=fraction,
            replace=True
        )
        male_children_average = (
            sample.loc[sample["child_sex"] == "M", "child_height"].mean()
        )
        male_children_averages.append(male_children_average)
        female_children_average = (
            sample.loc[sample["child_sex"] == "F", "child_height"].mean()
        )
        female_children_averages.append(female_children_average)
        sample_differences.append(
            male_children_average - female_children_average
        )
    series_differences = pd.Series(data=sample_differences)
    fig, ax = ds.plot_histogram(
        series=series_differences,
        bin_range=(4.5, 5.8),
        bin_width=0.05,
        percentiles=[0.025, 0.975]
    )
    ax.set_title(label="Histogram of children weight differences")
    ax.set_xlabel(xlabel="Height (in)")
    ax.set_ylabel(ylabel="Sample fraction")
    fig.savefig(fname=histogram_children_heights_differences, format="svg")
    ds.html_figure(file_name=histogram_children_heights_differences)
    # Two-sample t test of the series
    print("Two-sample t test of the two series")
    print("===================================")
    print()
    series1 = pd.Series(data=male_children_averages)
    series1_ave = series1.mean()
    series1_n = series1.count()
    series1_var = series1.var()
    series2 = pd.Series(data=female_children_averages)
    series2_ave = series2.mean()
    series2_n = series2.count()
    series2_var = series2.var()
    ds.two_sample_t(
        series1=series1,
        series2=series2
    )
    # Two-sample t test of the differences
    print("Two-sample t test of the differences")
    print("====================================")
    print()
    delta_one_two = math.fabs(
        series1_ave - series2_ave
    )
    va = series1_var / series1_n
    vb = series2_var / series2_n
    vc = series1_n + series2_n - 2
    ve = math.sqrt(
        1 / series1_n + 1 / series2_n
    )
    t_critical_equal = stats.t.isf(alpha / 2, vc)
    standard_deviation_pooled = math.sqrt(
        ((series1_n - 1) * series1_var +
         (series2_n - 1) * series2_var) / vc
    )
    lower_limit = delta_one_two - t_critical_equal * \
                  standard_deviation_pooled * ve
    upper_limit = delta_one_two + t_critical_equal * \
                  standard_deviation_pooled * ve
    if 0 < lower_limit or 0 > upper_limit:
        print(
             'The two averages are statistically, '
             'significantly different '
             'because 0 is not contained within the '
             'confidence interval ' +
             '(' + str(lower_limit.round(3)) + ', ' +
             str(upper_limit.round(3)) + ')'
             ' of the difference ' +
             str(round(number=delta_one_two, ndigits=3)) + '.'
        )
    else:
        print(
            'The two averages are not statistically, '
             'significantly different '
             'because 0 is contained within the '
             'confidence interval ' +
             '(' + str(lower_limit.round(3)) + ', ' +
             str(upper_limit.round(3)) + ')'
             ' of the difference ' +
             str(round(number=delta_one_two, ndigits=3)) + '.'
        )
    print()
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
