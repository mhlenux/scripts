#! /bin/bash

srcExt=$1
destExt=$2
srcDir=$3
destDir=$4

opts="-c:v libx265 -crf 28 -c:a aac -map_metadata 0"
# ffmpeg-batch-convert.sh mp4 mp4 /input/files /output/files

for filename in "$srcDir"/*."$srcExt"; do

  # remove extension
  basePath=${filename%.*}
  # get rid of the path itself
  baseName=${basePath##*/}
  
  # ffmpeg -i file.mp4 -c:v libx265 -crf 28 -c:a aac -map_metadata 0 /output/file.mp4
  ffmpeg -i "$filename" $opts "$destDir"/"$baseName"."$destExt"

done

echo "Conversion from ""${srcDir}/*.${srcExt}"" to ${destDir}/*.${destExt} complete!"