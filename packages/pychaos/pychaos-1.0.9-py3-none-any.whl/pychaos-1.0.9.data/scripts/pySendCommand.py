#!python

# import pychaos
import sys
import time
import os
import bson
from kafka import KafkaProducer


if len(sys.argv)<4:
    print("You must specify a <broker:port [9092]> <NodeUID> <cmdname> [JSON VALUE]");
    sys.exit(1);

topic=sys.argv[2].replace('/','.')
topic=topic+"_cmd"
print("sending to:"+sys.argv[1]+" topic:"+topic)
cmd={}

cmd['bc_alias']=""
producer = KafkaProducer(bootstrap_servers=sys.argv[1],acks='all',batch_size=0)

if producer.bootstrap_connected():
    print("Connected")
else:
    print("cannot connect to:"+sys.argv[1])
    sys.exit(1)

if len(sys.argv)==5:
    cmd=sys.argv[4]

cmd['bc_alias']=sys.argv[3]
encoded=bson.dumps(cmd)
producer.send(topic,encoded)
#producer.send(topic,b'ciao')
#producer.flush()

future = producer.send(topic,encoded)
result=future.get(timeout=60)

if result:
    print("sent ok")
else:
    print("## error sending "+cmd )

sys.exit(0)
