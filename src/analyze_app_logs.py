import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_parsed_logs():
    """Load parsed HDFS and Hadoop log data."""
    hdfs_path = "processed_data/app-logs/hdfs_parsed.csv"
    hadoop_path = "processed_data/app-logs/hadoop_parsed.csv"

    df_hdfs = pd.read_csv(hdfs_path, parse_dates=["timestamp"])
    df_hadoop = pd.read_csv(hadoop_path, parse_dates=["timestamp"])

    df_hdfs["dataset"] = "HDFS"
    df_hadoop["dataset"] = "Hadoop"

    return df_hdfs, df_hadoop


def generate_summary_stats(df_hdfs, df_hadoop, out_dir):
    """Generate summary statistics CSVs."""
    stats_dir = os.path.join(out_dir, "summary_stats")
    os.makedirs(stats_dir, exist_ok=True)

    # Log level distribution per dataset
    level_counts_hdfs = df_hdfs["level"].value_counts().reset_index()
    level_counts_hdfs.columns = ["level", "count"]
    level_counts_hdfs.to_csv(os.path.join(stats_dir, "hdfs_level_distribution.csv"), index=False)

    level_counts_hadoop = df_hadoop["level"].value_counts().reset_index()
    level_counts_hadoop.columns = ["level", "count"]
    level_counts_hadoop.to_csv(os.path.join(stats_dir, "hadoop_level_distribution.csv"), index=False)

    # Component frequency per dataset
    comp_hdfs = df_hdfs["component"].value_counts().reset_index()
    comp_hdfs.columns = ["component", "count"]
    comp_hdfs.to_csv(os.path.join(stats_dir, "hdfs_component_frequency.csv"), index=False)

    comp_hadoop = df_hadoop["component"].value_counts().head(15).reset_index()
    comp_hadoop.columns = ["component", "count"]
    comp_hadoop.to_csv(os.path.join(stats_dir, "hadoop_component_frequency.csv"), index=False)

    # Timeline: events per minute
    for name, df in [("hdfs", df_hdfs), ("hadoop", df_hadoop)]:
        df_ts = df.set_index("timestamp").resample("min").size().reset_index()
        df_ts.columns = ["timestamp", "event_count"]
        df_ts.to_csv(os.path.join(stats_dir, f"{name}_events_per_minute.csv"), index=False)

    # Error/WARN summary for Hadoop (the dataset with errors)
    errors = df_hadoop[df_hadoop["level"].isin(["ERROR", "FATAL", "WARN"])]
    error_by_component = errors.groupby("component").size().reset_index(name="count")
    error_by_component = error_by_component.sort_values("count", ascending=False)
    error_by_component.to_csv(os.path.join(stats_dir, "hadoop_errors_by_component.csv"), index=False)

    print(f"Summary stats saved to {stats_dir}")


def generate_plots(df_hdfs, df_hadoop, out_dir):
    """Generate visualization plots."""
    plots_dir = os.path.join(out_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    # 1. Log level distribution - side by side bar chart
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    hdfs_levels = df_hdfs["level"].value_counts()
    hadoop_levels = df_hadoop["level"].value_counts()

    hdfs_levels.plot(kind="bar", ax=axes[0], color="steelblue", edgecolor="white")
    axes[0].set_title("HDFS - Log Level Distribution")
    axes[0].set_ylabel("Count")
    axes[0].set_xlabel("")
    axes[0].tick_params(axis="x", rotation=0)

    hadoop_levels.plot(kind="bar", ax=axes[1], color=["#2ecc71", "#f1c40f", "#e74c3c", "#9b59b6"], edgecolor="white")
    axes[1].set_title("Hadoop - Log Level Distribution")
    axes[1].set_ylabel("Count")
    axes[1].set_xlabel("")
    axes[1].tick_params(axis="x", rotation=0)

    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "log_level_distribution.png"), dpi=150)
    plt.close()

    # 2. Top 10 components per dataset
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    hdfs_comp = df_hdfs["component"].value_counts().head(10)
    hadoop_comp = df_hadoop["component"].value_counts().head(10)

    hdfs_comp.plot(kind="barh", ax=axes[0], color="steelblue", edgecolor="white")
    axes[0].set_title("HDFS - Top 10 Components")
    axes[0].set_xlabel("Count")
    axes[0].invert_yaxis()

    hadoop_comp.plot(kind="barh", ax=axes[1], color="coral", edgecolor="white")
    axes[1].set_title("Hadoop - Top 10 Components")
    axes[1].set_xlabel("Count")
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "top_components.png"), dpi=150)
    plt.close()

    # 3. Event timeline (events per minute)
    fig, axes = plt.subplots(2, 1, figsize=(14, 7))

    for ax, df, name in [(axes[0], df_hdfs, "HDFS"), (axes[1], df_hadoop, "Hadoop")]:
        timeline = df.set_index("timestamp").resample("min").size()
        ax.fill_between(timeline.index, timeline.values, alpha=0.7, color="steelblue")
        ax.set_title(f"{name} - Event Rate Over Time")
        ax.set_ylabel("Events/min")
        ax.set_xlabel("Time")

    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "event_timeline.png"), dpi=150)
    plt.close()

    # 4. Hadoop errors by component
    errors = df_hadoop[df_hadoop["level"].isin(["ERROR", "FATAL", "WARN"])]
    error_comp = errors["component"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    error_comp.plot(kind="barh", ax=ax, color="#e74c3c", edgecolor="white")
    ax.set_title("Hadoop - Top 10 Components by Error/Warn Count")
    ax.set_xlabel("Count")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "hadoop_errors_by_component.png"), dpi=150)
    plt.close()

    print(f"Plots saved to {plots_dir}")


def main():
    out_dir = "processed_data/app-logs"

    df_hdfs, df_hadoop = load_parsed_logs()
    generate_summary_stats(df_hdfs, df_hadoop, out_dir)
    generate_plots(df_hdfs, df_hadoop, out_dir)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
