#!/bin/bash

echo "Killing all node.py processes on macOS..."

ps aux | grep '[p]ython.*node.py' | awk '{print $2}' | xargs -r kill

echo "All node.py processes have been terminated."
