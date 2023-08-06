Munter.py
=========

Helps you speed up your tour and trip planning.

Disclaimer
----------

The time calculations produced by this program are not guaranteed to be
accurate. Any harm or hazard encountered due to blindly trusting these
estimates is your own fault.

Installation
------------

If you use pip, then simply `pip install munter.py`.

If you don't use pip, then download the source code and unpack it into
its own directory. You can invoke it directly via `python munter.py
[options]`.

How to use it
-------------

For detailed information, see:

`./munter.py --help`

The program supports both imperial and metric, and has four "travel
modes" at this time: uphill, flat, downhill, bushwhacking. It also
supports a simple fitness modifier: slow, average, fast.

By default, the output will be the time in hours and minutes of the
specified leg. If you prefer, you can use the `-p` switch to get a
"prettier" output.

There is also a GUI mode available, based on WxPython, which can be used
by simply invoking like so:

`./munter.py -g`

### Use as a library

You can also use Munter.py programmatically from Python, like so:

`import munter`  
`est = munter.time_calc(distance=3.2, elevation=2300, fitness='slow')`

This will store a value like "3.64914" in the `est` variable.

Workflow
--------

My workflow involves planning my tour using tools like ArcGIS or
CalTopo. Then, I take the stats between each leg (distance, vertical
gain/loss) of the tour and run them through Munter.py and record its
output to my field notebook.

The text-based "pretty" format can be directly transferred to e.g. the
format used by SnowPit Technologies' "Avalanche Field Notebook" or your
own personal format (e.g. RitR No. 471).

Future plans
------------

* Better documentation

Version History
---------------

- 2.3.0 (Jul 2020)

  Implement 'auto-start in GUI' feature.

  The program tries to detect whether it was invoked from a terminal or
  not, and if not, it will automatically switch to GUI mode. Useful for
  invocation via e.g. dmenu(1).

- 2.2.1 (Jun 2020)

  Complete fixes recommended by pylint(1).

- 2.2.0 (Jun 2020)

  Implement GUI mode.

- 2.1.0 (Jun 2020)

  Implement fitness modifier. Make some text changes and other
  miscellaneous and minor improvements.

- 2.0.1 (Jun 2020)

  README improvement.

- 2.0.0 (Jun 2020)

  Package for distribution as a standalone program (and library).

- 1.0.2 (Jun 2020)

  A few small bugfixes.

- 1.0.1 (Jun 2020)

  Add LICENSE and README.

- 1.0.0 (Jun 2020)

  First released version. Includes sensible defaults and a rudimentary CLI
  "GUI".

- pre-1.0.0 (Mar 2017)

  In use privately/internally since 2017.
