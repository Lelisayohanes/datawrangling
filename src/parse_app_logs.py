import re
import os
import pandas as pd


def parse_hdfs_log(filepath):
    """Parse HDFS log entries into structured records.

    Expected format:
        YYMMDD HHMMSS <seq> <LEVEL> <component>: <message>
    """
    pattern = re.compile(
        r"^(\d{6})\s+(\d{6})\s+(\d+)\s+(\w+)\s+([\w.$]+):\s+(.*)$"
    )
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                date_str, time_str, seq, level, component, message = match.groups()
                timestamp = f"20{date_str[:2]}-{date_str[2:4]}-{date_str[4:6]} " \
                            f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"
                records.append({
                    "timestamp": timestamp,
                    "level": level,
                    "component": component,
                    "message": message,
                    "source": os.path.basename(filepath),
                })
    return records


def parse_hadoop_log(filepath):
    """Parse Hadoop log entries into structured records.

    Expected format (log4j):
        YYYY-MM-DD HH:MM:SS,mmm <LEVEL> [<thread>] <class>: <message>
    """
    pattern = re.compile(
        r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}),\d{3}\s+"
        r"(\w+)\s+\[([^\]]*)\]\s+([\w.$]+):\s+(.*)$"
    )
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                timestamp, level, thread, component, message = match.groups()
                records.append({
                    "timestamp": timestamp,
                    "level": level,
                    "thread": thread,
                    "component": component,
                    "message": message,
                    "source": os.path.basename(filepath),
                })
    return records


def main():
    log_dir = "data/app-logs"
    out_dir = "processed_data/app-logs"
    os.makedirs(out_dir, exist_ok=True)

    # Parse HDFS logs
    hdfs_path = os.path.join(log_dir, "HDFS_2k.log")
    if os.path.exists(hdfs_path):
        hdfs_records = parse_hdfs_log(hdfs_path)
        df_hdfs = pd.DataFrame(hdfs_records)
        df_hdfs.to_csv(os.path.join(out_dir, "hdfs_parsed.csv"), index=False)
        print(f"HDFS: parsed {len(df_hdfs)} entries")

    # Parse Hadoop logs
    hadoop_path = os.path.join(log_dir, "Hadoop_2k.log")
    if os.path.exists(hadoop_path):
        hadoop_records = parse_hadoop_log(hadoop_path)
        df_hadoop = pd.DataFrame(hadoop_records)
        df_hadoop.to_csv(os.path.join(out_dir, "hadoop_parsed.csv"), index=False)
        print(f"Hadoop: parsed {len(df_hadoop)} entries")


if __name__ == "__main__":
    main()
