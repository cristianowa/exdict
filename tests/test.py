import unittest
import exdict
import tempfile
import os


class ExdictTestCase(unittest.TestCase):
    def test_creation(self):
        exd = exdict.Exdict(foo=1)
        self.assertIsInstance(exd, exdict.Exdict)
        self.assertEqual(exd.foo, 1)

    def test_getter(self):
        exd = exdict.Exdict(foo=1)
        self.assertEqual(exd["foo"], 1)


    def test_setter(self):
        exd = exdict.Exdict()
        exd["foo"] = 1
        self.assertEqual(exd["foo"], 1)

    def test_attribute_set(self):
        exd = exdict.Exdict()
        exd.foo = 1
        self.assertEqual(exd["foo"], 1)

    def test_attribute_get(self):
        exd = exdict.Exdict(foo=1)
        self.assertEqual(exd.foo, 1)

    def test_from_yaml(self):
        yaml = """
foo:
  first:
    bar: 1
    two: 2
  third:
    level: deep
duck: canard
        """

        tmp = tempfile.mktemp(suffix="yaml")
        with open(tmp, "w") as f:
            f.write(yaml)
        exd = exdict.Exdict.from_yaml(tmp)
        os.unlink(tmp)
        self.assertIn("foo", exd.keys())
        self.assertIn("first", exd.foo.keys())
        self.assertIn("third", exd.foo.keys())
        self.assertIn("level", exd.foo.third.keys())
        self.assertEqual(exd.foo.third.level, "deep")
        self.assertEqual(exd.foo.first.bar, 1)
        self.assertEqual(exd.foo.first.two, 2)

    def test_from_dict(self):
        d = {"foo":{"bar":1,"two":2, "third":{"level":"deep"}}, "duck":"canard"}
        exd = exdict.Exdict.from_dict(d)
        self.assertIn("foo", exd.keys())
        self.assertIn("third", exd.foo.keys())
        self.assertIn("level", exd.foo.third.keys())
        self.assertEqual(exd.foo.third.level, "deep")
        self.assertEqual(exd.foo.bar, 1)
        self.assertEqual(exd.foo.two, 2)
        self.assertEqual(exd.duck, "canard")

    def test_inheritance(self):
        class ClsUnTst(exdict.Exdict):
            def foo(self):
                print "foo"
        objuntst = ClsUnTst()
        objuntst["one"] = 1
        objuntst["two"] = 2
        self.assertIn("foo", dir(objuntst))
        self.assertIn("one", dir(objuntst))
        self.assertIn("two", dir(objuntst))

    def test_key_not_present(self):
        uut = exdict.Exdict()
        self.assertIsNone(uut.foo)

if __name__ == '__main__':
    unittest.main()
