import sys
import json
import socket
import time
#kirsche.emzy.de:50001
#electrum.jochen-hoenicke.de:50003
#electrum-server.ninja:50001
#electrum.emzy.de:50001
#e2.keff.org:50001
#fortress.qtornado.com:50001
#electrumx.erbium.eu:50001
#in servers.json find servers use t port.
f = open('tst', 'w')
f.write('.i 608\n.o 32\n')
MAX_BL = 2016
ID = 0
OFFSET = 0
MAX_ID = 300
s = socket.create_connection(('kirsche.emzy.de', 50001))
s.setblocking(0)
for i in range(MAX_ID):
	s.send(json.dumps({"id": ID, "method": 'blockchain.block.headers', "params": [(ID*MAX_BL) - OFFSET, MAX_BL]}).encode() + b'\n')
	total_data = []
	data = ''
	begin = time.time()
	while 1:
		if total_data and time.time()-begin>4:
			break
		elif time.time()-begin>8:
			break
		try:
			data = s.recv(32768)
			if data:
				total_data.append(data)
				begin = time.time()
			else:
				time.sleep(0.15)
		except:
			pass
	try:
		res_b = json.loads(b''.join(total_data).decode())
	except:
		continue
	#if res is None:
	#	print("JSON-RPC: no response")
		#sys.exit(1)
	#	break
	#b = res.read()
	#res_b = json.loads(b)
	if res_b is None:
		print('JSON-RPC: cannot JSON-decode body')
		#sys.exit(2)
		break
	if 'error' in res_b and res_b['error'] != None:
		print(res_b['error'])
		#sys.exit(3)
		break
	if 'result' not in res_b:
		print('JSON-RPC: no result in object')
		#sys.exit(4)
		break
	ID = ID + 1
	res = res_b['result']
	count = res['count']
	if count > 0:
		t = res['hex']
		h = int(len(t)/160)
		OFFSET = OFFSET + (MAX_BL-h)
		#print(str(len(t)))
		#print(str(len(t)/160))
		for j in range(h):
			g = t[j*160:(j+1)*160]
			#print(g)
			#print('\n')
			f.write('{0:0608b} {1:032b}\n'.format(int(g[0:152], 16), int(g[152:], 16)))
	else:
		if OFFSET > (10 * MAX_BL):
			break
	#print('pass')
if ID > 0:
	f.write('.e')
else:
	print("Nothing done!")
	sys.exit(5)
print('bl generated :' + str(ID))
f.close()
sys.exit(0)