#!/bin/bash -x

git clone -b cleanUp  https://github.com/jstupak/aQGC.git

./aQGC/install.sh
source aQGC/setup.sh
./aQGC/generateEvents.sh -m $aQGCWorkDir/aQGC/test.mg -d $delphesDir/cards/delphes_card_MuonColliderDet.tcl -a $aQGCWorkDir/aQGC/analyzeDelphes.py

