import csv
from collections import defaultdict
import sys

def load_lookup_table(file_path):
    lookup = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())
            lookup[key] = row['tag']
    return lookup

def parse_flow_logs(log_file_path, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    
    with open(log_file_path, 'r') as f:
        for line in f:
            fields = line.strip().split()
            if len(fields) < 14: 
                continue
            
            dst_port = int(fields[6])
            protocol = {6: 'tcp', 17: 'udp', 1: 'icmp'}.get(int(fields[7]), 'unknown')
            
            key = (dst_port, protocol)
            tag = lookup_table.get(key, 'Untagged')
            
            tag_counts[tag] += 1
            port_protocol_counts[key] += 1
    
    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        writer.writerow(["Tag Counts:"])
        writer.writerow(["Tag", "Count"])
        for tag, count in sorted(tag_counts.items()):
            writer.writerow([tag, count])
        
        writer.writerow([])  
        
        writer.writerow(["Port/Protocol Combination Counts:"])
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            writer.writerow([port, protocol, count])

def main(lookup_file, log_file, output_file):
    lookup_table = load_lookup_table(lookup_file)
    tag_counts, port_protocol_counts = parse_flow_logs(log_file, lookup_table)
    write_output(tag_counts, port_protocol_counts, output_file)
    print(f"Processing complete. Results written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <lookup_file> <log_file> <output_file>")
        sys.exit(1)
    
    lookup_file, log_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    main(lookup_file, log_file, output_file)