# App Logs - Processed

## Purpose
This directory contains structured log data and analysis outputs derived from raw HDFS and Hadoop application logs.


## Raw Data Context
For full details on raw data, see `data/app-logs/README.md`.

### Raw Data Summary
- **Purpose**: Application log data for operational analysis
- **Source**: Two log files (2000 entries each)
  - `HDFS_2k.log`: Hadoop Distributed File System logs
  - `Hadoop_2k.log`: Hadoop MapReduce job execution logs
- **Structure**: Unstructured text with varying log formats per source


## Processed Data

### Parsing
Raw log entries were parsed into structured fields using regex-based parsers in `src/parse_app_logs.py`.

**HDFS format**: `YYMMDD HHMMSS <seq> <LEVEL> <component>: <message>`
**Hadoop format**: `YYYY-MM-DD HH:MM:SS,mmm <LEVEL> [<thread>] <class>: <message>`

### Transformations Applied
1. **Log Parsing**: Extracted timestamp, level, component, and message fields
2. **Timestamp Normalization**: Converted to consistent ISO-like datetime format
3. **Thread Extraction**: Captured thread context from Hadoop logs
4. **Source Tagging**: Added source file identifier per record

### Output Structure
- `hdfs_parsed.csv`: Parsed HDFS log entries (2000 records)
- `hadoop_parsed.csv`: Parsed Hadoop log entries (2000 records)
- `summary_stats/`: Aggregated statistics
  - `hdfs_level_distribution.csv`: Log level counts for HDFS
  - `hadoop_level_distribution.csv`: Log level counts for Hadoop
  - `hdfs_component_frequency.csv`: Component frequency for HDFS
  - `hadoop_component_frequency.csv`: Top 15 components for Hadoop
  - `hdfs_events_per_minute.csv`: HDFS event timeline
  - `hadoop_events_per_minute.csv`: Hadoop event timeline
  - `hadoop_errors_by_component.csv`: Error/WARN/FATAL counts by component
- `plots/`: Visualizations
  - `log_level_distribution.png`: Level distribution comparison
  - `top_components.png`: Top 10 components per dataset
  - `event_timeline.png`: Event rate over time
  - `hadoop_errors_by_component.png`: Hadoop error sources

### Usage
```python
import pandas as pd

df_hdfs = pd.read_csv("hdfs_parsed.csv", parse_dates=["timestamp"])
df_hadoop = pd.read_csv("hadoop_parsed.csv", parse_dates=["timestamp"])
```


## Data Quality
- Total records parsed: 4,000 (2,000 per source)
- HDFS levels: INFO (1920), WARN (80)
- Hadoop levels: INFO (1040), WARN (808), ERROR (150), FATAL (2)
