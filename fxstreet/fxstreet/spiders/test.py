import os

xpaths_address = [
        '//*[(@id = "fxit-h1title")]',
        '//*[contains(concat( " ", @class, " " ), concat( " ", "fxit-countryurl", " " ))]',
        '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-actual-value", " " ))]',
        '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-cons-value", " " ))]',
        '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-prev-value", " " ))]',
        '//*[contains(concat( " ", @class, " " ), concat( " ", "fxst-nextevent", " " ))]//*[contains(concat( " ", '
        '@class, " " ), concat( " ", "fxst-date-value", " " ))]'
        ]
print(len(xpaths_address))
items = ['name', 'country', 'real', 'consensus', 'previous', 'next_release']
xpaths_address_fixed = []
for xpath_number in xpaths_address:
    xpaths_address_fixed.append('normalize-space(' + xpath_number + '/text())')
print(xpaths_address_fixed)
