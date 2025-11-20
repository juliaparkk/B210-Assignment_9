# create a dictionary of song titles keyed by track_number and write to CSV
def split_csv_line(line):
    fields = []
    field = ''
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == '"':
                if i + 1 < len(line) and line[i+1] == '"':
                    field += '"'
                    i += 1
                else:
                    in_quotes = False
            else:
                field += ch
        else:
            if ch == '"':
                in_quotes = True
            elif ch == ',':
                fields.append(field)
                field = ''
            else:
                field += ch
        i += 1
    fields.append(field)
    return fields

def escape_field(s):
    if s is None:
        s = ''
    s = str(s)
    if '"' in s:
        s = s.replace('"', '""')
    if ',' in s or '"' in s or '\n' in s:
        return f'"{s}"'
    return s

def find_header_index(headers, candidates):
    for cand in candidates:
        for i, h in enumerate(headers):
            if h == cand:
                return i
    # fallback: try partial matches
    for i, h in enumerate(headers):
        for cand in candidates:
            if all(tok in h for tok in cand.split()):
                return i
    return None

def create_track_dict(input_csv_path, output_csv_path):
    with open(input_csv_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    if not lines:
        raise ValueError("Input CSV is empty")

    header = split_csv_line(lines[0])
    normalized = [h.strip().lstrip('\ufeff').lower() for h in header]

    # Possible header names to look for
    track_number_names = ['track_number', 'tracknumber', 'track no', 'track_no', 'track no.']
    track_name_names = ['track_name', 'trackname', 'title', 'name']

    # find indices
    idx_track = find_header_index(normalized, track_number_names)
    idx_name = find_header_index(normalized, track_name_names)

    if idx_track is None or idx_name is None:
        # try looser heuristics
        for i, h in enumerate(normalized):
            if 'track' in h and 'number' in h:
                idx_track = idx_track or i
            if ('track' in h and 'name' in h) or ('title' in h) or (h == 'name'):
                idx_name = idx_name or i

    if idx_track is None or idx_name is None:
        raise ValueError("Could not find `track_number` or `track_name` headers in CSV")

    track_dict = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        row = split_csv_line(line)
        # protect against short rows
        name = row[idx_name].strip() if idx_name < len(row) else ''
        number = row[idx_track].strip() if idx_track < len(row) else ''
        # normalize empty track numbers to an explicit key
        if number == '':
            number = '<missing>'
        if number not in track_dict:
            track_dict[number] = []
        track_dict[number].append(name)

    # Write output CSV: track_number,track_titles (titles joined by " | ")
    keys = list(track_dict.keys())
    # attempt numeric sort where possible
    def key_sort(k):
        try:
            return int(k)
        except:
            return k
    keys.sort(key=key_sort)

    with open(output_csv_path, 'w', encoding='utf-8', newline='') as outf:
        outf.write('track_number,track_titles\n')
        for k in keys:
            joined = ' | '.join(track_dict[k])
            outf.write(f"{escape_field(k)},{escape_field(joined)}\n")

    return track_dict

if __name__ == '__main__':
    # Default paths (edit if needed)
    input_path = r"C:\Users\jinas\OneDrive\Documents\taylor_discography.csv"
    output_path = r"C:\Users\jinas\Downloads\tracks_by_number.csv"

    d = create_track_dict(input_path, output_path)
    print(f"Wrote {output_path}  (keys: {len(d)})")
    # print first 10 keys for quick check
    cnt = 0
    for k in sorted(d.keys(), key=lambda x: int(x) if x.isdigit() else x):
        print(k, "->", len(d[k]), "titles")
        cnt += 1
        if cnt >= 10:
            break