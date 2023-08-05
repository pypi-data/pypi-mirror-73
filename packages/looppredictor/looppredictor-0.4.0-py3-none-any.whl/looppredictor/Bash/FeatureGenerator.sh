#!/bin/bash

script_dir=$(cd $(dirname $0);pwd)
basepath=$(dirname $script_dir)
targetFile=$1
annoFile_path=$2
userpath=$3
annoFile=$(ls $annoFile_path)
genome=$4
model=$5

if [ ! -d $userpath/tmp3  ];then
  mkdir $userpath/tmp3
else
  echo "----------------------------tmp3 fold exist----------------------------"
fi

if [ ! -d $userpath/log ];then
  mkdir $userpath/log
else
  echo "----------------------------log fold exist-----------------------------"
fi

$basepath/Bash/bedtools merge -d 5000 -i $userpath/tmp3/target_bedr1.sorted.tmp > $userpath/tmp3/target_bedr2.tmp
target_count=$(< $targetFile wc -l)
for i in $(seq 1 $target_count)
do
	(echo "parsing: $i"
	  chrom=$(awk -v var="$i" 'NR==var{print $1}' $userpath/tmp3/target_bedr2.tmp)
      strt=$(awk -v var="$i" 'NR==var{print $2}' $userpath/tmp3/target_bedr2.tmp)
      end=$(awk -v var="$i" 'NR==var{print $3}' $userpath/tmp3/target_bedr2.tmp)
      #tmp_df=$(awk -v var="$i" -v chrom="$chrom" -v strt="$strt" -v end="$end" 'NR>var{if($1==chrom){print chrom"\t"strt"\t"end"\t"$1"\t"$2"\t"$3}}' $userpath/tmp3/target_bedr2.tmp )
      
      awk -v var="$i" -v chrom="$chrom" -v strt="$strt" -v end="$end" '{if($1==chrom && $2>strt && ($2-end)>10000){print chrom"\t"strt"\t"end"\t"$1"\t"$2"\t"$3}}' $userpath/tmp3/target_bedr2.tmp > $userpath/tmp3/target_row_"$i".tmp

      cat $userpath/tmp3/target_row_$i.tmp >> $userpath/tmp3/target_comb.tmp
      rm $userpath/tmp3/target_row_$i.tmp)&
    # allow only to execute $N jobs in parallel
    
    if [[ $(jobs -r -p | wc -l) -gt $num_processes ]]; then
        # wait only for first job
        wait -n
    fi
done
awk '{if(NF==6){print $1"\t"($2-2000)"\t"($3+2000)"\t"$4"\t"($5-2000)"\t"($6+2000)}}' $userpath/tmp3/target_comb.tmp > $userpath/tmp3/target_comb_final
sort -k1,1 -k2,2n -k3,3n -k4,4 -k5,5n -k6,6n $userpath/tmp3/target_comb_final > $userpath/tmp3/target_comb_final.sort 
targetFile=$userpath/tmp3/target_comb_final.sort

for filename in $annoFile
do
	echo $filename
	Rscript $basepath/Rscript/GRangesTool_neighbor.R $targetFile $annoFile_path/$filename $userpath/tmp3/tmp_feature_$filename $genome &
done >> $userpath/log/GRangeNeighbor_Log.txt
wait
echo "----------------------------Annotation done!-----------------------------"

target_temp=$userpath/tmp3/target.tmp
awk '{print $1"	"$2"	"$3}' $target_temp > $userpath/tmp3/anchor1.tmp
awk '{print $4"	"$5"	"$6}' $target_temp > $userpath/tmp3/anchor2.tmp
annotatePeaks.pl $userpath/tmp3/anchor1.tmp $genome  >  $userpath/tmp3/tmp_feature_tss_anchor1 && >> $userpath/log/Homer_log.txt
annotatePeaks.pl $userpath/tmp3/anchor2.tmp $genome  >  $userpath/tmp3/tmp_feature_tss_anchor2 && >> $userpath/log/Homer_log.txt
echo "----------------------------Homer annotates done!-------------------------"
rm -f $userpath/tmp3/*.tmp

echo "----------------------------Merging features!-----------------------------"
Rscript $basepath/Rscript/MergeFeature_complete.R  $targetFile  $userpath/tmp3  $model $userpath/feature_out.txt

