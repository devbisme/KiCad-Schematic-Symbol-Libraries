# README

This is just a repository of KiCad schematic symbol libraries developed at XESS.

* `Lattice_iCE_FPGA.lib` currently contains the Lattice iCE40 HX FPGAs. (**More coming soon!**)
* `Cypress_PSoC.lib` contains a few Cypress PSoC 5LP chips.
* `Cypress_cy8c5xlp.lib` contains **all** the Cypress PSoC5LP chips.
* `xilinx6s.lib` contains **all** the Xilinx Spartan-6 FPGAs.
* `xilinx6v.lib` contains **all** the Xilinx Virtex-6 FPGAs.
* `xilinx7.lib` contains **all** the Xilinx 7-Series FPGAs (Zynq, Artix, Kintex and Virtex).
* `xess.lib` contains a grab-bag of parts, many auto-converted from Eagle. 

**Some of the schematic symbols in these libraries have changed!**
If you previously downloaded and used a library, you may find a newer version has differences
like rearranged pins.
**Including a changed library in an existing schematic could cause errors!**
Either checkout the library that corresponds to the one you've already been using
(look at the check-in dates), or verify that the symbols from the new library attach to the correct
nets in your schematic.
