#!/bin/bash -x

if [[ $# < 1 ]];
then
    echo "Usage: ./generateEvents.sh [-m madgraphScript] [-d delphesCard] [-a analysisScript]"
    echo "Example: ./generateEvents.sh -m $PWD/foo -d $PWD/delphes/cards/gen_card.tcl"
    exit
else
    while getopts m:d:a: flag; do
	echo "flag -$flag, Argument $OPTARG";
	case "$flag" in
	    m) mgScript=$OPTARG;;
	    d) delphesCard=$OPTARG;;
	    a) analysisScript=$OPTARG;;
	esac
    done
fi

#restore environment
. ~/.aQGCEnv

touch $aQGCWorkDir/.dummy

#########################################################################

python $madgraphDir/bin/mg5_aMC < $mgScript

gzs=`find . -newer $aQGCWorkDir/.dummy -name "unweighted_events.lhe.gz" -exec echo {} \;`
echo $gzs

#------------------------------------------------------------------------

for gz in $gzs; do 
    lhe=${gz%%.gz}
    output=${lhe%%.lhe}.root  #set delphes output path/name
  
    gunzip $gz
    n=`grep -c \<event\> $lhe`
    echo $n
    sed s%examples/Pythia8/events.lhe%$lhe% $delphesDir/examples/Pythia8/configLHE.cmnd > configLHE.cmnd #this will create a new config pointing to your lhe
    sed "s%Main:numberOfEvents = 10%Main:numberOfEvents = $n%" --in-place configLHE.cmnd
    $delphesDir/DelphesPythia8 $delphesCard configLHE.cmnd $output  #this runs delphes using your new config
    python $analysisScript $output
done
