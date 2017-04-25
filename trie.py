#!/usr/bin/env python
# coding: utf-8
# weizx@2017-04-25 15:07:32
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

# https://zh.wikipedia.org/wiki/Trie
# http://www.shellcodes.org/Programming/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E7%AE%97%E6%B3%95/Trie%E6%A0%91.html

class Trie(object):
    def __init__(self):
        self.tree = dict()

    def insert_tree(self, item_list):
        root = self.tree
        for i in item_list:
            root.setdefault(i, {})
            root = root[i]

    def search_tree(self, item_list):
        root = self.tree
        for i in item_list:
            if root.get(i) == {}: # leaf
                return True
            if root.get(i):
                if i == item_list[-1]:
                    return True
                root = root[i]

        return False


class DomainSearch(Trie):
    '''search subdomains form a root domain tree'''
    def build_domain_tree(self,domain_list=[]):
        for i in domain_list:
            self.insert_tree(self.reverse_domain(i))

    def search_domain(self, domain):
        return self.search_tree(self.reverse_domain(domain))

    def reverse_domain(self, domain):
        return domain.split('.')[::-1]

if __name__ == '__main__':
    lst = ['g.cn', 't.co', 't.cn', 'pku.edu.cn']
    dmt = DomainSearch()
    dmt.build_domain_tree(lst)
    print dmt.tree
    assert dmt.search_domain('g.cn')
    assert dmt.search_domain('www.g.cn')
