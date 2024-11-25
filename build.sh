#!/bin/sh

git clone --depth=1 https://github.com/osfans/MCPDict.git
cd MCPDict/tools/
# Mark all dialects as new to force building all of them
sed -i 's/def outdated():/def outdated():\n\treturn False/g' tables/_詳情.py
python make.py
cd ../../
mkdir -p data/
mv MCPDict/app/src/main/assets/databases/mcpdict.db data/
rm -rf MCPDict/
python dump_info.py
