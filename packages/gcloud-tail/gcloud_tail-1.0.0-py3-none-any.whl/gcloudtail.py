import sys
import json
import subprocess

# show up to 1 minute or

def get_logs():
    args = ['gcloud', 'logging', 'read'] + sys.argv[1:] + ['--format', 'json', '--freshness', '30s']
    res = subprocess.run(args, stdout=subprocess.PIPE, check=True)
    return json.loads(res.stdout)

def main():
    try:
        seen_insert_ids = []
        while True:
            logs = get_logs()

            keepers = []
            for log in logs:
                insert_id = log['insertId']
                if any(insert_id in seen for seen in seen_insert_ids):
                    continue
                keepers.append(log)
            for log in sorted(keepers, key=lambda l: l['receiveTimestamp']):
                sys.stdout.write(json.dumps(log) + '\n')

            # stash the list of insert_ids we saw, and only keep 10
            seen_insert_ids.append(set(l['insertId'] for l in logs))
            seen_insert_ids = seen_insert_ids[-10:]
    except KeyboardInterrupt:
        sys.exit(1)

main()
