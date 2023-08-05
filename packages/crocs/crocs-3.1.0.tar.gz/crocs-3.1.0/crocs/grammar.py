from eacc.eacc import Rule, Grammar, T
from eacc.lexer import LexTok, XSpec, SeqTok, LexSeq
from eacc.token import TokVal, Plus, Minus, LP, RP, Mul, \
Comma, Sof, Eof, Char,  LB, RB, Pipe, Question, Equal, Hash,Comment, \
LBR, RBR, Dot, Escape, Lesser, Greater, Exclam, Caret, TokType, Num, String, \
Colon, Dollar

class RegExpr(TokType):
    pass

class GroupSymbol(TokType):
    pass

class GroupName(TokType):
    pass

class WordSymbol(TokType):
    pass

class NotWordSymbol(TokType):
    pass

class MetabSymbol(TokType):
    pass

class MetaBSymbol(TokType):
    pass


class RegexTokens(XSpec):
    t_escape = LexSeq(SeqTok(r'\\', Escape, discard=True), SeqTok(r'.', Char))
    t_word   = LexSeq(SeqTok(r'\\', Escape), SeqTok(r'w', WordSymbol))
    t_nword  = LexSeq(SeqTok(r'\\', Escape), SeqTok(r'W', NotWordSymbol))
    t_metab   = LexSeq(SeqTok(r'\\', Escape), SeqTok(r'b', MetabSymbol))
    t_metaB   = LexSeq(SeqTok(r'\\', Escape), SeqTok(r'B', MetaBSymbol))

    t_plus   = LexTok(r'\+', Plus)
    t_dot    = LexTok(r'\.', Dot)
    t_pipe   = LexTok(r'\|', Pipe)
    t_lparen = LexTok(r'\(', LP)
    t_rparen = LexTok(r'\)', RP)
    t_gref   = LexSeq(SeqTok(r'\\', Escape), SeqTok(r'[0-9]', Num))

    # t_lbracket = LexTok(r'\[', LB)
    # t_rbracket = LexTok(r'\]', RB)

    t_include = LexSeq(SeqTok(r'\[', LB), 
    SeqTok(r'(\\\[|[^\[])+', String), SeqTok(r'\]', RB))

    t_exclude = LexSeq(SeqTok(r'\[', LB), SeqTok(r'\^', Caret),
    SeqTok(r'(\\\[|[^\[])+', String), SeqTok(r'\]', RB))

    t_lbrace   = LexTok(r'\{', LBR)
    t_rbrace   = LexTok(r'\}', RBR)
    t_comma    = LexTok(r'\,', Comma)
    t_question = LexTok(r'\?', Question)
    t_caret    = LexTok(r'\^', Caret)
    t_dollar    = LexTok(r'\$', Dollar)

    t_colon    = LexTok(r'\:', Colon)
    t_mul      = LexTok(r'\*', Mul)

    # t_minus  = LexTok(r'\-', Minus)
    # t_hash  = LexTok(r'\#', Hash)
    t_equal   = LexTok(r'\=', Equal)
    t_exclam  = LexTok(r'\!', Exclam)
    t_lesser  = LexTok(r'\<', Lesser)
    t_greater = LexTok(r'\>', Greater)

    t_comment = LexSeq(SeqTok(r'\(', LP), 
    SeqTok(r'\?', Question), SeqTok(r'\#', Hash), 
    SeqTok(r'(\\\)|[^)])+', Comment), SeqTok(r'\)', RP))

    t_pngroup = LexSeq(SeqTok(r'\(', LP), 
    SeqTok(r'\?', Question), SeqTok(r'P', GroupSymbol),
    SeqTok(r'\<', Lesser), SeqTok(r'[a-zA-Z0-9]+', GroupName),
    SeqTok(r'\>', Greater))

    t_ngref = LexSeq(SeqTok(r'\(', LP), 
    SeqTok(r'\?', Question), SeqTok(r'P', GroupSymbol),
    SeqTok(r'\=', Equal), SeqTok(r'[a-zA-Z0-9]+', GroupName),
    SeqTok(r'\)', RP))

    t_char = LexTok(r'.', Char)

    root = [t_gref, t_colon, t_ngref, t_comment, t_word, t_nword, t_metab, 
    t_metaB, t_escape, t_pngroup, t_plus, t_dot, t_lparen, t_rparen, t_mul, 
    t_exclude, t_include, t_lbrace, t_rbrace, t_comma, t_question, t_dollar, 
    t_caret, t_pipe, t_equal, t_lesser, t_greater, t_exclam, t_char]

class RegexGrammar(Grammar):
    # r_escape  = Rule(Escape, Char, type=Char)

    # No easy way out.
    o_pipe0 = Rule(LP)
    o_pipe1 = Rule(Mul)
    o_pipe2 = Rule(Question)
    o_pipe3 = Rule(LBR)
    o_pipe4 = Rule(LB)
    o_pipe5 = Rule(Char)
    o_pipe6 = Rule(Dot)
    o_pipe7 = Rule(Plus)
    o_pipe8 = Rule(Escape)
    o_pipe9 = Rule(Dollar)

    r_pipe  = Rule(T(RegExpr), Pipe, T(RegExpr), type=RegExpr, 
    up=(o_pipe0, o_pipe1, o_pipe2, o_pipe3, o_pipe4, o_pipe5, o_pipe6, 
    o_pipe7, o_pipe8, o_pipe9))

    r_group  = Rule(LP, T(RegExpr, type=RegExpr), RP, type=RegExpr)
    r_ngroup = Rule(LP, Question, GroupSymbol,
    Lesser, GroupName, Greater, T(RegExpr), RP, type=RegExpr)

    r_word  = Rule(Escape, WordSymbol, type=RegExpr)
    r_nword  = Rule(Escape, NotWordSymbol, type=RegExpr)
    r_metab  = Rule(Escape, MetabSymbol, type=RegExpr)
    r_metaB  = Rule(Escape, MetaBSymbol, type=RegExpr)

    # Non capturing group.
    r_ncapture  = Rule(LP, Question, Colon, T(RegExpr, type=RegExpr), RP, type=RegExpr)

    r_dot    = Rule(Dot, type=RegExpr)
    r_caret  = Rule(Caret, type=RegExpr)
    r_dollar  = Rule(Dollar, type=RegExpr)

    r_times0 = Rule(RegExpr, LBR, T(Char, 1), Comma, T(Char, 1), RBR, type=RegExpr)
    r_times1 = Rule(RegExpr, LBR, T(Char, 1), RBR, type=RegExpr)
    r_times2 = Rule(RegExpr, LBR, T(Char, 1), Comma, RBR, type=RegExpr)
    r_times3 = Rule(RegExpr, LBR, Comma, T(Char, 1), RBR, type=RegExpr)

    r_times4 = Rule(RegExpr, Mul, type=RegExpr)
    r_times5 = Rule(RegExpr, Question, type=RegExpr)
    r_times6 = Rule(RegExpr, Plus, type=RegExpr)
    r_times7 = Rule(RegExpr, Plus, Question, type=RegExpr)
    r_times8 = Rule(RegExpr, Mul, Question, type=RegExpr)
    r_times9 = Rule(RegExpr, Question, Question, type=RegExpr)

    r_times10 = Rule(RegExpr, LBR, Char, Comma, Char, RBR, Question, type=RegExpr)
    r_times11 = Rule(RegExpr, LBR, Char, Comma, RBR, Question, type=RegExpr)
    r_times12 = Rule(RegExpr, LBR, Comma, Char, RBR, Question, type=RegExpr)
    r_times13 = Rule(RegExpr, LBR, Char, RBR, Question, type=RegExpr)

    r_include = Rule(LB, String, RB, type=RegExpr)
    r_exclude = Rule(LB, Caret, String, RB, type=RegExpr)

    r_gref = Rule(Escape, Num, type=RegExpr)
    r_comment = Rule(LP, Question, Hash, Comment, RP, type=RegExpr)

    r_ngref = Rule(LP, Question, GroupSymbol,
    Equal, GroupName, RP, type=RegExpr)

    r_cnext = Rule(LP, Question, Lesser, Equal, 
    T(RegExpr), RP, T(RegExpr, min=0), type=RegExpr)

    r_ncnext = Rule(LP, Question, Lesser, Exclam, 
    T(RegExpr), RP, T(RegExpr, 0), type=RegExpr)

    r_cback = Rule(T(RegExpr, 0), LP, Question, Equal, 
    T(RegExpr), RP, type=RegExpr)

    r_ncback = Rule(T(RegExpr, 0), LP, Question, 
    Exclam, T(RegExpr), RP, type=RegExpr)

    r_char = Rule(Char, type=RegExpr)
    r_done = Rule(Sof, T(RegExpr), Eof)

    root = [r_gref, r_ngref,  r_ncapture, r_comment, r_word, r_nword, r_metab,
    r_ngroup, r_group, r_dollar, r_caret, r_dot, r_cnext, r_ncnext, r_cback, r_metaB,
    r_ncback, r_times0, r_times1, r_times2, r_times3, r_times4, r_times5,     
    r_times6, r_times7, r_times8, r_times9, r_times10, r_times11, r_times12, 
    r_times13, r_pipe, r_exclude, r_include, r_char, r_done]

class HClassTokens(XSpec):
    """
    Character class/set tokens.
    """
    t_escape = LexSeq(SeqTok(r'\\', Escape, discard=True), SeqTok(r'.', Char))
    t_minus  = LexTok(r'\-', Minus)
    t_char = LexTok(r'.', Char)

    root = [t_escape, t_minus, t_char]

class HClassGrammar(Grammar):
    r_seq  = Rule(Char, Minus, Char, type=RegExpr)
    r_char = Rule(Char, type=RegExpr)
    r_done = Rule(Sof, T(RegExpr), Eof)

    root = [r_seq, r_char, r_done]

