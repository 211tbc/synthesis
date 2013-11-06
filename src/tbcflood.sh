for run in 1 2 3 4 5 6 7 8
do  
    ../../bin/python test_scripts/tbcrandomtest.py
done

sleeptime=$(python -S -c "import random; print random.randrange(1,10)")
sleep $sleeptime

for run in 1 2 3 4
do
    ../../bin/python test_scripts/tbcrandomtest.py
done

sleeptime=$(python -S -c "import random; print random.randrange(1,10)")
sleep $sleeptime

for run in 1 2 3 4 5 6
do
    ../../bin/python test_scripts/tbcrandomtest.py
done

sleeptime=$(python -S -c "import random; print random.randrange(1,10)")
sleep $sleeptime

for run in 1 2
do
    ../../bin/python test_scripts/tbcrandomtest.py
done
