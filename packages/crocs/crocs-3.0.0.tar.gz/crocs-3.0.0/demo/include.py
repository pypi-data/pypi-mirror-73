from crocs.regex import Pattern, Include,Any

e = Any(Include('a', 'b', 'c'), '1')

regstr = e.mkregex()
print(regstr)


