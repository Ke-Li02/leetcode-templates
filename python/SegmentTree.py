class SegmentTree:

    def __init__(self, nums: list[int]):
        n = len(nums)
        pow2 = 1
        exp = 0

        # pad to the nearest power of 2
        while pow2 < n:
            pow2 = pow2 << 1
            exp += 1

        self.n = n # the length of the original array
        self.tree = [None] * ((pow2 << 1) - 1)
        self.height = exp + 1
        self.start = pow2 - 1 # the index of the first leaf node

        # populate the leaf nodes
        for i in range(n):
            self.tree[self.start + i] = nums[i]

        # populate the internal nodes
        for i in range(self.start - 1, -1, -1):
            leftVal = self.tree[self.getLeftChild(i)] or 0
            rightVal = self.tree[self.getRightChild(i)] or 0
            self.tree[i] = leftVal + rightVal

    def getParent(self, index: int) -> int:
        return (index - 1) // 2 if index > 0 else None

    def getLeftChild(self, index: int) -> int:
        leftChild = index * 2 + 1
        return leftChild if leftChild < len(self.tree) else None

    def getRightChild(self, index: int) -> int:
        rightChild = index * 2 + 2
        return rightChild if rightChild < len(self.tree) else None

    def update(self, index: int, val: int) -> None:
        if index < 0 or index >= self.n:
            return

        # update the value of the leaf node
        curr = self.start + index
        self.tree[curr] = val
        curr = self.getParent(curr)

        # update the value of the internal nodes
        while curr != None:
            leftVal = self.tree[self.getLeftChild(curr)] or 0
            rightVal = self.tree[self.getRightChild(curr)] or 0
            self.tree[curr] = leftVal + rightVal
            curr = self.getParent(curr)

    def sumRange(self, left: int, right: int) -> int:
        if right < left or left < 0 or right >= self.n:
            return -1

        res = 0
        leftNode = self.start + left
        rightNode = self.start + right

        while leftNode <= rightNode:
            if leftNode == rightNode:
                res += self.tree[leftNode]
                break

            # if leftNode is a right child
            if leftNode % 2 == 0:
                res += self.tree[leftNode]
                leftNode = self.getParent(leftNode) + 1
            # if leftNode is a left child
            else:
                leftNode = self.getParent(leftNode)

            # if rightNode is a left child
            if rightNode % 2 == 1:
                res += self.tree[rightNode]
                rightNode = self.getParent(rightNode) - 1
            # if rightNode is a right child
            else:
                rightNode = self.getParent(rightNode)

        return res