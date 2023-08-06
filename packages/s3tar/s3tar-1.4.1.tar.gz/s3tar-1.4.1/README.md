# s3tar
Pulls (filtered) files from S3 and adds them to a tar archive.

Creates the command line script `star`.

```
$ star --help

Usage: star [OPTIONS] PATH

  Generates a tar archive of S3 files.

  Files are selected by a path made up of 'bucket/prefix' and optionaly by a
  time-based and/or name filter.

  'profile' is the AWS CLI profile to use for accessing S3.  If you use
  chaim or cca then this is the alias name for the account.

  The time based filter relies on the files being named with ISO Formatted
  dates and times embedded in the file names.  i.e.
  'file.2020-03-04T12:32:21.txt' The regular expression used is:

      /.*[._-]{1}([0-9-]{10}T[0-9:]{8}).*/

  The 'start' and 'end' parameters can either be ISO formatted date strings
  or unix timestamps.  If only the date portion of the date/time string is
  given the time defaults to midnight of that day.

  The length parameter is a string of the form '3h', '2d', '1w' for,
  respectively 3 hours, 2 days or 1 week.  Only hours, days or weeks are
  supported.  The 'length' and 'end' parameters are mutually exclusive, give
  one or the other, not both.

  If neither the 'end' nor the 'length' parameter is given, the end time
  defaults to 'now'.

  If the 'start' parameter is not given no time filtering of the files is
  performed, and all files found down the path are copied across to the tar
  archive recursively.

  To use the last modified time stamp of the files rather than their names
  for filtering pass the '-M' flag.

  To use the name filter, pass in a partial string that object names must
  contain.

  The tar archive can be compressed using gzip, bzip2 or lzma. Defaults to
  gzip. Pass a one char string to the `-c` option of "g", "b", "z" or "n".
  "n" is no compression. The output tar archive will be named accordingly:
  ".tar.gz" for gzip, ".tar.bz2" for bzip2, ".tar.xz" for lzma and ".tar"
  for no compression.

  The output filename of the tar archive will be $HOME/<bucket name>.tar
  You can change this with the "-o" option.

  Using the "-q" switch will turn off all messages (except errors) apart
  from the final output of the full path of the tar archive that is created.

  Using the "-v" switch will make the program verbose, showing each file
  that is copied into the tar archive.

  Files in Glacier and Glacier Deep Archive are ignored.

Options:
  -c, --compression TEXT  optional compression ['b', 'g', 'n', 'z'], default
                          'g'

  -e, --end TEXT          optional end time
  -l, --length TEXT       optional time length (i.e. 1d, 3h, 4w)
  -M, --usemodified       use last modified time stamp rather than filename
                          for filtering

  -N, --name TEXT         optional name filter
  -o, --output TEXT       output file name (default: bucket name)
  -p, --profile TEXT      AWS CLI profile to use (chaim alias)
  -q, --quiet             be very quiet, only show the tar file name
  -s, --start TEXT        optional start time
  -v, --verbose           show files that are being copied
  --help                  Show this message and exit.

```

## Install
The script is python3 only (>=python3.6).

Install it under your python3 user directories with:

```
python3 -m pip install s3tar --user
```

If this is the first python3 user script you have you will have to adjust
your path.  The script location will be `$HOME/.local/bin` on a Linux
machine, so add that to you path in your shell init file e.g.

```
echo "export PATH=$HOME/.local/bin:$PATH" >>~/.bashrc
```

If your shell is bash.

To check that installed ok:

```
star --help
```

Should display the help text.

[modeline]: # ( vim: set ft=markdown tw=74 fenc=utf-8 spell spl=en_gb mousemodel=popup: )
