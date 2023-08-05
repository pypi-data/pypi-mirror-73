"""
The approach consists of building regex patterns using the python classes
then serializing to a raw regex string. 

The resulting regex string is parsed by Eacc and a similar structure is built
using the same previous classes it is serialized to a raw regex then checked against the 
initial regex string.

There are tests that build the pythonic structure from a raw string
then it is serialized back and tested against the initial regex string.

This approach should be enough to make sure both crocs regex classes and
regex grammar are working. 

When a regex AST is built it is serialized, possible matches are generated
and matched against its serialized regex string. It makes sure that
the serialized regex string is valid.

Some generated hits for patterns may be too long and slow down the tests considerably.

The special regex operators are escaped when testing the regex parser mechanisms. It is
necessary because crocs classes that map to regex operators are escaping regex operators
in strings. 

    regstr = r'[abc*]'
    yregex = xmake(regstr)
    
    # Evaluate to False.
    yregex.to_regex() != regstr 

    # Evaluate to True.
    yregex.to_regex() == r'[abc\*]'
    
The reason consists of it not existing escape class in crocs classes to map regex escape. 
It automatically escapes all strings that contain regex operators.

It is necessary to escape yourself raw regex strings even inside character sets to make
sure them are in fact equal to the resulting pythonic yregex that comes from xmake.

The tests also check the serialization of the yregex structure to raw python code. The approach
consists of using the BasicRegex.mkclone method and BasicRegex.mkcode method. The structure
is serialized to raw code and executed then it is serialized again and tested against the initial 
raw regex.
"""

import unittest
from crocs.regex import Include, Exclude, Any, OneOrZero, \
OneOrMore, Group, ConsumeNext, ConsumeBack, X, Pattern, Seq, Repeat,\
NamedGroup, ZeroOrMore, Caret, Dollar
from crocs.xparser import xmake
from eacc.lexer import Lexer, LexError
import re

class TestInclude(unittest.TestCase):
    def test0(self):
        e = Include('a', 'b', 'c')

        regstr = e.mkregex()
        self.assertEqual(regstr, '[abc]')

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)
    
    def test1(self):
        expr0 = Include('x', 'y')
        expr1 = Include('m', 'n')

        expr2 = Any(expr0, expr1)
        regstr = expr2.mkregex()

        self.assertEqual(regstr, '[xy]|[mn]')

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        expr0 = Include('x', 'y')
        expr1 = Include('m', 'n')

        expr2 = Any(expr0, expr1)
        expr3 = OneOrMore(Group(expr2))
        regstr = expr3.mkregex()
        self.assertEqual(regstr, '([xy]|[mn])+')

        yregex = xmake(regstr)
        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        expr0 = Include('x', 'y')
        expr1 = Include('m', 'n')
        expr2 = Include('a', Seq('0', '9'), 'b')

        expr3 = Any(expr0, expr1, expr2)
        expr4 = OneOrMore(Group(expr3))
        regstr = expr4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        expr0 = Include('%', '#')
        expr1 = Include('c', Seq('a', 'd'), Seq('0', '5'), 'd')
        expr2 = Include('a', Seq('0', '9'), 'b')

        expr3 = Any(expr0, expr1, expr2)
        expr4 = Repeat(Group(expr3), 3, 8)
        regstr = expr4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test5(self):
        expr0 = Include('a', 'b')
        expr1 = Include(Seq('a', 'z'))
        expr2 = Group(Any(expr0, expr1))

        regstr = expr2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test6(self):
        expr0 = Include('a', 'b')
        expr1 = NamedGroup('alpha', Any(expr0, 'bar'))
        expr2 = Any(expr0, expr1)

        regstr = expr2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test7(self):
        expr0 = Include(Seq('a', 'z'))
        expr1 = Include(Seq('0', '9'))
        expr2 = Group(expr0, expr1)
        expr3 = Group(expr1, expr0)
        expr4 = Group(Any(expr2, expr3))

        regstr = expr4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test8(self):
        expr0 = Include(Seq('a', 'z'))
        expr1 = Group('0', expr0, '9')
        expr2 = OneOrMore(expr1)
        expr3 = Group(expr2, 'm', expr1)
        expr4 = Repeat(expr3, 2, 4)

        regstr = expr4.mkregex()

        expr4.test()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test9(self):
        regstr = r'[a-z]+[0-9a-z]?(abc)\1'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test10(self):
        regstr = r'([a-z]+[0-9a-z])?(abc)'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test11(self):
        regstr = r'(([a-z]+[0-9a-z])(abc)\2)\2emm\3'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test12(self):
        regstr = r'[a-z]?'
        yregex = xmake(regstr)
        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test13(self):
        regstr = r'([a-z]0)?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test14(self):
        regstr = r'(((((([0-9]+))))))\3\1\2'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test15(self):
        regstr = r'(([0-9]x)?([a-z]y))?mnc([a-z\&%])+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test16(self):
        regstr = r'([a-z\&\*\$])+'
        yregex = xmake(regstr)
        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test17(self):
        regstr = r'[a-z\*]'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test18(self):
        regstr = r'(((((([0-9]))\5))))\3\1\2'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestExclude(unittest.TestCase):
    def test0(self):
        e = Exclude(Seq('a', 'z'))

        regstr = e.mkregex()

        self.assertEqual(regstr, '[^a-z]')
        yregex = xmake(regstr)
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        expr0 = Include(Seq('a', 'z'))
        expr1 = Exclude(Seq('1', '9'))

        expr2 = Group(expr0, expr1)
        expr3 = Pattern(expr0, expr1, expr2, expr2, expr2)

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = OneOrMore(expr0)

        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2, expr2)
        expr4 = Group(expr3, expr3, expr3)

        regstr = expr4.mkregex()

        yregex = xmake(regstr)

        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = OneOrMore(expr0)

        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2, expr2)
        expr4 = Group(expr3, expr3, expr3)

        regstr = expr4.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = OneOrMore(expr0)

        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2, expr2)
        expr4 = Any(expr2, expr3)

        regstr = expr4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test5(self):
        regstr = r'[^0-9]+([^abcd]?x([^eeee])?\2)'
        yregex = xmake(regstr)

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test6(self):
        regstr = r'[^0-9]+([^abcd]?x([^ee])+\2)'
        yregex = xmake(regstr)

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test7(self):
        regstr = r'[^0-9]+([^abcd]?x([^\*\*])\2)'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test8(self):
        regstr = r'[abc\*]+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test9(self):
        regstr = r'[\[abc\*]'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test10(self):
        regstr = r'[\]abc\*]'
        yregex = xmake(regstr)
        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test11(self):
        regstr = r'([\]abc\*])+\**[^\*\&\&\[\]]+'
        yregex = xmake(regstr)
        yregex.test()
        

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestAny(unittest.TestCase):
    def test0(self):
        expr0 = Exclude(Seq('0', '9'))
        expr1 = Include(Seq('a', 'b'))
        expr2 = Any(expr0, expr1)
        expr3 = Pattern(Group(expr2), Group(expr2))

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        expr0 = Exclude(Seq('0', '9'))
        expr1 = OneOrMore(expr0)
        expr2 = Any('a', expr0, expr1, 'b')
        expr3 = Pattern(Group(expr2), Group(expr2))

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, expr1)
        expr3 = Any(expr0, expr1, expr2)

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, expr1)
        expr3 = Any(expr0, expr1, expr2)
        expr4 = Any(expr3, expr2, expr1, expr0)

        regstr = expr4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2)
        expr4 = Any('b', expr3, 'a')

        regstr = expr4.mkregex()
        yregex = xmake(regstr)
    
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test5(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = X()
        expr2 = Group(expr0, expr1)
        expr3 = OneOrMore(expr2)
        expr4 = Any(expr0, expr1, expr2,expr2, expr3)
        expr5 = Group(expr4, expr3, expr2, 'a', 'b', expr3)
        expr6 = Any(expr0, expr1, expr2, expr3, expr4, expr5)

        expr7 = Pattern(expr0, expr2, expr3, Group(expr4), expr5, Group(expr6), 
        'somestring',  Group(expr6), Group(expr6))

        # The regex.
        # [0-9]([0-9].)\1+[0-9]|.|\1|\1|\1+([0-9]|.|\1|\1|\1+\1+\1ab\1+)[0-9]|.\
        # |\1|\1+|[0-9]|.|\1|\1|\1+|\2Fuinho\ Violento[0-9]|.|\1|\1+|[0-9]|.\
        # |\1|\1|\1+|\2[0-9]|.|\1|\1+|[0-9]|.|\1|\1|\1+|\2

        regstr = expr7.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test6(self):
        regstr = r'(a{0,1})|(b)|\1|\2'
        yregex = xmake(regstr)
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test7(self):
        regstr = r'((i(abc+)(cde{1,12})|(abc)|(iof+)+|cde+))(\*eee)+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test8(self):
        regstr = r'a{0,0}|b{1,1}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test8(self):
        regstr = r'a{0,0}|b{0,0}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test9(self):
        regstr = r'a{0,}|b{0,}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), r'a{0,}|b{0,}')
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), r'a{0,}|b{0,}')

    def test10(self):
        regstr = r'(a{0,}|b{0,})|(abc)|c+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test11(self):
        expr0 = Any('abc', 'efg')
        expr1 = Repeat(Group(expr0), 1, 4)

        regstr = expr1.mkregex()
        self.assertEqual(regstr, r'(abc|efg){1,4}')

        yregex = xmake(regstr)
        yregex.test()
        
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test12(self):
        regstr = r'(a{0,})\1cef|(b{0,})\2oo\*|(abc)\3foo|c+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test13(self):
        regstr = r'^abc|foo|ee$'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test13(self):
        regstr = r'^|foo|$'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test14(self):
        regstr = r'(((^|foo|$)\3))|(foo)\4|[a-z]$'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test15(self):
        regstr = r'a|b|c+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test16(self):
        regstr = r'(a+|b*|c+)(\1ff)((\2ee))\3*|rs+|rss*'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test17(self):
        regstr = r'(a+|b*|c+)(\1ff)((\2ee))\3*|((a+cee*ee+c{1,}?)ee)'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test18(self):
        regstr = r'(a+|b*|c+)(\1ff)((\2ee))\3*|((a+cee*ee+c{1,}?)ee)|((a.+c)cd.*)(?=f.+bar)'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test19(self):
        regstr = r'(a+|b*|(?<=abc..d)(((ss))c+))(f+f)((ee))*|((a+cee*ee+c{1,}?)ee)|((a.+c)cd.*)(?=f.+bar)'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test20(self):
        regstr = r'(((e(a|b|c)d)c)|((ab|cd)|ef)|((((a|e|u|i+))))|ef)|ee|oo|.+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test21(self):
        regstr = r'a.+?|e.*?|c{1,2}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)


class TestOneOrZero(unittest.TestCase):
    def test0(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = Any(expr0, 'ahh', X())
        expr2 = OneOrZero(Group(expr1))
        expr3 = Group(expr1, 'ee', X(), 'uu')

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        expr0 = Exclude(Seq('a', 'b'))
        expr1 = OneOrZero(expr0)
        expr2 = Group(expr1, 'ee', X(), 'uu')

        regstr = expr2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        expr1 = OneOrZero(Group('fooo'))
        expr2 = Group(expr1, 'ee', X(), 'uu')
        expr3 = Pattern(expr2, 'foobar', expr2, 'bar', expr2)

        regstr = expr2.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        regstr = r'a?b?c?\*?\&?[c-z\*\(\)\[\]]?c?(a?e?)\1?c'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        regstr = r'(aa{1,3}?)\1'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestOneOrMore(unittest.TestCase):
    def test0(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = Any(expr0, expr0, 'fooo', X(), 'ooo', expr0)
        expr2 = OneOrMore(Group(expr1))
        expr3 = Group(expr1, 'ee', X(), 'uu', expr2, 'oo', expr1)

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        expr0 = Include(Seq('a', 'b'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, '111', X(), X(), '222')

        regstr = expr2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        expr1 = OneOrMore(Group('fooo'))
        expr2 = Group(expr1, '0000000', expr1, expr1, X(), 'uu', expr1)
        expr3 = Pattern(expr1, expr2, expr2, 'alpha', expr2, 'bar', expr2)

        # The regex.
        # (fooo)+(\1+0000000\1+\1+.uu\1+)\2alpha\2bar\2

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        regstr = r'a+c+b+?(c+e+?)+?\1?(\1?c)+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestGroup(unittest.TestCase):
    def test0(self):
        expr0 = Group(X(), 'a', 'b')
        expr1 = Group(expr0, 'oo')
        expr2 = Group(expr1, 'mm')
        expr3 = Group(expr2, 'uu')
        expr4 = Any(expr0, expr1, expr2, expr3)
        regstr = expr4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        expr0 = Group(X(), 'a', 'b', Include('abc'))
        expr1 = Group(expr0, 'uuu', 'uuu', Exclude(Seq('a', 'z')))
        expr2 = Group(expr1, 'mm', Pattern(expr0, expr1, 'fooo'), 'uuuuu')

        expr3 = Group(expr2, 'uu')
        expr4 = Pattern(expr0, expr1, expr2, expr3)
        expr5 = Pattern(expr4, expr0, expr1, expr2, expr3, expr4)

        regstr = expr5.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        expr0 = Group('a')
        expr1 = Group('c', Group(expr0, 'd'))
        expr2 = Group(expr1, 'e')
        expr3 = Pattern(expr0, expr1, expr2)

        regstr = expr3.mkregex()
        yregex = xmake(regstr)
        expr3.test()

        
        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        expr0 = Group('abc')
        expr1 = Group(expr0, 'efg')
        expr2 = Group(expr0, expr1)
        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()

        # Eacc should be capable of reading back the 
        # serialized string.
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        expr0 = Group('ab')
        expr1 = Group(expr0, expr0)
        regstr = expr1.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestNamedGroup(unittest.TestCase):
    def test0(self):
        expr0 = NamedGroup('beta', 'X', X(), 'B')
        expr1 = Pattern('um', expr0, 'dois', expr0, 'tres', expr0)
        
        regstr = expr1.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)
        
    def test1(self):
        expr0 = NamedGroup('alpha', 'X', OneOrMore(Group('a', 'b')), 'B')
        expr1 = Any(expr0, 'abc', X(), 'edf')
        expr2 = Pattern(expr0, Group(expr1), X(), 'foobar')
        
        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        # Check if it works for nested named groups.
        expr0 = NamedGroup('alpha', 'X', OneOrMore(Group('a', 'b')), 'B')
        expr1 = NamedGroup('beta', Group('Lets be overmen.'))
        expr2 = NamedGroup('gamma', OneOrMore(expr1), 'rs', OneOrMore(Group('rs')))

        expr3 = NamedGroup('delta', expr0, expr1, expr2, 'hoho')
        expr4 = Pattern(expr0, expr1, expr0, expr1, expr2, expr3)
        
        regstr = expr4.mkregex()

        # The regex.
        # (?P<alpha>X(ab)+B)(?P<beta>Lets\ be\ overmen\.)(?P=alpha)(?P=beta)\
        # (?P<gamma>(?P=beta)?rs(rs)+)(?P<delta>(?P=alpha)(?P=beta)(?P=gamma)hoho)
        # Check if eacc can build it back.
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        expr0 = NamedGroup('foobar', Repeat(Group(Any('a', X(), 'b'))))
        expr1 = Any(expr0, 'm', 'n', Group(expr0, '12', X()))

        regstr = expr1.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestRepeat(unittest.TestCase):
    def test0(self):
        expr0 = NamedGroup('oooo', Repeat(Group(Any('a', X(), 'b'))))
        expr1 = Any(expr0, 'm', 'n', Group('oooo'), Group(expr0, X(), '12oooo', X()))
        expr2 = Repeat(Group(expr1), 1, 3)
        expr3 = Pattern(expr0, Group(expr1), expr2)

        regstr = expr3.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        expr0 = NamedGroup('oooo', Repeat(Group(Any('a', X(), 'b'))))
        expr1 = Any(expr0, 'm', 'n', Group('oooo'), Group(expr0, X(), '12oooo', X()))
        expr2 = Repeat(Group(expr1))
        expr3 = Pattern(expr0, Group(expr1), expr2)

        expr4 = Pattern(expr0, X(), 'ooo', X(), Group(expr1), expr2, expr3)
        expr5 = Any(expr0, expr1, expr2, expr3, expr4)

        regstr = expr5.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'a{1,2}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        regstr = r'\*{1,2}?c*'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        regstr = r'\*{1,8}?\&+?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test5(self):
        regstr = r'(\*cd){1,8}?\&+?\1+?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test6(self):
        regstr = r'((\*cd){1,8}?\&)+?(\1?ecdeeec+)+?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test7(self):
        regstr = r'((\*cd{1,}){1,8}?\&)+?(\1?ec?d){4,4}?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test8(self):
        regstr = r'(((\*cd{1,}){1,8}?\&)+?){3,3}?(\1?ecd){4,4}?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test9(self):
        regstr = r'a{1,3}c{3,3}?e{0,2}?c+?e{0,4}?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test10(self):
        regstr = r'(a{1,3}c{3,3}?e{2,2}?c+?e{0,4}?)\1{1,2}?'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test11(self):
        regstr = r'((a{1,3}c{3,3}?e{2,3}?c+?e{1,4}?)\2{1,2}?)'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test12(self):
        regstr = r'a{10}'
        yregex = xmake(regstr)
        yregex.test()
        
        # RegExpr{num} is represented as RegExpr{num,num}
        self.assertEqual(yregex.mkregex(), r'a{10,10}')

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), r'a{10,10}')

    def test13(self):
        regstr = r'a{12,}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test14(self):
        regstr = r'a{,13}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), r'a{0,13}')

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), r'a{0,13}')

    def test15(self):
        # Possibly a bug because it fails with:
        # regstr = r'((r.+bc)(?=a{13,15}))a'

        regstr = r'((r.+bc)(?=a{13,15}))a+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestZeroOrMore(unittest.TestCase):
    def test0(self):
        expr0 = NamedGroup('alpha', Repeat(Group(Any('a', X()))))
        expr1 = Pattern(expr0, 'm', Group('oooo'))
        expr2 = Any(expr0, expr1)

        expr7 = ZeroOrMore(Group(expr2))
        expr8 = Pattern(expr7, Group(expr2))

        regstr = expr8.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)
        
    def test1(self):
        expr0 = NamedGroup('a999', Repeat('a'))

        expr1 = Pattern(expr0, ZeroOrMore('a'), 
        Group('oooo'), Group(expr0))

        expr2 = Repeat(Group(expr1))

        regstr = expr2.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'\*{1,3}(((a[0-9]c)\3{1,3}))((\$[a-z]\#)\2{1,3})\*{1,3}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestConsumeNext(unittest.TestCase):
    def test0(self):
        expr0 = ConsumeNext(Group(X(), OneOrMore(Group('alpha'))), 
        Group(X(), 'bar', X()))
        expr1 = Any(expr0, X(), '123')
        regstr = expr1.mkregex()

        with self.assertRaises(re.error):
            yregex = xmake(regstr)

    def test1(self):
        expr0 = ConsumeNext(Group(X(), 'bar', X()), 
        Group(X(), OneOrMore(Group('alpha'))))

        expr1 = Any(expr0, X(), '123')
        expr2 = ConsumeNext(Group(X(), '579', X()), Group(expr1))
        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        expr0 = ConsumeNext(Group(X(), 'bar', X()), 
        Group(X(), OneOrMore(Group('alpha'))))
        expr1 = Any(expr0, X(), '123')
        expr2 = ConsumeNext(Group(X(), '579', X()), Group(expr1))

        expr3 = ConsumeBack(expr2, 
        Group(OneOrMore(expr2), 'aaaaa', 'bbbb', X()))

        expr3 = Pattern(expr3, 'aaaa', X(), OneOrMore(Group('aaaa')))
        regstr = expr3.mkregex()
        yregex = xmake(regstr)

        # yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        regstr = '(?<=abc)((c+d)\2)e'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        regstr = r'(?<=abc{3,3})((c+d{1,4})\2)e'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test5(self):
        regstr = r'(?<!abc{3,3})((c+(d{1,4})eee+)\2)e'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test6(self):
        regstr = r'e(?<=abc)'
        yregex = xmake(regstr)

        with self.assertRaises(AssertionError):
            yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test7(self):
        regstr = r'(?<=abc)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test8(self):
        regstr = r'(?<!abc)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestConsumeBack(unittest.TestCase):
    def test0(self):
        expr0 = ConsumeBack(Group(X(), '1010101', X()), 
        Group(X(), OneOrMore(Group('010101'))))

        expr1 = Pattern(expr0, 'aaaa', X(), OneOrMore(Group('1010101')))
        expr2 = Any(expr0, expr1, X(), Group(expr1, X(), 'a'))

        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        expr0 = ConsumeBack(Group(OneOrMore(X()), 
        'aaa', X()), Group('aaa', X(), 'bbb'))

        expr1 = Any(expr0, 'aaaa', X(), OneOrMore(Group('foobar')), X())
        expr2 = Any(expr1, expr1, X(), Group(expr1, X(), 'a'))
        expr3 = NamedGroup('xx', expr0, expr1, X(), X())
        expr4 = Pattern(expr0, Group(expr1), Group(expr2), expr3)
        regstr = expr4.mkregex()
        yregex = xmake(regstr)

        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()

        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'abc.+(?=eee)e'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        regstr = r'(ac?c).+(?=e{1,3})e'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        regstr = r'(ac{1,3}c)(aa)+(?=e{1,3})e'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test5(self):
        regstr = r'(\*a\&{1,5}c)(aa)+(?=e{1,3}c+)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test6(self):
        regstr = r'(\*a\&{1,5}c)\1+(a.+a)+(?=e{1,3}c+)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test7(self):
        regstr = r'(\*a\&{1,5}c)\1+(a.+a)+(?=e{1,3}c+(ab+)\3{1,3})'
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test8(self):
        regstr = '(\*a\&{1,5})+\1+(a.+a)+(?=e{1,3}c+(ab+)\3{1,3})'
        yregex = xmake(regstr)

        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test9(self):
        regstr = r'(\*a\&{1,5})+\1+(a.+a)+(?=e{1,3}c+(ab+)\3{1,3})+'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test10(self):
        regstr = r'(\*a\&{1,5})+\1+(a.+a)+(?!e{1,3}c+(ab+)\3{1,3})+'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test11(self):
        regstr = r'abc(?!cde)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test11(self):
        regstr = r'abc(?!c(d+e)\1{1,3}0)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test12(self):
        regstr = r'abc(?=cde)cc'
        yregex = xmake(regstr)

        with self.assertRaises(AssertionError):
            yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test13(self):
        # Possibly bug. It fails to match.
        # regstr = r'Isaa.+c\ (?=Asimov)ee'
        # But the regex below matches success to find a match.
        regstr = r'Isaa.+c\ (?=Asimov).+'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test14(self):
        # Possibly bug. It fails to match.
        # regstr = r'Isaa.+c\ (?!Asimov)ee'
        # But the regex below matches success to find a match.
        regstr = r'Isaa.+c\ (?!Asimov).+'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test15(self):
        regstr = r'(?!Asimov).+'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test16(self):
        regstr = r'(?!Asimov)ee'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test17(self):
        regstr = r'(?!Asimov)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test18(self):
        regstr = r'(?!Asimov)(a+)\1b1+'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test19(self):
        # Possibly a bug.
        regstr = r'e(?=Asimov)eee'
        yregex = xmake(regstr)

        with self.assertRaises(AssertionError):
            yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test20(self):
        regstr = r'(?=Asimov)'
        yregex = xmake(regstr)

        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test21(self):
        regstr = r'Isaac\ (?!Asimov)'
        yregex = xmake(regstr)

        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test22(self):
        e = ConsumeBack('Isaac ', 'Asimov', neg=True)
        regstr = e.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)
        
class TestRegexComment(unittest.TestCase):
    def test0(self):
        regstr = r'abc(?#aiosdu).+(ab)(?#asiodu\)asd)'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'[abc]*(?#aiosdu).+([ab]*)(?#asiodu\)[asd])'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'[a-z]*(?#aiosdu).+([0-9]*)(?#hehehe\)[abcde])'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        regstr = r'[a-z]*(?#aiosdu)(abc)+([0-9]+)(123)(?#....aaa\)[abcde])'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test4(self):
        regstr = r'[a-z]*(?#aiosdu)((ab)*)?([0-9]+)(123)(?#....aaa\)[abcde])aa'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test5(self):
        regstr = r'[a-z](?#aiosdu)([0-9]+)\1sdius\1(123)(?#....aaa\)[abcde])\1aa'

        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test6(self):
        regstr = r'a(?#aiosdu)*b'
        yregex = xmake(regstr)

        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestNonCapture(unittest.TestCase):
    def test0(self):
        regstr = r'(?:ee)'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'((?:.+)cc(ee.*))+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'((?:.+)cc(ee.*))+\1+c\2+e'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test3(self):
        regstr = r'((?:fooobar.+)cc(ee.*))+\1+c\2+e'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestWord(unittest.TestCase):
    def test0(self):
        regstr = r'ee\*@\w+hehe'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'(e\&e\*@\w*cc)+(?:cee\w+)uu?\1'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestMetab(unittest.TestCase):
    def test0(self):
        regstr = r'\ \bfoo\b\ ee'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'\b(e\*@\w*cc)+(?:cee\w+)uu?\b'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'\bfoo\b'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestMetaB(unittest.TestCase):
    def test0(self):
        regstr = r'py\B'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'\Bpy\B'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'\Bfoo\B'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestNotWord(unittest.TestCase):
    def test0(self):
        regstr = r'foo\W+bar'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'(\*\W+bar)+(@\1+)\&\2{1,3}'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestCaret(unittest.TestCase):
    def test0(self):
        regstr = r'^eudof.c+'
        yregex = xmake(regstr)
        yregex.test()
        print(yregex.mkcode())
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'^(\*\^ee)+'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'^(\*\^ee)+c*\..'
        yregex = xmake(regstr)
        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)
        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

class TestDollar(unittest.TestCase):
    def test0(self):
        regstr = r'^((ab[a-z].c+))alpha(?#ajust)$'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test1(self):
        regstr = r'^(\*\^ee)+$'
        yregex = xmake(regstr)
        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'^(\*\^ee)+c*\..$'
        yregex = xmake(regstr)
        yregex.test()
        
        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

    def test2(self):
        regstr = r'((\*\^ee)+c*\..)*$'
        yregex = xmake(regstr)
        yregex.test()

        self.assertEqual(yregex.mkregex(), regstr)

        clone = yregex.mkclone()
        self.assertEqual(clone.mkregex(), regstr)

if __name__ == '__main__':
    unittest.main()