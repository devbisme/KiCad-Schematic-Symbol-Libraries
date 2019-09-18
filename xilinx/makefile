.PHONY: update clean

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

update: 
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/usapackages/usaall.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/v7packages/v7all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/k7packages/k7all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/a7packages/a7all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/v6packages/v6all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/v5packages/v5all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/v4packages/v4all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/zuppackages/zupall.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/z7packages/z7all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/s7packages/s7all.zip
	wget -N --no-check-certificate http://www.xilinx.com/support/packagefiles/s6packages/s6all.zip

clean:

