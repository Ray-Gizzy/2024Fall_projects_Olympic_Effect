import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
import numpy as np

def calculate_growth_rate(df, metric_column):
    """
    Calculate the growth rate for GDP or FDI per year.

    :param df: a cleaned dataframe
    :param metric_column: the GDP/FDI column
    :return: DataFrame with an additional column 'Growth Rate (%)'
    """
    growth_rates = [0]

    for i in range(1, len(df)):
        previous_year = df.loc[i - 1, metric_column]  # row:i-1, col: metric
        current_year = df.loc[i, metric_column]

        if previous_year == 0:
            growth_rates.append(0)
        else:
            growth_rate = ((current_year - previous_year) / previous_year) * 100
            growth_rates.append(growth_rate)

    df['Growth Rate (%)'] = growth_rates
    return df


def index_rename_and_calculate_growth_rate(df, rename_dict=None, host_year=None, metric_column=None):
    """
    Second clean the data to prepare for growth rate comparison plot.

    :param df: a cleaned dataframe from DataProcess.py
    :param rename_dict: the columns needed to be renamed
    :param host_year: either 2000 or 2008
    :param metric_column: GDP or FDI column to apply the "calculate_growth_rate" function
    :return: cleaned dataFrame
    """
    df.reset_index(inplace=True)
    df.columns = df.columns.str.strip()
    if rename_dict:
        df.rename(columns=rename_dict, inplace=True)

    if df['Year'].iloc[0] > df['Year'].iloc[-1]:  # High to Low
        df.sort_values(by='Year', inplace=True)  # Sort ascending
    calculate_growth_rate(df, metric_column=metric_column)
    df['Relative Year'] = df['Year'] - host_year
    return df


def growth_rate_plot(dfs, countries, metric, colors):
    """
    Plot the growth rate for countries.

    :param dfs: dataframes from "index_rename_and_calculate_growth_rate"
    :param countries: countries to compare growth rates
    :param metric: column to compare growth rates
    :param colors: color of line
    """
    if colors is None:
        colors = ['blue', 'yellow']

    plt.figure(figsize=(8, 5))
    for df, country, color in zip(dfs, countries, colors):
        plt.plot(
            df['Relative Year'],
            df['Growth Rate (%)'],
            label=f"{country} {metric} Growth Rate",
            marker='o',
            color=color
        )
    plt.axvline(x=0, color='red', linestyle='--', label='Host Year')
    plt.title(f"{metric} Growth (Relative to Hosting Year)")
    plt.xlabel("Years (Relative to Hosting Year)")
    plt.ylabel(f"{metric} Growth Rate (%)")
    plt.legend()
    plt.grid()
    plt.show()


def two_subplots(
        df1, host_year1, legend1, title1,
        df2, host_year2, legend2, title2,
        x_column, y_column, xlabel, ylabel,
        ):
    """
    Plot two subplots for given dataframes and metrics.

    :param df1: DataFrame for the first plot.
    :param df2: DataFrame for the second plot.
    :param x_column: Column name for the x-axis.
    :param y_column: Column name for the y-axis.
    :param title1: Title for the first subplot.
    :param title2: Title for the second subplot.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param legend1: Legend for the first plot.
    :param legend2: Legend for the second plot.
    :param host_year1: 2000
    :param host_year2: 2008
    """

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)  # Subplot 1: 1ROW, 2COLS
    plt.plot(df1[x_column], df1[y_column], label=legend1, marker='o', color='blue')
    plt.axvline(x=host_year1, color='red', linestyle='--', label=f'{host_year1} Olympics')
    plt.title(title1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)  # Subplot 2
    plt.plot(df2[x_column], df2[y_column], label=legend2, marker='o', color='yellow')
    plt.axvline(x=host_year2, color='red', linestyle='--', label=f'{host_year2} Olympics')
    plt.title(title2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    # Adjust layout and show
    plt.tight_layout()
    plt.show()


def two_plot_health(
        df1, host_year1, title1,
        df2, host_year2, title2,
        x_column, y_column, xlabel, ylabel, metric, gender_column):
    """
    Compare health trends for two countries using three gender categories.

    :param df1: DataFrame for the first country (e.g., Australia).
    :param host_year1: host year for the first country.
    :param title1: Title for the first country.
    :param df2: DataFrame for the second country.
    :param host_year2: host year for the second country.
    :param title2: Title for the second country.
    :param x_column: Column name for the x-axis.
    :param y_column: Column name for the y-axis.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param metric: column to compare health trends
    :param gender_column: Column name for the gender categories.
    """

    genders = ['Female', 'Male', 'Both sexes']
    colors = ['blue', 'orange', 'green']

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    for gender, color in zip(genders, colors):
        gender_data = df1[df1[gender_column] == gender]
        plt.plot(
            gender_data[x_column],
            gender_data[y_column],
            label=f'Australia {gender} {metric}',
            marker='o',
            color=color
        )
    plt.axvline(x=host_year1, color='red', linestyle='--', label=f'{host_year1} Olympics')
    plt.title(title1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    # Plot for the second country
    plt.subplot(1, 2, 2)
    for gender, color in zip(genders, colors):
        gender_data = df2[df2[gender_column] == gender]
        plt.plot(
            gender_data[x_column],
            gender_data[y_column],
            label=f'China {gender} {metric}',
            marker='o',
            color=color
        )
    plt.axvline(x=host_year2, color='red', linestyle='--', label=f'{host_year2} Olympics')
    plt.title(title2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()


def load_and_merge_data(cleaned_data_dict):
    """
    Load and merge cleaned data dynamically based on the provided dictionary.

    :param cleaned_data_dict: Dictionary with metric names as keys and a nested dictionary
                              containing "AUS" and "CHI" DataFrames.
    :return: Merged DataFrame with country-specific columns.
    """
    merged_data = pd.DataFrame()

    for metric_name, country_data in cleaned_data_dict.items():
        aus_data = country_data["AUS"]
        chi_data = country_data["CHI"]

        # Select relevant columns and rename for each country
        aus_data = aus_data[["Relative Year", metric_name]].rename(columns={metric_name: f"{metric_name}_AUS"})
        chi_data = chi_data[["Relative Year", metric_name]].rename(columns={metric_name: f"{metric_name}_CHI"})

        if merged_data.empty:
            # Initialize merged_data with the first metric
            merged_data = aus_data.merge(chi_data, on="Relative Year", how="left")
        else:
            # Merge subsequent metrics
            merged_data = merged_data.merge(aus_data, on="Relative Year", how="left")
            merged_data = merged_data.merge(chi_data, on="Relative Year", how="left")

    return merged_data


def calculate_correlation(df, metrics, time_period=None):
    """
    Calculate correlation between metrics within a specific time period.

    :param df: DataFrame containing metrics
    :param metrics: List of column names for metrics to analyze
    :param time_period: Tuple (start, end) to filter by Relative Year
    :return: Correlation matrix
    """
    if time_period:
        df = df[df['Relative Year'].between(*time_period)]
    return df[metrics].corr()


metric_groups = {
    "Economic": ["GDP_per_capita", "FDI", "Gov_Consumption"],
    "Social": ["Num_Arrivals", "Obesity_rate", "Underweight_rate", "Unemployment_Rate(%)"],
    "Environmental": ["MtCO2e"]
}

country_suffix = {"Australia": "_AUS", "China": "_CHI"}


def compute_country_correlation_matrices(merged_data, metric_groups, country_suffix):
    """
    Compute correlation matrices for each country and each metric group.

    :param merged_data: DataFrame with merged country metrics.
    :param metric_groups: Dictionary of metric groups and their metrics.
    :param country_suffix: Dictionary mapping country names to their column suffixes.
    :return: Dictionary containing correlation matrices for each country and group.
    """
    correlation_matrices = {country: {} for country in country_suffix}

    for country, suffix in country_suffix.items():
        print(f"\nComputing correlation matrices for {country}:")
        for group, metrics in metric_groups.items():
            group_columns = [f"{metric}{suffix}" for metric in metrics if f"{metric}{suffix}" in merged_data.columns]
            if len(group_columns) > 1:
                group_corr = calculate_correlation(merged_data, group_columns, time_period=(-5, 5))
                correlation_matrices[country][group] = group_corr
                print(f"\n{group} Correlation Matrix for {country}:")
                print(group_corr)
            else:
                print(f"Not enough data for {group} metrics in {country}.")
    return correlation_matrices


def plot_correlation_heatmap(correlation_matrix, title="Correlation Heatmap"):
    """
    Plot a heatmap for the given correlation matrix.

    :param correlation_matrix: Correlation matrix (Pandas DataFrame)
    :param title: Title for the heatmap
    """

    if correlation_matrix is not None and not correlation_matrix.empty:
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title(title, fontsize=16)
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
    else:
        print(f"No data available to plot heatmap: {title}")


def plot_all_heatmaps(correlation_matrices, metric_groups):
    """
    Plot heatmaps for each country and metric group.

    :param correlation_matrices: Dictionary containing correlation matrices by country.
    :param metric_groups: Dictionary defining the metric groups (e.g., Economic, Social).
    """
    for country, group_data in correlation_matrices.items():
        print(f"Generating heatmaps for {country}:")
        for group, group_corr in group_data.items():
            if group_corr is not None:  # Ensure there is a valid correlation matrix
                title = f"{group} Metric Correlation ({country})"
                plot_correlation_heatmap(group_corr, title=title)
            else:
                print(f"Not enough data for {group} metrics in {country}.")


# Define predefined combinations with descriptions
predefined_combinations = {
    "1": {
        "description": "Do GDP and FDI correlated?",
        "metrics": ("GDP_per_capita", "FDI")
    },
    "2": {
        "description": "How does fiscal policy impact government consumption?",
        "metrics": ("GDP_per_capita", "Gov_Consumption")
    },
    "3": {
        "description": "Does tourism impact economic growth?",
        "metrics": ("Num_Arrivals", "GDP_per_capita")
    },
    "4": {
        "description": "Health trade-offs",
        "metrics": ("Obesity_rate", "Underweight_rate")
    },
    "5": {
        "description": "Environmental cost of economic growth",
        "metrics": ("GDP_per_capita", "MtCO2e")
    },
    "6": {
        "description": "Does increasing tourism lead to higher GHG emission?",
        "metrics": ("Num_Arrivals", "MtCO2e")
    },
    "7": {
        "description": "Economic growth's effect on employment",
        "metrics": ("Unemployment_Rate(%)", "GDP_per_capita")
    }
}


def predefined_correlation_analysis(merged_data):
    # Display the menu with descriptions first
    print("\nAvailable Metric Combinations:")
    for key, combination in predefined_combinations.items():
        print(f"{key}: {combination['description']}")

    # Add a short delay to ensure the output is printed before input prompt
    time.sleep(0.5)

    # User selects a combination
    selected_key = input("\nChoose a combination number (e.g., 1): ").strip()
    if selected_key not in predefined_combinations:
        print("Invalid selection!")
        return

    combination = predefined_combinations[selected_key]
    metric1, metric2 = combination["metrics"]
    print(f"\nSelected combination: {combination['description']}")

    # User selects a country suffix
    country = input("Select a country suffix (AUS or CHI): ").strip().upper()
    if country not in ["AUS", "CHI"]:
        print("Invalid country suffix!")
        return

    suffix = f"_{country}"
    print(f"\nSelected country suffix: {country}")

    # Check if the selected metrics exist directly in merged_data
    metric1_col = f"{metric1}{suffix}"
    metric2_col = f"{metric2}{suffix}"
    print(f"Checking columns: {metric1_col} and {metric2_col}")

    if metric1_col not in merged_data.columns or metric2_col not in merged_data.columns:
        print(f"Missing: {metric1_col} or {metric2_col} in {country}. Cannot calculate correlation.")
        return

    # Calculate correlation
    correlation_value = merged_data[[metric1_col, metric2_col]].corr().iloc[0, 1]
    print(f"\nCorrelation between {metric1} and {metric2} in {country}: {correlation_value:.2f}")

    # Visualization (optional)
    plt.figure(figsize=(6, 4))
    plt.scatter(merged_data[metric1_col], merged_data[metric2_col], alpha=0.6, edgecolor='k')
    plt.title(f"Correlation between {metric1} and {metric2} in {country}")
    plt.xlabel(metric1)
    plt.ylabel(metric2)
    plt.grid(True)
    plt.show()


def highlight_key_correlations_all_matrices(correlation_matrices, country):
    """
    Highlight the strongest and weakest correlations across all metric group matrices for a given country.

    :param correlation_matrices: Dictionary of correlation matrices (key: group name, value: DataFrame)
    :param country: Country name (e.g., "Australia", "China")
    """
    print(f"\n=== Highlighting Key Correlations for {country} ===")

    for group, matrix in correlation_matrices.items():
        # Flatten the matrix for easier analysis (ignore diagonal)
        flattened = matrix.where(~np.eye(matrix.shape[0], dtype=bool))

        strongest_pair = flattened.unstack().idxmax()
        weakest_pair = flattened.unstack().idxmin()

        strongest_value = flattened.unstack().max()
        weakest_value = flattened.unstack().min()

        print(f"\n{group} Correlation Matrix:")
        print(f"  Strongest correlation: {strongest_pair} = {strongest_value:.2f}")
        print(f"  Weakest correlation: {weakest_pair} = {weakest_value:.2f}")


def plot_predefined_combinations_bar(predefined_combinations, merged_data):
    """
    Computes correlations for predefined combinations and plots a bar chart.

    :param predefined_combinations: Dictionary of metric pairs and descriptions.
    :param merged_data: DataFrame containing merged data with metrics for both countries.
    """
    correlations = []

    for key, combo in predefined_combinations.items():
        metric1, metric2 = combo["metrics"]

        # Check if the metrics exist in the merged_data
        for country_suffix in ["_AUS", "_CHI"]:
            metric1_col = f"{metric1}{country_suffix}"
            metric2_col = f"{metric2}{country_suffix}"

            if metric1_col in merged_data.columns and metric2_col in merged_data.columns:
                # Compute correlation
                corr_value = merged_data[[metric1_col, metric2_col]].corr().iloc[0, 1]
                correlations.append({
                    "Combination": f"{metric1} vs {metric2}",
                    "Country": "Australia" if country_suffix == "_AUS" else "China",
                    "Correlation": corr_value
                })
            else:
                print(f"Missing: {metric1_col} or {metric2_col} in {country_suffix.replace('_', '')}")

    # Create DataFrame for plotting
    corr_df = pd.DataFrame(correlations)

    # Create bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=corr_df, x="Combination", y="Correlation", hue="Country", dodge=True)
    plt.title("Correlation Strengths for Predefined Metric Pairs")
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.ylabel("Correlation Coefficient")
    plt.xlabel("Metric Pairs")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(title="Country")
    plt.tight_layout()
    plt.show()



