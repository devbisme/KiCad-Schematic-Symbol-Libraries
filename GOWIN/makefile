gowin := gowin_pinouts
			
gowin_fpga.lib : $(gowin:=.zip)
	kipart $^ -r gowin -b -s name -o $@ -w
	mv -f $@ ..

clean:
