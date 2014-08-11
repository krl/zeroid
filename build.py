import serpent, json, random
from pyethereum import transactions, blocks, processblock,utils

NUM_ACCOUNTS=4

root_code = serpent.compile(open('zeroid.se').read())
root_key = utils.sha3('cow')
root_addr = utils.privtoaddr(root_key)

keys = {}

for x in range(NUM_ACCOUNTS):
  key  = utils.sha3(str(x+4))
  addr = utils.privtoaddr(key)
  keys[addr] = key

endowment = {root_addr: 10**18}

for x in keys:
  endowment[x] = 10**18

genesis = blocks.genesis(endowment)

tx1 = transactions.contract(0, 10**12, 100000, 0, root_code).sign(root_key)

result, contract = processblock.apply_transaction(genesis, tx1)

nonce=1

for address in keys:

  longitude = random.randint(1000, 110000)
  latitude  = random.randint(1000, 110000)
  datalist  = serpent.encode_datalist([0, longitude, latitude])
  
  tx = transactions.Transaction(0,
                                10**12,
                                10000,
                                contract,
                                1000,
                                datalist).sign(keys[address])
  #nonce = nonce + 1
                                
  result, ans = processblock.apply_transaction(genesis, tx)

storage = genesis.to_dict()["state"][contract]["storage"]

integers = {}

for k in storage:
    integers[int(k, 16)] = int(storage[k], 16)

print(json.dumps(integers, sort_keys=True,
                 indent=4, separators=(',', ': ')))

