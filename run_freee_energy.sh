#!/bin/bash

MDP="MDP"
echo ".mdp files are stored in $MDP"
# make a new directory to store .mdp files
mkdir $MDP
# clone mdp files for all lambda states
perl perl_free_energy.pl NPT_free_energy.mdp

# energy minimisation step. -nt - number of cores to run task
echo "Starting minimisation MD simulation..."
gmx grompp -f em.mdp -c start.gro -p topol.top -o em.tpr
gmx mdrun -s em.tpr -nt "5" -deffnm em -v

# equilibration step. -nt - number of cores to run task
echo "Starting equilibration MD simulation..."
gmx grompp -f equil.mdp -c em.gro -p topol.top -o equil.tpr
gmx mdrun -s equil.tpr -nt "5" -deffnm equil -v

# Main free energy calculation loop over all lambda states. -nt - number of cores to run task
echo "Starting free energy calculations via MD simulation..."
for (( i=0; i<41; i++ ))
do
    LAMBDA=$i

    mkdir Lambda_$LAMBDA
    cd Lambda_$LAMBDA

    if [ $LAMBDA -eq 0 ]; 
        then
            gmx grompp -f ../$MDP/NPT_free_energy_$LAMBDA.mdp -c ../equil.gro -p ../topol.top -o md$LAMBDA.tpr
            gmx mdrun -s md$LAMBDA.tpr -nt "5" -deffnm md$LAMBDA -v;
        else
            gmx grompp -f ../$MDP/NPT_free_energy_$LAMBDA.mdp -c ../Lambda_$((i-1))/md$((i-1)).gro -p ../topol.top -o md$LAMBDA.tpr
            gmx mdrun -s md$LAMBDA.tpr -nt "5" -deffnm md$LAMBDA -v; 
        fi
        
    echo "Ending. Job completed for lambda = $LAMBDA"

    cd ../
done

echo "Finished MD, analysing results..."
gmx bar -f Lambda_*/md*.xvg -o -oi -b 1000 > result.txt

exit;
