
python3 ../tensorflow1/models/tutorials/image/imagenet/classify_image.py --image_file /home/pi/pyth/image.jpg &>> analysis.txt
grep score analysis.txt
rm analysis.txt
