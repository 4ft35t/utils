#!/usr/bin/env python3
# coding: utf-8
# @2021-09-30 11:00:33
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

from publicsuffixlist import PublicSuffixList

ps = PublicSuffixList(accept_unknown=False)

class DomainTree():
    def __init__(self):
        self.root = {}

    def insert(self, domain):
        reversed_list = self.reverse_domain(domain)
        root = self.root
        n = len(reversed_list) - 1
        for index, s in enumerate(reversed_list):
            root.setdefault(s, {})
            root = root.get(s)
            if index == n: # 叶子节点做标记，应对同一域名的根域名和子域名同时存在情况
                root['is.leaf'] = True

    @staticmethod
    def reverse_domain(domain):
        domain = domain.strip()
        return domain.split('.')[::-1]

    def isin(self, domain):
        reversed_list = self.reverse_domain(domain)
        root = self.root
        n = len(reversed_list) - 1
        for index, s in enumerate(reversed_list):
            root = root.get(s)
            if not root: return False
            if index == n and not root.get('is.leaf'): return False
        return True

    def isin_by_rootdomain(self, domain):
        root_domain = ps.privatesuffix(domain)
        return self.isin(root_domain)


class DomainSearch(DomainTree):
    def __init__(self, kwds_domains=[]):
        super().__init__()
        self.set_kwds_domains(kwds_domains)

    def set_kwds_domains(self, kwds_domains):
        self.root = {}
        for dm in kwds_domains:
            self.insert(dm)

    def search(self, target_domains=[], rootdomain=False):
        ''' rootdomain: True, 根域名匹配就为真
        rootdomain: False, 子域名严格匹配才为真
        '''
        ret = []
        func = self.isin_by_rootdomain if rootdomain else self.isin
        yield from filter(lambda x: func(x), target_domains)


def test():
    dt = DomainTree()
    dt.insert('g.cn')
    dt.insert('a.g.cn')
    dt.insert('x.com')
    dt.insert('y.com')

    print(dt.root)
    print(dt.isin('t.g.cn'))
    print(dt.isin_by_rootdomain('t.g.cn'))

    ds = DomainSearch(['a.cn', 'b.com'])
    t = ds.search(['a.a.cn', 'a.cn', 'a.t.cn'])
    print(list(t))
    t = ds.search(['a.a.cn', 'a.cn', 'a.t.cn'], True)
    print(list(t))

if __name__ == '__main__':
    test()
