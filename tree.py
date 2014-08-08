#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Construct Binary Tree From Inorder and Preorder/Postorder Traversal
# http://leetcode.com/2011/04/construct-binary-tree-from-inorder-and-preorder-postorder-traversal.html
# 中文版 http://blog.csdn.net/sgbfblog/article/details/7783935

class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class Tree(object):
	def __init__(self):
		self.root = None
	
	def __build_tree_inorder_preorder(self, in_order, pre_order):
		'''利用中序遍历序列和前序遍历序列重建二叉树
		1. 先序遍历的第一个结点总是根结点, 先序遍历时父亲结点总是在孩子结点之前遍历
		2. 中序遍历序列中，根节点左侧的 n 个节点是左子树，右侧 m 个节点是右子树
		3. 如上，前序遍历序列中，从第二个节点开始计数，前 n 个为左子树，后 m 个为右子树
		'''
		if not (in_order and pre_order): # 任意一个序列为空
			return

		root = pre_order[0]
		root_index = in_order.index(root)
		node = Node(root)
		# 递归构建左右子树
		node.left = self.__build_tree_inorder_preorder(self, in_order[:root_index], pre_order[1:root_index+1])
		node.right  = self.__build_tree_inorder_preorder(self, in_order[root_index+1:], pre_order[root_index+1:])
		return node

	def __build_tree_inorder_postorder(self, in_order, post_order):
		'''利用中序遍历序列和后序遍历序列重建二叉树
		1. 后续遍历序列中最后一个元素为根节点
		2. 中序遍历序列中，根节点左侧的 n 个节点是左子树，右侧 m 个节点是右子树
		3. 如上，后序遍历序列中，前 n 个为左子树，之后的 m 个为右子树
		'''
		if not (in_order and post_order): # 任意一个序列为空
			return

		root = post_order[-1]
		root_index = in_order.index(root)
		node = Node(root)
		# 递归构建左右子树
		node.left = self.__build_tree_inorder_postorder(in_order[:root_index], post_order[:root_index])
		node.right  = self.__build_tree_inorder_postorder(in_order[root_index+1:], post_order[root_index:-1])
		return node

	def build_tree(self, root=None, left=None, right=None, in_order=None, pre_order= None, post_order=None):
		if root is not None: # 手工指定各节点值
			self.root = Node(root, left, right)
			return

		if in_order: # 通过已知遍历序列重建树
			if pre_order: # 前序遍历序列
				self.root = self.__build_tree_inorder_preorder(in_order, pre_order)
			elif post_order: # 后序遍历序列
				self.root = self.__build_tree_inorder_postorder(in_order, post_order)

	def pre_order(self):
		'''前序遍历
		'''
		root = self.root
		def __pre_order(r):
			if r:
				yield r.value
				for i in __pre_order(r.left):
					yield i
				for i in __pre_order(r.right):
					yield i
		return [i for i in __pre_order(root)]

	def in_order(self):
		'''中序遍历
		Ref: http://www.gocalf.com/blog/traversing-binary-tree.html
			http://coolshell.cn/articles/9886.html
		'''
		root = self.root
		def __in_order(r):
			if not r:
				return
			for i in __in_order(r.left):
				yield i
			yield r.value
			for i in __in_order(r.right):
				yield i
		return [i for i in __in_order(root)]

	def post_order(self, r=None):
		'''后序遍历
		'''
		root = self.root
		def __post_order(r):
			if not r:
				return
			for i in __post_order(r.left):
				yield i
			for i in __post_order(r.right):
				yield i
			yield r.value
		return [i for i in __post_order(root)]

	def get_all_depth(self):
		'''计算所有节点的深度, 前序遍历
		Ref: http://cnn237111.blog.51cto.com/2359144/842146
		'''
		root = self.root
		def __get_depth(r, depth=1):
			if not r:
				return
			yield (r.value, depth)
			depth += 1
			for i in __get_depth(r.left, depth):
				yield i
			for i in __get_depth(r.right, depth):
				yield i

		return dict(__get_depth(root))

	def get_leaf_node(self):
		'''获取所有叶子节点
		'''
		root = self.root
		def __get_leaf(r):
			if not r:
				return
			if r.left is None and r.right is None:
				yield r
			for i in __get_leaf(r.left):
				yield i
			for i in __get_leaf(r.right):
				yield i
		return [i for i in __get_leaf(root)]

	def get_path(self, value, root=None):
		'''获取某个节点在树中的访问路径
		Ref: http://blog.csdn.net/GetNextWindow/article/details/23332265
		'''
		if not root:
			root = self.root
		stack = []
		def __get_path(root):
			stack.append(root.value)
			found  = False
			if root.value == value:
				return stack

			if not found and root.left: # 先从左子树找
				found = __get_path(root.left)

			if not found and root.right:
				found = __get_path(root.right)

			if not found: # 当前节点的左右子树都没找到
				stack.pop()
			return found

		return __get_path(root)


def test():
	import pdb;pdb.set_trace()
	n1 = Node(1, Node(2), Node(3))
	n2 = Node(4, Node(5))
	t = Tree()
	t.build_tree(0, n1, n2)
	print t.pre_order()
	print t.in_order()
	print t.post_order()
	t1 = Tree()
	t1.build_tree('X', n2, t.root)
	print t1.pre_order()
	print t.get_all_depth()

	in_list   = 'ABCDEFGHI'
	post_list = 'ACEDBHIGF'
	t.build_tree(in_order=in_list, post_order=post_list)
	print t.get_all_depth()
	print [i.value for i in t.get_leaf_node()]
	print t.get_path('H')

	in_list   = "T b H V h 3 o g P W F L u A f G r m 1 x J 7 w e 0 i Q Y n Z 8 K v q k 9 y 5 C N B D 2 4 U l c p I E M a j 6 S R O X s d z t".split(" ")
	post_list = "T V H o 3 h P g b F f A u m r 7 J x e w 1 Y Q i 0 Z n G L K y 9 k q v N D B C 5 4 c l U 2 8 E I R S 6 j d s X O a M p W t z".split(" ")
	t.build_tree(in_order= in_list, post_order=post_list)
	depth = t.get_all_depth()
	max_depth = sorted(depth.items(), key= lambda x:x[1], reverse=True)[0]
	print max_depth
	print t.get_path(max_depth[0])

	
if __name__ == '__main__':
	test()
