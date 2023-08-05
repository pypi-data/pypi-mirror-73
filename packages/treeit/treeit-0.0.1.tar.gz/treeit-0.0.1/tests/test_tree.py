from treeit import Tree, TreeCmd

demo = """
.
├── a
│   ├── a
│   │   ├── a
│   │   │   ├── a
│   │   │   └── b
│   │   └── b
│   │       ├── a
│   │       └── b
│   └── b
├── b
└── c
"""


def test_1():
    a = dict()
    a['a'] = dict(a=dict(a=dict(a=1, b=1), b=dict(a=1, b=1)), b=1)
    a['b'] = 1
    a['c'] = 1

    t = Tree(a, color=False)
    res = t.result()
    # print(res)
    # diff = difflib.ndiff(res, demo)
    # print(''.join(diff))


if __name__ == '__main__':
    test_1()
