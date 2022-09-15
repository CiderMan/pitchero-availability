# pitchero-availability

At the time of writing, Pitchero does not provide a means of exporting the player availability as
a text file (or in any other format). This script is a quick and dirty means of achieving this,
albeit with a couple of simple manual steps.

## Running it

1. Go to the Pitchero availability page (which has a URL of the form
`https://www.pitchero.com/admin/club/<club ID>/teams/availability`) and make sure that the
date of interest is the first column on the page
2. Save the page in the default HTML form (_not_ as a single file)
3. Run this script, giving the name of the HTML file as an argument
4. Marvel at the finest, handcrafted ASCII output

For example:
```
$ availability.py availability.html
Showing availability for 2022-09-18:

Available:
    A Player
    Another Player

Not sure:
    Some Player

Unavailable:
    Non Player

Not set:
    Ex Player
```

### Windows

Note that, on Windows, you may need to run it using the python launcher: `py availability.py availability.html`

## Changing it

There are currently no tests, in the hope that this workaround will not be needed for long...

The code has been formatted with [black](https://github.com/psf/black) and the options `-l 99`

The code has passed [pylint](https://github.com/PyCQA/pylint) with version 2.9.4
