#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <node_id|all>"
  exit 1
fi

if [ "$1" == "all" ]; then
  echo "Killing all node.py processes..."
  ps aux | grep "[p]ython.*node.py" | awk '{print $2}' | xargs -r kill
  echo "All node.py processes have been terminated."
else
  NODE_ID=$1
  echo "Killing node.py process for Node $NODE_ID..."
  ps aux | grep "[p]ython.*node.py $NODE_ID" | awk '{print $2}' | xargs -r kill
  echo "Node $NODE_ID process has been terminated."
fi