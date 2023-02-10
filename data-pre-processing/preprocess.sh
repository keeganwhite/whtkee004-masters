START="$(date +%s)"
echo "Starting pre-processing"
echo
cd preprocessing || exit
echo "******************************************"
echo "******STEP 1 - SPLIT PCAPs INTO FLOWS*****"
echo "******************************************"
# shellcheck disable=SC2164
cd flow-splitting || exit
sudo ./flow-splitter.sh
cd ..
echo

echo "******************************************"
echo "***********STEP 2 - LABEL FLOWS***********"
echo "******************************************"
# shellcheck disable=SC2164
cd label || exit
echo
sudo ./label.sh || exit
echo
#echo "Starting to fix formatting..."
#python clean.py || exit
#cd ..
echo  "DONE"

# shellcheck disable=SC2004
DURATION=$(($(date +%s) - ${START} ))
echo "The total duration in seconds was:"
echo ${DURATION}
