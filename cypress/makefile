psoc := CY8C5XLP
			
Cypress_cy8c5xlp.lib : $(psoc:=.csv)
	kipart $^ -r psoc5lp -b -s name -o $@ -w
	mv -f $@ ..

clean:
