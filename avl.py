
class Node:
    def __init__(self, key_, value_, parent_=None, left_=None, right_=None):
        self.key = key_
        self.value = value_
        self.parent = parent_
        self.left = left_
        self.right = right_
        self.height = 0


class BinaryTree:
    def __init__(self):
        self.root = None

    def search_rec(self, key, curr_node):
        if key == curr_node.key:
            return curr_node.value
        elif key < curr_node.key:
            curr_node = curr_node.left
        elif key > curr_node.key:
            curr_node = curr_node.right

        if curr_node is None:
            return None
        else:
            return self.search_rec(key, curr_node)

    def search(self, key):
        curr_node = self.root
        return self.search_rec(key, curr_node)

    def recalculate_height(self, node):
        if node.right is None and node.left is None:
            return 0
        elif node.right is not None and node.left is not None:
            return max(node.left.height, node.right.height) + 1
        elif node.left is None:
            return node.right.height + 1
        elif node.right is None:
            return node.left.height + 1

    def balance(self, child, parent, grandparent):
        if grandparent is None or parent is None:
            return
        parent.height = self.recalculate_height(parent)
        grandparent.height = self.recalculate_height(grandparent)

        if grandparent.left is None:
            grnd_wsp = grandparent.height
        elif grandparent.right is None:
            grnd_wsp = -1*grandparent.height
        else:
            grnd_wsp = grandparent.right.height - grandparent.left.height

        if parent.left is None:
            prnt_wsp = parent.height
        elif parent.right is None:
            prnt_wsp = -1*parent.height
        else:
            prnt_wsp = parent.right.height - parent.left.height

        if grnd_wsp == -2 and prnt_wsp <= 0:
            parent = grandparent.left
            parent.parent = grandparent.parent
            grandparent.left = parent.right
            if grandparent.left is not None:
                grandparent.left.parent = grandparent
            parent.right = grandparent
            if parent.parent is not None:
                if parent.key < parent.parent.key:
                    parent.parent.left = parent
                else:
                    parent.parent.right = parent
            grandparent.parent = parent
            grandparent.height = self.recalculate_height(grandparent)
            parent.height = self.recalculate_height(parent)
            if grandparent == self.root:
                self.root = parent
            return
        elif grnd_wsp == 2 and prnt_wsp >= 0:
            parent = grandparent.right
            parent.parent = grandparent.parent
            grandparent.right = parent.left
            if grandparent.right is not None:
                grandparent.right.parent = grandparent
            parent.left = grandparent
            if parent.parent is not None:
                if parent.key < parent.parent.key:
                    parent.parent.left = parent
                else:
                    parent.parent.right = parent
            grandparent.parent = parent
            grandparent.height = self.recalculate_height(grandparent)
            parent.height = self.recalculate_height(parent)
            if grandparent == self.root:
                self.root = parent
            return
        elif grnd_wsp == -2 and prnt_wsp > 0:
            parent = grandparent.left
            child = parent.right
            parent.parent = child
            child.parent = grandparent
            if child.left is not None:
                parent.right = child.left
                child.left.parent = parent

            else:
                parent.right = None

            child.left = parent
            grandparent.left = child
            parent.height = self.recalculate_height(parent)
            child.height = self.recalculate_height(child)
            self.balance(parent, child, grandparent)
            return
        elif grnd_wsp == 2 and prnt_wsp < 0:
            parent = grandparent.right
            child = parent.left
            parent.parent = child
            child.parent = grandparent

            #if child.left is not None:
                #parent.left = child.left
                #child.left.parent = parent

            if child.right is not None:
                parent.left = child.right
                child.right.parent = parent
            else:
                parent.left = None
            child.right = parent
            grandparent.right = child
            parent.height = self.recalculate_height(parent)
            child.height = self.recalculate_height(child)
            self.balance(parent, child, grandparent)
            return
        else:
            self.balance(parent, grandparent, grandparent.parent)
            return

    def insert_rec(self, key, data, parent_node):
        if key == parent_node.key:
            parent_node.value = data
            return
        if key < parent_node.key and parent_node.left is not None:
            self.insert_rec(key, data, parent_node.left)
            parent_node.height = self.recalculate_height(parent_node)
            return
        if key > parent_node.key and parent_node.right is not None:
            self.insert_rec(key, data, parent_node.right)
            parent_node.height = self.recalculate_height(parent_node)
            return
        if key < parent_node.key and parent_node.left is None:
            parent_node.left = Node(key, data, parent_node)
            parent_node.height = self.recalculate_height(parent_node)
            if parent_node.parent is not None:
                parent_node.parent.height = self.recalculate_height(parent_node.parent)
            self.balance(parent_node.left, parent_node, parent_node.parent)
            return
        if key > parent_node.key and parent_node.right is None:
            parent_node.right = Node(key, data, parent_node)
            parent_node.height = self.recalculate_height(parent_node)
            if parent_node.parent is not None:
                parent_node.parent.height = self.recalculate_height(parent_node.parent)
            self.balance(parent_node.right, parent_node, parent_node.parent)
            return

    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data)
            return
        else:
            return self.insert_rec(key, data, self.root)

    def delete(self, key):
        curr_node = self.root
        parent_right = None
        parent_left = None
        while key != curr_node.key:
            if key < curr_node.key:
                parent_left = curr_node
                parent_right = None
                curr_node = curr_node.left
            elif key > curr_node.key:
                parent_right = curr_node
                parent_left = None
                curr_node = curr_node.right

            if curr_node is None:
                return None

        node_to_delete = curr_node

        if node_to_delete.right is None and node_to_delete.left is None:
            if parent_right is not None:
                parent_right.right = None
                parent_right.heigth = self.recalculate_height(parent_right)
                if parent_right.parent is not None:
                    parent_right.parent.heigth = self.recalculate_height(parent_right.parent)
                self.balance(None, parent_right.left, parent_right)
            elif parent_left is not None:
                parent_left.left = None
                parent_left.heigth = self.recalculate_height(parent_left)
                if parent_left.parent is not None:
                    parent_left.parent.heigth = self.recalculate_height(parent_left.parent)
                self.balance(None, parent_left.right, parent_left)
##
        elif node_to_delete.right is None and node_to_delete.left is not None:
            grandparent = node_to_delete.parent
            child = node_to_delete.left
            child.parent = grandparent
            if grandparent is not None:
                if child.key < grandparent.key:
                    grandparent.left = child
                else:
                    grandparent.right = child
                grandparent.heigth = self.recalculate_height(grandparent)
            self.balance(None, child, grandparent)

        elif node_to_delete.right is not None and node_to_delete.left is None:
            grandparent = node_to_delete.parent
            child = node_to_delete.right
            child.parent = grandparent
            if grandparent is not None:
                if child.key < grandparent.key:
                    grandparent.left = child
                else:
                    grandparent.right = child
                grandparent.heigth = self.recalculate_height(grandparent)
            self.balance(None, child, grandparent)

        elif node_to_delete.right is not None and node_to_delete.left is not None:

            smallest_from_right = node_to_delete.right
            smallests_parent = node_to_delete

            i = 0
            while smallest_from_right.left is not None:
                smallests_parent = smallest_from_right
                smallest_from_right = smallest_from_right.left
                i+=1

            node_to_delete.key = smallest_from_right.key
            node_to_delete.value = smallest_from_right.value

            if i > 0:
                smallests_parent.left = smallest_from_right.right
                if smallest_from_right.right is not None:
                    smallest_from_right.right.parent = smallests_parent
            if i == 0:
                node_to_delete.right = smallest_from_right.right
                if node_to_delete.right is not None:
                    node_to_delete.right.parent = node_to_delete


            node_to_delete.height = self.recalculate_height(node_to_delete)
            smallests_parent.height = self.recalculate_height(smallests_parent)
            self.balance(smallests_parent.right, smallests_parent, smallests_parent.parent)

    def height_rec(self, node):
        if node is None:
            return 0
        left_height = self.height_rec(node.left)
        right_height = self.height_rec(node.right)
        if left_height >= right_height:
            return left_height + 1
        else:
            return right_height + 1

    def height(self):
        curr_node = self.root
        return self.height_rec(curr_node)

    def str_rec(self, node):
        wynik = ""
        if node is not None:
            wynik += self.str_rec(node.left)

            wynik += f"{node.key}:{node.value} "

            wynik += self.str_rec(node.right)

        return wynik

    def __str__(self):
        wynik = self.str_rec(self.root)
        wynik = wynik[:-1]
        return wynik

    def print_tree(self):
        print("==============")
        self.__print_tree(self.root, 0)
        print("==============")

    def __print_tree(self, node, lvl):
        if node is not None:
            self.__print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)

            self.__print_tree(node.left, lvl + 5)



dict = {50:'A', 15:'B', 62:'C', 5:'D', 2:'E', 1:'F', 11:'G', 100:'H', 7:'I', 6:'J', 55:'K', 52:'L', 51:'M', 57:'N', 8:'O', 9:'P', 10:'R', 99:'S', 12:'T'}

tree = BinaryTree()

for key in dict:
    tree.insert(key, dict[key])

# print 2D tree
tree.print_tree()

# print tree as key:value
print(tree)

print(tree.search(10))

tree.delete(50)
tree.delete(52)
tree.delete(11)
tree.delete(57)
tree.delete(1)
tree.delete(12)
tree.insert(3, "AA")
tree.insert(4, "BB")
tree.delete(7)
tree.delete(8)

# 2D tree
tree.print_tree()

# print tree as key:value
print(tree)
