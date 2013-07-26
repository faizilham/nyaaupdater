Documentation
=============

Nyaa Parser
----------------

`nyaa_parser.py`: Fetching and parsing Nyaa.eu html page.

1. `fetch(url, regexPattern)`
   - Connect to URL (Nyaa.eu search URL) and fetch result by `regexPattern` using `NyaaParser`.
   - The result will be a list of dictionary {`name`, `link`, `page`, `desc`, `date`}.
2. `download(url, filename)`
   - Download from URL as `filename`.
3. `parse(raw_xml_string, regexPattern)`
   - Parsing raw xml data to build the feed dictionary

Nyaa DB
-----

`nyaa_db.py`: Manage feed database.

The feed database (`nyaa_checklist.csv`) is a comma-seperated values of:

- `series_id`: The series name.
- `search_url`: Nyaa.eu search URL.
- `regex_pattern`: Regex pattern of desired result.
- `last_downloaded`: The last downloaded file's name, without `.torrent` extension.


1. Building a NyaaDB object
   - You may use a custom file as long as it is consistent with the format above.
   - `db = NyaaDB()`
   - You may also use a sqlite file (`nyaa_checklist.db`) by using `db = NyaaSQLiteDB()`

2. Load the database
   - `db.load()`
   - It will return a dictionary of key `series_id` and `values list [search_url, regex_pattern, last_downloaded]`. Ex: `{series1: [url, pattern, filename]}`
   - You can also access this list using `db.data`

3. Add
   - `db.add(new_data)`
   - Add new_data to database
   - `new_data` is a dictionary of key `series_id` and `values list [search_url, regex_pattern, last_downloaded]`. Ex: `{series1: [url, pattern, filename]}`

4. Delete
   - `db.delete(keys)`
   - Delete entries with key keys from database.
   - Keys is list of `series_id`. Ex: `[series1, series2, series3]`

5. Update
   - `db.update(updates)`
   - Update database with updates.
   - Updates is a dictionary of key `series_id` and `values list [search_url, regex_pattern, last_downloaded]`. Ex: `{series1: [url, pattern, filename]}`
   - If URL, pattern or filename is not empty / `None`, it will be updated to the database.
   - Please make sure the `last_downloaded` is the last downloaded file's name, without `.torrent` extension.

4. Write changes to database
   - `db.write()`
   - Write changes to database file. `write()` is automatically called by add, delete, and update.

