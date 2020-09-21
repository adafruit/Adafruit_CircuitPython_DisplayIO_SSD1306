Introduction
============
DisplayIO driver for SH1107 monochrome displays. DisplayIO drivers enable terminal output. This driver depends on a future (TBD) quirk added to DisplayIO. 


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython Version 5+ <https://github.com/adafruit/circuitpython>`_
* Adafruit SH1107 128 x 64 OLED display, used for testing.

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example (to be updated)
=============

.. code-block:: python

    import board
    import displayio
    import adafruit_displayio_ssd1306
    import busio

    displayio.release_displays()

    # This pinout works on a Metro and may need to be altered for other boards.
    spi = busio.SPI(board.SCL, board.SDA)
    tft_cs = board.D9
    tft_dc = board.D8
    tft_reset = board.D7

    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset, baudrate=1000000)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

