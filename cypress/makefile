psoc := cy8c5xlp
			
Cypress_cy8c5xlp.lib : $(psoc:=.csv)
	kipart $^ -r psoc5lp -b -s name -o $@ -w
	mv -f $@ ..

clean:
