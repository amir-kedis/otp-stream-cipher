#!/bin/bash

tmux new-session -d -s otp

tmux send-keys -t otp:1 'cd ~/dev/otp-stream-cipher' C-m
tmux send-keys -t otp:1 'nvim .' C-m

tmux new-window -t otp:2
tmux send-keys -t otp:2 'cd ~/dev/otp-stream-cipher' C-m
tmux send-keys -t otp:2 'sleep 1;python main.py receiver --output data/output.txt' C-m

tmux new-window -t otp:3
tmux send-keys -t otp:3 'cd ~/dev/otp-stream-cipher' C-m
tmux send-keys -t otp:3 'python main.py sender --input data/input.txt' C-m

tmux attach-session -t otp


