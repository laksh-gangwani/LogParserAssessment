# VPC Flow Log Parser and Tagger

This Python script parses AWS VPC Flow Logs and tags each entry based on a lookup table. It generates statistics on tag counts and port/protocol combination counts.

## Requirements

- Python 3.x
- No external libraries required

## Assumptions

1. The program only supports the default log format for AWS VPC Flow Logs.
2. Only version 2 of the flow logs is supported.
3. The input files (both flow logs and lookup table) are ASCII text files.
4. The flow log file size can be up to 10 MB.
5. The lookup file can have up to 10,000 mappings.
6. Tags can map to more than one port/protocol combination.
7. All matches are case-insensitive.

## Usage

```
python flow_log_parser.py <lookup_file> <log_file> <output_file>
```

- `<lookup_file>`: Path to the CSV file containing the lookup table
- `<log_file>`: Path to the text file containing the VPC flow logs
- `<output_file>`: Path where the output CSV file will be written

## Input File Formats

### Lookup Table (CSV)

The lookup table should be a CSV file with the following columns:
- dstport: Destination port number
- protocol: Protocol (e.g., tcp, udp, icmp)
- tag: Tag to be applied

Example:
```
dstport,protocol,tag
25,tcp,sv_P1
68,udp,sv_P2
23,tcp,sv_P1
```

### Flow Log File

The flow log file should be in the default AWS VPC Flow Log format (version 2). Each line should contain space-separated fields as described in the [AWS documentation](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html).

## Output

The script generates a CSV file with two sections:

1. Tag Counts: Shows the count of each tag applied to the flow log entries.
2. Port/Protocol Combination Counts: Shows the count of each unique port and protocol combination found in the flow logs.

## License

This project is open-source and available under the MIT License.