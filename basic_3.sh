rm new_concat.txt
for i in {1..15}
do
echo "Cleaning all output files"
mkdir output
rm output/out${i}.txt
echo "Creating output file ${i}"
touch output/out${i}.txt
echo python basic_3.py input/in${i}.txt output/out${i}.txt
python3.11 basic_3.py input/in${i}.txt output/out${i}.txt
sed -n '1p' output/out${i}.txt >> new_concat.txt
done
