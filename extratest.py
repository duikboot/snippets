import unittest


class CollectionTest(unittest.TestCase):

    def assertList(self, result, expect):
        # Verifies lists have the same contents
        lhs = [r for r in result]
        lhs.sort()
        rhs = list(expect)
        rhs.sort()
        if not lhs and rhs or rhs and not lhs:
            self.fail(
                'One of the lists is empty: ' + str(lhs) + " != " + str(rhs))
        for i in lhs:
            if i not in rhs:
                self.fail(str(i) + ' is not in ' + str(rhs))
        for i in rhs:
            if i not in lhs:
                self.fail(str(i) + ' is not in ' + str(lhs))

    def assertDictContents(self, result, expect, exact=True):
        for r, e in zip(sorted(result.items()), sorted(expect.items())):
            if r[0] != e[0]:  # compare keys
                self.fail("Dictionary keys: %s != %s\n"
                          "Dictionaries not Equal: result: %s, expect: %s" %
                          (str(r[0]), str(e[0]), result, expect))
            base_message = ("Dictionary key contents %s mismatch: key: %s\n"
                            "result contents: %s\n"
                            "expect contents: %s\n"
                            "result: %s\n expect: %s\n")
            if type(r[1]) != type(e[1]):
                self.fail(base_message % ("type", str(r[0]), str(r[1]),
                                          str(e[1]), result, expect))
            if isinstance(r[1], basestring):
                if r[1] != e[1]:
                    self.fail(base_message % ("string", str(r[0]), str(r[1]),
                                              str(e[1]), result, expect))
            elif isinstance(r[1], (list, tuple, set)):
                if sorted(r[1]) != sorted(e[1]):
                    self.fail(base_message % ("list", str(r[0]), str(r[1]),
                                              str(e[1]), result, expect))
            elif isinstance(r[1], dict):
                if not self.assertDictContents(r[1], e[1]):
                    self.fail(base_message % ('dictionary', str(r[0]),
                                              str(r[1]), str(e[1]), result,
                                              expect))
        return True
