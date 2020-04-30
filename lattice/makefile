all : Lattice_ECP5_FPGA.lib Lattice_iCE_FPGA.lib 

ice := ice40pinouthx1k ice40pinouthx4k ice40pinouthx8k \
	ice40lm-1k_pinlist ice40lm-2k_pinlist ice40lm-4k_pinlist \
	ice40lp640 \
	ice40pinoutlp1k ice40pinoutlp4k ice40pinoutlp8k \
	ice40pinoutlp384 \
	ice40pinoutul1k ice5pinoutup3k ice5pinoutup5k\
	ice5pinoutlp1k ice5pinoutlp2k ice5pinoutlp4k

ecp5 := ECP5_pinouts.zip

Lattice_ECP5_FPGA.lib : ${ecp5}
	kipart $^ -r lattice -b -s name -o $@ -w
	mv -f $@ ..


Lattice_iCE_FPGA.lib : $(ice:=.csv)
	kipart $^ -b -s name -o $@ -w
	mv -f $@ ..

clean:
	rm -f $(ice:=.csv) $(ecp5:=.csv)

%.csv : %.xlsx
	python ice_xlsx_to_csv.py $^
