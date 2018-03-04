LIBS: xilinxultra.lib xilinx7.lib xilinx6s.lib xilinx6v.lib

xilinxultra.lib: zupall.zip usaall.zip
	kipart -r xilinxultra -s name -b -w -o $@ $^
	mv -f $@ ..
	
xilinx7.lib: s7all.zip a7all.zip k7all.zip v7all.zip z7all.zip
	kipart -r xilinx7 -s name -b -w -o $@ $^
	mv -f $@ ..

xilinx6s.lib: s6all.zip
	kipart -r xilinx6s -s name -b -w -o $@ $^
	mv -f $@ ..

xilinx6v.lib: v6all.zip
	kipart -r xilinx6v -s name -b -w -o $@ $^
	mv -f $@ ..

clean:

