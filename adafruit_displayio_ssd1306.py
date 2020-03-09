# The MIT License (MIT)
#
# Copyright (c) 2019 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_displayio_ssd1306`
================================================================================

DisplayIO driver for SSD1306 monochrome displays


* Author(s): Scott Shawcroft

Implementation Notes
--------------------

**Hardware:**

* `Monochrome 1.3" 128x64 OLED graphic display <https://www.adafruit.com/product/938>`_
* `Monochrome 128x32 I2C OLED graphic display  <https://www.adafruit.com/product/931>`_
* `Monochrome 0.96" 128x64 OLED graphic display <https://www.adafruit.com/product/326>`_
* `Monochrome 128x32 SPI OLED graphic display <https://www.adafruit.com/product/661>`_
* `Adafruit FeatherWing OLED - 128x32 OLED <https://www.adafruit.com/product/2900>`_

**Software and Dependencies:**

* Adafruit CircuitPython (version 5+) firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_SSD1306.git"

# Sequence from page 19 here: https://cdn-shop.adafruit.com/datasheets/UG-2864HSWEG01+user+guide.pdf
_INIT_SEQUENCE = (
    b"\xAE\x00"  # DISPLAY_OFF
    b"\x20\x01\x00"  # Set memory addressing to horizontal mode.
    b"\x81\x01\xcf"  # set contrast control
    b"\xA1\x00"  # Column 127 is segment 0
    b"\xA6\x00"  # Normal display
    b"\xc8\x00"  # Normal display
    b"\xA8\x01\x3f"  # Mux ratio is 1/64
    b"\xd5\x01\x80"  # Set divide ratio
    b"\xd9\x01\xf1"  # Set pre-charge period
    b"\xda\x01\x12"  # Set com configuration
    b"\xdb\x01\x40"  # Set vcom configuration
    b"\x8d\x01\x14"  # Enable charge pump
    b"\xAF\x00\x00"  # DISPLAY_ON
)

# pylint: disable=too-few-public-methods
class SSD1306(displayio.Display):
    """SSD1306 driver"""

    def __init__(self, bus, **kwargs):
        # Patch the init sequence for 32 pixel high displays.
        init_sequence = bytearray(_INIT_SEQUENCE)
        height = kwargs["height"]
        if "rotation" in kwargs and kwargs["rotation"] % 180 != 0:
            height = kwargs["width"]
        init_sequence[16] = height - 1  # patch mux ratio
        if kwargs["height"] == 32:
            init_sequence[25] = 0x02  # patch com configuration
        super().__init__(
            bus,
            init_sequence,
            **kwargs,
            color_depth=1,
            grayscale=True,
            pixels_in_byte_share_row=False,
            set_column_command=0x21,
            set_row_command=0x22,
            data_as_commands=True,
            set_vertical_scroll=0xD3,
            brightness_command=0x81,
            single_byte_bounds=True,
        )
