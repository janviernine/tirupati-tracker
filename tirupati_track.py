import requests, re, sys
from html import unescape

# Tracking URL for your parcel
# To track a different parcel, replace this with that parcel's Frm_DocTrackWeb.aspx?docno=... link
URL = "https://www.shreetirupaticourier.net/Frm_DocTrackWeb.aspx?docno=<PASTE_YOUR_docno_TOKEN>&Tmp=<PASTE_YOUR_Tmp>"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,*/*",
}

try:
    r = requests.get(URL, headers=headers, timeout=20)
    r.raise_for_status()
    html = r.text
except Exception as e:
    print(f"ERROR fetch: {e}")
    sys.exit(0)

def extract(pattern):
    m = re.search(pattern, html, re.S|re.I)
    return m.group(1).strip() if m else ""

doc = extract(r'id="lblDocNumber"[^>]*>(.*?)</span>')
from_center = extract(r'id="txtFromCenter"[^>]*>(.*?)</span>')
to_center = extract(r'id="txtToCent[^"]*"[^>]*>(.*?)</span>')
date = extract(r'id="txtDate"[^>]*>(.*?)</span>')
status = extract(r'id="lblStatus"[^>]*>(.*?)</span>')
status = re.sub(r'<[^>]+>', ' ', status)
status = re.sub(r'\s+', ' ', unescape(status)).strip()
rows = re.findall(r'<tr>\s*<td>(OUT|IN|[^<]+)</td>\s*<td>([^<]+)</td>\s*<td>(.*?)</td>', html, re.S|re.I)
clean_rows = []
for job, dt, route in rows:
    route = re.sub(r'<[^>]+>', '', route)
    route = re.sub(r'\s+', ' ', unescape(route)).strip()
    clean_rows.append(f"{job} | {dt.strip()} | {route}")
print(f"AWB: {doc}")
print(f"Route: {from_center} -> {to_center}")
print(f"Booked: {date}")
print(f"STATUS: {status}")
print("Tracking:")
for cr in clean_rows:
    print(f" - {cr}")
print(f"CHECKSUM: {status} | {' ; '.join(clean_rows)}")
