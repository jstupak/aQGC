export aQGCWorkDir=$PWD

if [[ $HOSTNAME == "login.snowmass21.io" ]]; then
    #important
    module load python/2.7.15
    module load py-numpy/1.15.2-py2.7
    module load py-six/1.11.0-py2.7
    . /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.22.08/x86_64-centos7-gcc48-opt/bin/thisroot.sh

    #convenient
    module load emacs
else
    which root >> /dev/null
    if [[ $? -ne 0 ]]; then
        echo "Please ensure ROOT is available and retry"
    fi
fi

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#MadGraph
wget https://launchpad.net/mg5amcnlo/3.0/3.1.x/+download/MG5_aMC_v3.1.1.tar.gz
tar -xzvf MG5_aMC_v3.1.1.tar.gz
if [[ $? -ne 0 ]]; then
    echo "ERROR getting madgraph"
    exit
else
    export madgraphDir=$aQGCWorkDir/MG5_aMC_v3_1_1
    rm MG5_aMC_v3.1.1.tar.gz
fi

#Pythia
wget https://pythia.org/download/pythia83/pythia8306.tgz
tar -xzvf pythia8306.tgz
rm pythia8306.tgz
cd pythia8306
./configure --prefix=$aQGCWorkDir
make -j
make install
if [[ $? -ne 0 ]]; then
    echo "ERROR compiling pythia"
    exit
else
    export pythiaDir=$aQGCWorkDir/pythia830g
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${aQGCWorkDir}/lib
    export PYTHIA8=$aQGCWorkDir
    rm pythia8306.tgz
    cd ..
fi

#Delphes
git clone https://github.com/delphes/delphes.git
cd delphes
make HAS_PYTHIA8=true -j -I${aQGCWorkDir}/include/Pythia8
if [[ $? -ne 0 ]]; then
    echo "ERROR compiling delphes"
    exit
else
    export delphesDir=$aQGCWorkDir/delphes
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${delphesDir}
    cd ..
fi

export -p > ~/.aQGCEnv
