manufacturers := gowin xilinx cypress lattice

all         : $(manufacturers:=.all)
clean       : $(manufacturers:=.clean)

%.all:
	$(MAKE) -C $(subst .all,,$@)

%.clean:
	$(MAKE) -C $(subst .clean,,$@) clean
