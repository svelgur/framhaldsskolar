!* innaimport v1.0.0 Helgi E. Eyjólfsson 14sep2020
program innaimport
	
	version 15.1
	syntax anything ,year(numlist max=1)

	import delimited `1' , delimiter(";") varnames(2)  clear

	format %010.0f kennitala 
	quietly destring ein*, replace dpcomma
	
	gen einingar = eináönnþrep + (eináönn * (30/17.5))

	sort kennitala einingar
	by kennitala (einingar), sort: gen heimskoli = einingar[_N]

	quietly gen heimaskoli = 1 if heimskoli == einingar
	quietly replace heimaskoli = 0 if heimaskoli ==.

	drop if heimaskoli==0
	
	gsort kennitala einingar -einlokiðánúvbrautþrep
	
	di _newline as text "Ár valið er " as result `year'
	di as text "Nemandi skipaður í heimsakóla"
	

	
	quietly nsplit kennitala, d(4 2 3 1)
	quietly gen aldur2 = `year'-2000-kennitala2 if kennitala4==0
	quietly replace aldur2 = `year'-1900-kennitala2 if kennitala4==9
	quietly replace aldur2 = 999 if kennitala1==0000
	quietly mvdecode aldur2, mv(999)
	drop kennitala1-kennitala4
	
	di _newline as text "Tví/margtekningum eytt" _newline as text "Fjölda eytt:"
	duplicates drop kennitala, force

	duplicates report kennitala
end
