for i in {1..15}
do
echo "Cleaning all output files"
mkdir output_efficient
rm output_efficient/out${i}.txt
echo "Creating output file ${i}"
touch output_efficient/out${i}.txt
echo python efficient_3.py input_efficient/in${i}.txt output_efficient/out${i}.txt
python efficient_3.py input_efficient/in${i}.txt output_efficient/out${i}.txt
done
