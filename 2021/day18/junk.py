
    def __eq__(a, b):
        return id(a) == id(b)

    def is_root(self):
        return self.parent is None



    def walk(self):
        last = self.parent
        n = self

        while True:
            tmp = n
            if n.is_leaf():
                # hit a leaf so go back up
                n = n.parent
            elif last == n.parent or last is None:
                # coming down so go left
                n = n.left
            elif last == n.left:
                # coming up from left so go right
                n = n.right
            elif last == n.right:
                # coming up from right so go back up
                n = n.parent
            else:
                ValueError

            last = tmp

            if not n or n == self:
                return None
            if n.is_leaf():
                return n

    def walkback(self):
        last = self.parent
        n = self

        while True:
            tmp = n
            if n.is_leaf():
                # hit a leaf so go back up
                n = n.parent
            elif last == n.parent or last is None:
                # coming down so go right
                n = n.right
            elif last == n.right:
                # coming up from right so go left
                n = n.left
            elif last == n.left:
                # coming up from left so go back up
                n = n.parent
            else:
                ValueError

            last = tmp

            if not n or (last == n.left and n == self):
                return None
            if n.is_leaf():
                return n



    def zzzzreduce(self):
        def reduce_helper(n, depth=0):
            bail = False
            if n.is_leaf():
                if n.val >= 10:
                    print('split: {}'.format(n))
            else:
                if depth > 4:
                    raise ValueError
                elif depth == 4:
                    print('explode: {}'.format(n))
                else:
                    reduce_helper(n.left, depth + 1)
                    reduce_helper(n.right, depth + 1)
        reduce_helper(self)




def smag(n):
    m = []
    c = []
    d = 0

    for v, dv in n:
        z = dv - d
        if z > 0:
            m += [3] * (dv - d)
            d += z
        elif z == 0:
            m[-1] = 2
        elif z < 0:
            for i in range(abs(z)):
                m.pop()

            pass

        print(d, m)
        c.append(math.prod(m))

    print(c)
        

