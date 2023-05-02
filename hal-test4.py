import os
import sys
import time
import subprocess

p=subprocess.Popen(['llama.cpp/main',
    '-m',
    'llama.cpp/models/vicuna-13B-1.1-GPTQ-4bit-128g.GGML.bin',
    '--repeat_penalty',
    '1.0',
    '--color',
    '-i',
    '-r',
    'User:',
    '-f',
    'llama.cpp/prompts/chat-with-bob.txt'],
    stderr=None,
    encoding='ascii')  

llama_in=None
while True:
    llama_out = p.communicate(input=llama_in)            
    print(llama_out)
    llama_in=input(prompt="User:");        
