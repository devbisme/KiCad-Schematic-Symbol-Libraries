# README

This is a repository of KiCad schematic symbol libraries developed at XESS.

* `Cypress_PSoC.lib` contains a few Cypress PSoC 5LP chips.
* `Cypress_cy8c5xlp.lib` contains **all** the Cypress PSoC5LP chips.
* `gowin_fpga.lib` contains **all** the GOWIN FPGAs.
* `Lattice_ECP5_FPGA.lib` contains the Lattice ECP5 & ECP5-5G FPGAs.
* `Lattice_iCE_FPGA.lib` contains the Lattice iCE40 HX, LM, LP & Ultralight FPGAs.
* `pic32.lib` contains the PIC32 MX 1XX/2XX 28/36/44-pin microcontrollers.
* `wch.lib` contains the WCH CH54* and CH55* 8051 microcontrollers.
* `xess.lib` contains a grab-bag of parts, many auto-converted from Eagle. 
* `xilinx6s.lib` contains **all** the Xilinx Spartan-6 FPGAs.
* `xilinx6v.lib` contains **all** the Xilinx Virtex-6 FPGAs.
* `xilinx7.lib` contains **all** the Xilinx 7-Series FPGAs (Zynq, Artix, Kintex, Spartan and Virtex).
* `xilinxultra.lib` contains **all** the Xilinx Ulatrascale FPGAs (Zynq, Kintex and Virtex).


## But I Don't Like How the Symbols Look!

OK, people are picky. Maybe even more picky when they're getting something for free.
(There's probably a psychology paper in there, somewhere.)

The good thing is: *you can change these schematic symbols!*
Obviously you can modify any individual symbol using the KiCad schematic symbol editor.
But you can also make library-wide changes using the [`kipart`](https://pypi.org/project/kipart/) utility as follows:

1. Use the `kilib2csv` utility to convert one or more of the libraries into a CSV file.
2. Open the CSV file as a spreadsheet and reorder the pins, change pin types, assign pins to different units, etc.
3. Finally, run `kipart` on the modified CSV file to create your own custom library.
4. Bask in the glory of your own originality.


**Some of the schematic symbols in these libraries have changed!**
If you previously downloaded and used a library, you may find a newer version has differences
like rearranged pins.
**Including a changed library in an existing schematic could cause errors!**
Either checkout the library that corresponds to the one you've already been using
(look at the check-in dates), or verify that the symbols from the new library attach to the correct
nets in your schematic.
