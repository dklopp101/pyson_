from parser import *
import pickle

TEST_PYS_FILE = 'c:/Users/klopp/OneDrive/Desktop/pyson/testing/tokenizer_test.pys'
TEST_FILE_DUMP = 'c:/Users/klopp/OneDrive/Desktop/pyson/testing/tokenizer_test_dump.b'

# list of test-file token source strings in order.
test_token_strings = [
    'const', 'x', '=', '1',
    'var', 'y', '=', '2',
    'sub', 'add', '(', 'a', ',', 'b', ')', '{', 'return', 'a', '+', 'b', '}',
    'if', '(', 'x', '==', '1', ')', '{', 'print', 'x', '}',
    'elif', '(', 'y', '!=', '2', ')', '{', 'print', 'y', '}',
    'else', '{', 'print', '0', '}',
    'while', '(', 'x', '<', '10', ')', '{', 'x', '=', 'x', '+', '1', '}',
    'print', 'x',
    'x', '=', '1', '+', '2', '*', '3', '/', '(', '4', '-', '5', ')', '%', '6',
    'x', '=', '(', '1', '+', '2', ')', '*', '(', '3', '/', '4', ')', '-', '5',
    'const', 'x', '=', '1',
    'var', 'y', '=', '2',
    'sub', 'add', '(', 'a', ',', 'b', ')', '{', 'return', 'a', '+', 'b', '}',
    'if', '(', 'x', '==', '1', ')', '{', 'print', 'x', '}',
    'elif', '(', 'y', '!=', '2', ')', '{', 'print', 'y', '}',
    'else', '{', 'print', '0', '}',
    'while', '(', 'x', '<', '10', ')', '{', 'x', '=', 'x', '+', '1', '}',
    'print', 'x',
    'var', 'arr', '=', '[', '1', ',', '2', ',', '3', ']',
    'if', '(', '!', 'x', ')', '{', 'print', '0', '}',
    'var', 'z', '=', 'x', '&', 'y',
    'if', '(', 'x', '>', '1', ')', '{', 'print', 'x', '}',
    'if', '(', 'x', '<=', '10', ')', '{', 'print', 'x', '}',
    'if', '(', 'y', '>=', '2', ')', '{', 'print', 'y', '}']

# list of test-file token codes in order.
test_token_codes = [(500, 100), 
                    (501, 501),
                    (503, 24), 
                    (502, 502), 
                    (500, 1), 
                    (501, 501), 
                    (503, 24), 
                    (502, 502), 
                    (500, 2), 
                    (501, 501), 
                    (503, 11), 
                    (501, 501), 
                    (503, 29), 
                    (501, 501), 
                    (503, 12), 
                    (503, 13), 
                    (500, 7), 
                    (501, 501), 
                    (503, 19), 
                    (501, 501), 
                    (503, 14), 
                    (500, 3), 
                    (503, 11), 
                    (501, 501), 
                    (503, 30), 
                    (502, 502), 
                    (503, 12), 
                    (503, 13), 
                    (500, 8), 
                    (501, 501), 
                    (503, 14), 
                    (500, 4), 
                    (503, 11), 
                    (501, 501), 
                    (503, 31), 
                    (502, 502), 
                    (503, 12), 
                    (503, 13), 
                    (500, 8), 
                    (501, 501), 
                    (503, 14), 
                    (500, 5), 
                    (503, 13), 
                    (500, 8), 
                    (502, 502), 
                    (503, 14), 
                    (500, 6), 
                    (503, 11), 
                    (501, 501),
                    (503, 27), 
                    (502, 502), 
                    (503, 12), 
                    (503, 13), 
                    (501, 501), 
                    (503, 24), 
                    (501, 501), 
                    (503, 19), 
                    (502, 502), 
                    (503, 14), 
                    (500, 8), (501, 501), (501, 501), (503, 24), (502, 502), (503, 19), 
(502, 502), (503, 21), (502, 502), (503, 22), (503, 11), (502, 502), (503, 20), (502, 502), (503, 12), 
(503, 23), (502, 502), (501, 501), (503, 24), (503, 11), (502, 502), (503, 19), (502, 502), (503, 12), 
(503, 21), (503, 11), (502, 502), (503, 22), (502, 502), (503, 12), (503, 20), (502, 502), (500, 100), 
(501, 501), (503, 24), (502, 502), (500, 1), (501, 501), (503, 24), (502, 502), (500, 2), (501, 501), 
(503, 11), (501, 501), (503, 29), (501, 501), (503, 12), (503, 13), (500, 7), (501, 501), (503, 19), 
(501, 501), (503, 14), (500, 3), (503, 11), (501, 501), (503, 30), (502, 502), (503, 12), (503, 13), 
(500, 8), (501, 501), (503, 14), (500, 4), (503, 11), (501, 501), (503, 31), (502, 502), (503, 12), 
(503, 13), (500, 8), (501, 501), (503, 14), (500, 5), (503, 13), (500, 8), (502, 502), (503, 14),
(500, 6), (503, 11), (501, 501), (503, 27), (502, 502), (503, 12), (503, 13), (501, 501), (503, 24), 
(501, 501), (503, 19), (502, 502), (503, 14), (500, 8), (501, 501), (500, 1), (501, 501), (503, 24), (503, 15), (502, 502), (503, 29), (502, 502), 
(503, 29), (502, 502), (503, 16), (500, 3), (503, 11), (503, 17), (501, 501), (503, 12), (503, 13), 
(500, 8), (502, 502), (503, 14), (500, 1), (501, 501), (503, 24), (501, 501), (503, 18), (501, 501), 
(500, 3), (503, 11), (501, 501), (503, 28), (502, 502), (503, 12), (503, 13), (500, 8), (501, 501), 
(503, 14), (500, 3), (503, 11), (501, 501), (503, 32), (502, 502), (503, 12), (503, 13), (500, 8), 
(501, 501), (503, 14), (500, 3), (503, 11), (501, 501), (503, 33), (502, 502), (503, 12), (503, 13), 
(500, 8), (501, 501), (503, 14)]

def validator_test():
    filename = 'c:/Users/klopp/OneDrive/Desktop/pyson/testing/val_test.pys'

    try:
        lexer = Lexer()
        lexer.tokenize(filename)
    except Exception as e:
        print('FAILED - tokenizer threw exception: %s' % e)

    TokenListVerifier(lexer.toklist).verify_tokens()

def parser_test(do_silent=False, print_failed_toklist=True):
    result = True
    
    if not do_silent:
        print('\n               TESTING\n-------------------------------------\nNow Testing Lexer..')

    # tokenize the test file.
    try:
        lexer = Lexer()
        lexer.tokenize(TEST_PYS_FILE)
    except Exception as e:
        if not do_silent:
            print('FAILED - tokenizer threw exception: %s' % e)
        result = False

    # check the token codes are correct.
    for token, test_code_set in zip(lexer.toklist.list, test_token_codes):
        if token.type_set != test_code_set:
            if not do_silent:
                print('\nFAILED - token number: %d is incorrect! Type code mismatch\n %s' % (token.ndx, token.print_str))
            result = False

    # check the token source strings are correct.
    # this confirms identifiers and integers are parsing correctly
    for token, test_string in zip(lexer.toklist.list, test_token_strings):
        if token.rawstr != test_string:
            if not do_silent:
                print('\nFAILED - token number: %d is incorrect! Source string mismatch\n %s' % (token.ndx, token.print_str))
            result = False

    if not do_silent:
        print('\nLexer test passed!\n')
    
    if not result:
        if print_failed_toklist:
            print(lexer.toklist)


    # # lets pickle the token list created for examination after.
    # try:
    #     with open(TEST_FILE_DUMP, 'wb') as file:
    #         # Write the list to file.
    #         pickle.dump(lexer.toklist, file)
    # except FileNotFoundError:
    #     print("Error: The file was not found.")
    # except PermissionError:
    #     print("Error: You do not have permission to access this file.")
    # except IsADirectoryError:
    #     print("Error: The specified path is a directory, not a file.")
    # except OSError as e:
    #     print(f"Error: An I/O error occurred. {e}")
    # except Exception as e:
    #     print(f"Error building program list: \n {e}")


    # next we will test the TokenListVerifier.
    if not do_silent:
        print('Now Testing TokenListVerifier..\n')

    verifier = TokenListVerifier(lexer.toklist)
    result = verifier.verify_tokens(do_silent)
    
    return result

def validator_test():
    filename = 'c:/Users/klopp/OneDrive/Desktop/pyson/testing/val_test.pys'

    try:
        lexer = Lexer()
        lexer.tokenize(filename)
    except Exception as e:
        print('\nFAILED - tokenizer threw exception: %s' % e)
    finally:
        pass
        print(lexer.toklist)

    try:
        x = TokenListVerifier(lexer.toklist)
        x.verify_tokens()
        #print('\n\n--=-=-=-=-=- %s ' % x.block_checker.bugde)
    except Exception as e:
        print(e)

def main():
    validator_test()

main()



# if tok is if_stmt push on stack

# if tok is { push on stack

# if tok is } check if { is on stack if so pop it off, if next on stack is if then set can_elif&can_else=true then pop if off stack, otherwise if next on stack was else then
# set can-elif and can-else to false.

# if tok is elif_stmt check if can_elif = true, if so push on stack, if not report error.

# if tok is else check if can_else = true, if so push on stack, if not report error.


# can = f
