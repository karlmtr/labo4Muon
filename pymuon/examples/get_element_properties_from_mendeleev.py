""".. moduleauthor:: Sacha Medaer"""

from mendeleev import element


print('Type the element symbol followed by Enter:')
while True:
    el_str = str(input())
    try:
        elem = element(el_str)
    except:
        print('Element symbol not found, try again:')
    else:
        print('The element {} has the following properties:'.format(el_str))
        print('Atomic number: ', elem.atomic_number)
        print('Mass number: ', elem.mass_number)
        print('Density: ', elem.density, ' g/cm^3')
        print('\nType the next element symbol:')
