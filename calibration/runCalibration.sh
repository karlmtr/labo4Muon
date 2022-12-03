echo "No,A,B" > "calibrationValues.txt"
for i in {1..6}
do 
    echo $i
    echo $(python3 linear_fits.py ../data/calibration/ $i & ) >> "calibrationValues.txt"
done
