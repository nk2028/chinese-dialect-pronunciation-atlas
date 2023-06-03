#!/bin/sh

git clone --depth=1 https://github.com/nk2028/MCPDict.git
cd MCPDict/tools/
python make.py
cd ../../
mkdir -p data/
mv MCPDict/app/src/main/assets/databases/mcpdict.db data/
rm -rf MCPDict/
python dump_info.py
