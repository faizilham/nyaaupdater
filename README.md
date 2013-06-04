Nyaa.eu Feed Updater
====================

A Nyaa.eu torrent feed updater. Use Nyaa.eu search result URL to fetch new updates (i.e. you are following anime series in nyaa.eu and you want to get information of new episodes). Developed in Python 2.7.3

Project Contents
----------------

This project contains two main library and a sample code:

- `nyaa_parser.py`: For fetching and parsing nyaa.eu search page result
- `nyaa_db.py`:	For managing feed database.
- `nyaa_checklist.csv`: The feed database.
- `nyaa_check.py`: The sample code. It checks torrent updates and downloads `.torrent` files if new updates exist.

For more information, please check the [documentation](DOCUMENTATION.md).

The Nyaa.eu Feed Updater is a copyright (c) 2013 of [Faiz Ilham M](http://faizilham.com) and released under [The MIT License](LICENSE).
You may use, modify or distribute the code as long as you include the license notice.
