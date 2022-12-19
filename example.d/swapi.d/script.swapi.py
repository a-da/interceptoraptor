from swapi import get_people

p1 = get_people('1')
assert p1
p2 = get_people(2)
assert p1
p3 = get_people(3)
assert p3
