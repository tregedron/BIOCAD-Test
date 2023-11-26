#!/bin/bash

MDP="MDP"
echo ".mdp files are stored in $MDP"

gmx grompp -f em.mdp -c start.gro -p topol.top -o em.tpr
gmx mdrun -s em.tpr -nt "5" -deffnm em -v

gmx grompp -f equil.mdp -c em.gro -p topol.top -o equil.tpr
gmx mdrun -s equil.tpr -nt "5" -deffnm equil -v

for (( i=0; i<41; i++ ))
do
    LAMBDA=$i

    mkdir Lambda_$LAMBDA
    cd Lambda_$LAMBDA

    # A new directory will be created for each value of lambda and
    # at each step in the workflow for maximum organization.

    #################
    # PRODUCTION MD #
    #################
    echo "Starting production MD simulation..."

    if [ $LAMBDA -eq 0 ]; 
        then
            gmx grompp -f ../$MDP/NPT_free_energy_$LAMBDA.mdp -c ../equil.gro -p ../topol.top -o md$LAMBDA.tpr
            gmx mdrun -s md$LAMBDA.tpr -nt "5" -deffnm md$LAMBDA -v;
        else
            gmx grompp -f ../$MDP/NPT_free_energy_$LAMBDA.mdp -c ../Lambda_$((i-1))/md$((i-1)).gro -p ../topol.top -o md$LAMBDA.tpr
            gmx mdrun -s md$LAMBDA.tpr -nt "5" -deffnm md$LAMBDA -v; 
        fi

    

    echo "Production MD complete."

    # End
    echo "Ending. Job completed for lambda = $LAMBDA"

    cd ../
done

gmx bar -f Lambda_*/md*.xvg -o -oi -b 1000 > result.txt

exit;