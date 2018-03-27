import math, time, binascii
import myToolBox
import head

class ShenScheme:
    def __init__(self, taskNum, blockNum, segNum, userParam):
        self._taskNum = taskNum
        self._blockNum = blockNum
        self._segmentNum = segNum
        self._blockSize = self._segmentNum * 20

        self._tags = []
        self.verInfos = []
        self.group = head.group
        self.g = head.g
        self._x = userParam['x']
        self.v = self.g ** self._x
        self.u = userParam['u']

        self.fileName = 'shen' + userParam['fileName']


    def TagGen(self):
        self.fnameSig = self.group.hash(self.fileName, G1) ** self._x
        self.verInfos = [head.verInfos[i] for i in range(self._blockNum)]

        signatures = list()
        for i in range(self._blockNum):
            f = open(head.testDatafilePath, 'rb')
            f.seek(self._taskNum + i * self._blockSize, 0)
            blockBytes = f.read(self._blockSize)
            f.close()

            mi = self.group.init(ZR, 0)
            for j in range(self._segmentNum):
                mij = blockBytes[20 * j:20 * (j + 1)]
                mij = int(binascii.hexlify(mij), 16)
                mij = self.group.init(ZR, mij)
                mi += mij

            sig = self.group.hash(self.verInfos[i], G1) * self.u ** mi
            sig = sig ** self._x
            signatures.append(sig)

        self._tags = signatures

    def TagGen4Update(self):
        self.verInfos = [head.verInfos[i] for i in range(self._blockNum)]

        signatures = list()
        for i in range(self._blockNum):
            f = open(head.testDatafilePath, 'rb')
            f.seek(self._taskNum + i * self._blockSize, 0)
            blockBytes = f.read(self._blockSize)
            f.close()

            mi = self.group.init(ZR, 0)
            for j in range(self._segmentNum):
                mij = blockBytes[20 * j:20 * (j + 1)]
                mij = int(binascii.hexlify(mij), 16)
                mij = self.group.init(ZR, mij)
                mi += mij

            sig = self.group.hash(self.verInfos[i], G1) * self.u ** mi
            sig = sig ** self._x
            signatures.append(sig)

        self._tags = signatures


    def Challenge(self, CNum):
        assert CNum > 0
        assert CNum < self._blockNum

        chal = dict()

        selectBlockSet = myToolBox.getUniqueRandomNum(self._blockNum, CNum)

        chal = {i : self.group.random(ZR) for i in selectBlockSet}

        return chal

    def Proof(self, chal):
        assert isinstance(chal, dict)

        proof = dict()

        M = self.group.init(ZR, 0)
        T = self.group.init(G1, 1)
        for i in chal.keys():
            f = open(head.testDatafilePath, 'rb')
            f.seek(self._taskNum + i * self._blockSize, 0)
            blockBytes = f.read(self._blockSize)
            f.close()

            mi = self.group.init(ZR, 0)
            for j in range(self._segmentNum):
                mij = blockBytes[20*j:20*(j+1)]
                mij = int(binascii.hexlify(mij), 16)
                mij = self.group.init(ZR, mij)
                mi += mij

            M += mi * chal[i]
            T *= self._tags[i] ** chal[i]

        proof['T'] = T
        proof['M'] = M

        return proof


    def Verify(self, chal, proof):
        assert isinstance(proof, dict)

        hname = self.group.hash(self.fileName, G1)
        l = self.group.pair_prod(hname, self.v)
        r = self.group.pair_prod(self.fnameSig, self.g)
        assert l == r

        DI = self.group.init(GT, 1)
        for i in chal.keys():
            hwi = self.group.hash(self.verInfos[i], G1)
            DI *= self.group.pair_prod(hwi, self.v) ** chal[i]
        lhs = self.group.pair_prod(proof['T'], self.g)
        rhs = DI * self.group.pair_prod(self.u ** proof['M'], self.v)

        return lhs == rhs


if __name__ == '__main__':

    t0 = time.perf_counter()
    testCase = ShenScheme(0, 10, 50, head.userParam)
    t1 = time.perf_counter()
    print('Initialize time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    testCase.TagGen()
    t1 = time.perf_counter()
    print('TagGen time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    chal = testCase.Challenge(4)
    t1 = time.perf_counter()
    print('Challenge time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    proof = testCase.Proof(chal)
    t1 = time.perf_counter()
    print('Proof time :', (t1 - t0) * 1000, 'ms')

    t0 = time.perf_counter()
    result = testCase.Verify(chal, proof)
    t1 = time.perf_counter()
    print('Verification time :', (t1 - t0) * 1000, 'ms')

    print(result)

