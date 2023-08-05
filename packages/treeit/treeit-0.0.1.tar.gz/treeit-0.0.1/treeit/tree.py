class Tree:
    def __init__(self, data, **options):
        self.data = data
        self.color = True
        self.__init_options(options)
        self.res = []
        self.__make()

    def __init_options(self, options):
        if options:
            if options.get('color', True):
                self.color = True
            else:
                self.color = False

    def result(self):
        result = '\n'.join(self.res)
        return result

    def __make(self):
        if getattr(self, 'cmd_type', False):
            print('.')
        else:
            self.res.append('.')
        self.__process(self.data, 0, '', True)

    def __process(self, data, level, pre, first=False):
        items = list(data.items())
        length = len(items)
        for i in range(length):
            k, v = items[i]
            cur = self.get_pre(i == length - 1, first)
            if isinstance(v, dict):
                self.out_item(k, level, pre, i == length - 1, is_dir=True)
                self.__process(v, level + 1, pre + cur)
            else:
                self.out_item(k, level, pre, i == length - 1)

    @staticmethod
    def get_pre(last=False, first=False):
        if last:
            return "    "
        else:
            return "│   "

    def out_item(self, item, level, pre='', last=False, is_dir=False):
        if last:
            head = '└── '
        else:
            head = '├── '

        if is_dir:
            if self.color:
                target = '\033[34m{}\033[0m'.format(str(item))
            else:
                target = str(item)
        else:
            target = str(item)
        if getattr(self, 'cmd_type', False):
            print(pre + head + target)
        else:
            self.res.append(pre + head + target)


class TreeCmd(Tree):
    def __init__(self, data):
        self.cmd_type = True
        super(TreeCmd, self).__init__(data)
