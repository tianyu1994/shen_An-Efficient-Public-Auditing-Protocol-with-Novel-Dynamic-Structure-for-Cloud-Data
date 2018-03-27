'''
this python file for sharing

the PairingGroup:group,
pulblic key:g,
CSP's secret key:sk
'''
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, GT, pair
from schemeParam import publicParam, userSecretData

testDatafilePath = '/home/ty/workspace_for_py/AllSchemeTestData/test0'

def getUserParam(k):
    userParam = {
        'x': group.deserialize(userSecretData.sks[k]),
        'u': group.deserialize(publicParam.us[k]),
        'fileName': userSecretData.sks[k].decode()
    }
    return userParam


group = PairingGroup('SS512')
g = group.deserialize(publicParam.g)
userParam = {
    'x' : group.deserialize(userSecretData.sks[0]),
    'u' : group.deserialize(publicParam.us[0]),
    'fileName' : userSecretData.sks[0].decode()
}
verInfos = [publicParam.verInfos[i] for i in range(50000)]

# some params in tian's scheme
tian_r = group.random(ZR)

segmentNum = 200            #blockSize: 4KB
blockNumber= 50000        #62500
trialsNumber = 20

