from collections import deque
from copy import deepcopy
from parser import *

# NOTE: within this file 'cnfrm' is used as an abbreviation for 'confirm'.

# Source file is parsed into token objects which are turned into an ast.
# Ast is a list stmt & expr node objects with their own children nodes,
# which in turn can have their own children, and so on.

# expr nodes are operations, identifiers & integers. unary operations
# have the left node as operand, binary have left and right expr nodes.
# expr l/r nodes can be any expr, subcalls l_operand is subid, args are
# in exprnode args.

# operator precedence dict used by ast generator.
# key: operator-code, value: precedence number, lower the number: higher the precedence.
op_precedence = {
    11 :   1, # '('  
    12 :   1, # ')'  
    13 : 100, # '{'
    14 : 100, # '}'  
    15 :   1, # '['
    16 :   1, # ']'
    17 :   2, # '!'  
    18 :   2, # '&' 
    19 :   4, # '+'
    20 :   4, # '-'
    21 :   3, # '*'
    22 :   3, # '/'
    23 :   3, # '%'
    24 :  50, # '='
    27 :   6, # '<'
    28 :   6, # '>'
    29 :  55, # ','
    30 :   7, # '==' 
    31 :   7, # '!=' 
    32 :   6, # '<='
    33 :   6, # '>=' 
    34 :   1, # '++'
    35 :   1  # '--' 
}


stmt_list = {
    'const'      :  0,
    'var'        :  1,
    'sub'        :  2,
    'if'         :  3,
    'elif'       :  4,
    'else'       :  5,
    'while'      :  6,
    'return'     :  7,
    'print'      :  8,
    'fileopen'   :  9,
    'fileclose'  : 10
}

expr_list = {
    'operation'  :  0,
    'integer'    :  1,
    'identifier' :  2,
    'subcall'    :  3
}

class ExprNode:
    def __init__(self):
        self.op      = None
        self.l_oprnd = None
        self.r_oprnd = None
        self.val     = None # used by int & id exprs.
        self.args    = None

class StmtNode:
    def __init__(self, _type):
        self.type = _type
        self.id = None
        self.expr = None # used for if/elif/else/while test.
        self.args = deque() # used by subdef stmt nodes.
        self.body = deque()
        self.children = deque()

class AstGenerator:
# self.globlist = deque() = main list of global node objects.
# self.op_stack = deque() = operator stack used for processing exprs.
# self.opr_stack = deque() = operand stack used for processing exprs.
# self.curr_globnode_ndx = -1 = index of current global node.
# self.curr_body_ndx = -1 = index of current node inside a body list.
# self.curr_node = None = current node being processed.
# self.curr_node_ndx = -1 = 
# self.in_operation = False
# self.in_subdef = False
# self.tokndx = -1 = index of current token.
# self.toklist = list of token objects returned from parser tokenizer.

    def __init__(self):
        self.globlist = deque()
        self.op_stack = deque()
        self.opr_stack = deque()

        self.curr_globnode_ndx = -1
        self.curr_node_ndx = -1
        self.curr_body_ndx = -1
        self.curr_node = None
        self.curr_parent_node = None
        self.parent_nodes = deque()

        self.tokndx = -1
        self.toklist = None
        self.tok = None

        self.in_op = False
        self.in_expr = False
        self.in_subdef = False
        self.at_globlvl = False

    def build_toklist(self, input_file_path):
        # parse source file into token list.
        try:
            self.toklist  = tokenize(input_file_path)
        except Exception:
            print('exception thrown from parser.')
    
    def build_id_node(self, idstr):
        id_node = ExprNode()
        id_node.val = idstr
        return deepcopy(id_node)

    def build_int_node(self, intval):
        int_node = ExprNode()
        int_node.val = intval
        return deepcopy(int_node)

    def advance_tok(self):
        self.tokndx += 1
        self.tok = self.toklist[self.tokndx]

    def build_expr_node(self):
        pass

    def proc_ret_stmt(self):
        # confirm we're within subdef before proceding.
        if not self.in_subdef:
            print('return stmt not in subdef')
            raise Exception

        ret_node = StmtNode(7) # 7: ret stmt type code.
        ret_node.expr = self.build_expr_node()
        self.curr_parent_node.body.append(deepcopy(ret_node))

    def proc_print_stmt(self):
        print_node = StmtNode(8) # 8: print stmt type code.
        print_node.expr = self.build_expr_node()
        self.curr_parent_node.body.append(deepcopy(print_node))

    def proc_var_assign(self, id_node):
        assign_node = ExprNode()
        assign_node.op = 24 # 24: assignment op type code.
        assign_node.l_oprnd = deepcopy(id_node)
        assign_node.r_oprnd = self.build_expr_node()

        if self.at_globlvl:
            self.globlist.append(deepcopy(assign_node))
        else:
            self.curr_parent_node.body.append(deepcopy(assign_node))


    def makenew_parent_node(self, new_parent_node):
        """ Takes reference to new-parent-node.
            Appends current parent node to child nodes stack.
            Sets new parent to self.curr_parent_node.
        """ 

        if self.curr_parent_node: # if no parent node nothing to append to child-nodes-stack.
            self.parent_nodes.append(self.curr_parent_node)
        self.curr_parent_node = new_parent_node

    def proc_if_stmt(self):
        if self.at_globlvl:
            self.globlist[-1].append(StmtNode(3))
            if_node = self.globlist[-1] # create a ref of if-node for convenience.
        else:
            self.curr_parent_node.body.append(StmtNode(3))
            if_node = self.curr_parent_node.body[-1] # create a ref of if-node for convenience.
            self.makenew_parent_node(self, if_node)

        # process the if stmt test. next token must be left parent token.
        self.advance_tok()
        self.assert_optok(11) # 11: lparen op type code.
        
        # left parent found, but we will take tokndx back one because
        # build_expr_node needs to examine it.
        self.tokndx -= 1
        if_node.expr = deepcopy(self.build_expr_node())

        # confirm next tok is left-curly-brace
        self.advance_tok()
        self.assert_optok(13) # 13: lcurly brace op type code.

        # first check for simplest stuff, var assignments, simple stmts ect.
        if self.tok.type == 501: # 501: id tok type code.
            id_node = self.build_id_node(self.tok.rawstr)

            # tok was id, advance tok then check for assignment, inc or dec tokens.
            self.advance_tok()

            if self.tok.type == 503: # operator tok type code.
                # determine if assignment op or inc/dec op.
                if self.tok.subtype == 24: # assignment op type code.
                    self.proc_var_assign(id_node)

                elif self.tok.subtype == 34 or self.tok.subtype == 35: # 34/35: inc/dec type codes.
                    pass

            
    def proc_elif_stmt(self):
        pass

    def proc_else_stmt(self):
        pass

    def proc_while_stmt(self):
        pass

    def proc_const_dec(self):
        """ const dec: const stmt(id-expr, int-expr)
            const decs can only be integer literals.
            as oposed to var decs which can be int
            literals *or* an expression.
        """
        id_node = None
        int_node = None

        # confirm const dec is at global level.
        if not self.at_globlvl:
            print('const dec not at global level.')
            raise Exception         

        # confirm const dec isn't within an operator or expression.
        if self.in_expr:
            print('const dec within expression')
            raise Exception

        # confirm next token is an identifier if so make it's node.
        self.advance_tok()
        self.assert_toktype(501) # 501: identifier token
        
        id_node = self.build_id_node(self.tok.rawstr)

        # confirm next tok is an assignment op if so advance past it.
        self.advance_tok()
        self.assert_optok(24) # 24: assignment op type code.

        # confirm next tok is an integer tok if so make it's node.
        self.advance_tok()
        self.assert_toktype(502) # 501: int token
        int_node = self.build_int_node(self.tok.value)

        # everything's in order so create const node add to globlist.
        # const StmtNode, body has id node and int node in this order.
        self.globlist.append(StmtNode(0)) # 0- const type code.

        # [-1] index is top item of globist stack.
        self.globlist[-1].id = deepcopy(id_node)
        self.globlist[-1].expr = deepcopy(int_node)

        # const declaration complete.

    def proc_var_dec(self):
        """ var dec: var stmt(id-expr, expr)
            var dec's are same as const except they can be
            exprs instead of only int literals.
        """
        id_node = None
        expr_node = None

        # confirm var dec is at global level.
        if not self.at_globlvl:
            print('var dec not at global level.')
            raise Exception         

        # confirm var dec isn't within an operator or expression.
        if self.in_expr:
            print('var dec within expression')
            raise Exception

        # confirm next token is an identifier if so make it's node.
        self.advance_tok()
        self.assert_toktype(501) # 501: identifier token
        
        id_node = self.build_id_node(self.tok.rawstr)

        # confirm next tok is an assignment op if so advance past it.
        self.advance_tok()
        self.assert_optok(24) # 24: assignment op type code.

        # build var dec expr.
        expr_node = self.build_expr_node()

        # everything's in order so create const node add to globlist.
        # const StmtNode, body has id node and int node in this order.
        self.globlist.append(StmtNode(1)) # 1- var type code.

        # [-1] index is top item of globist stack.
        self.globlist[-1].id = deepcopy(id_node)
        self.globlist[-1].expr = deepcopy(expr_node)
        
        # var declaration complete.



