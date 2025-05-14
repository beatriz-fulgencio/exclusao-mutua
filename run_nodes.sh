#!/bin/bash

# Change to the directory where this script is located
cd "$(dirname "$0")"

# Number of nodes to launch
NODES=6

# Path to the node script
NODE_SCRIPT="node.py"

# Optional: absolute path to Python interpreter
PYTHON_BIN="python3"

echo "Detectando sistema operacional..."

OS="$(uname)"
echo "Sistema detectado: $OS"

if [ "$OS" == "Darwin" ]; then
echo "Executando em macOS usando Terminal.app (osascript)"
# Launch each node in a separate terminal window
for i in $(seq 1 $NODES)
do
echo "Launching node $i"
osascript -e "tell app \"Terminal\" to do script \"cd $(pwd) && $PYTHON_BIN $NODE_SCRIPT $i > node_$i.log 2>&1\""
done

elif [ "$OS" == "Linux" ]; then
echo "Executando em Linux usando gnome-terminal"

    # Launch each node in a separate terminal window
for i in $(seq 1 $NODES)
do
echo "Launching node $i"
gnome-terminal -- bash -c "cd $(pwd) && $PYTHON_BIN $NODE_SCRIPT $i; exec bash"
done

fi