#! /bin/sh
# Program:
#   to find out redundant rows in a file, here means the find out the items which has multiple natures
# Usage:
#   ./double.sh filename

if [ $# -lt 1 ];then
    echo "Usage: ./double.sh filename"
    exit
fi
if [ ! -e $1 ];then
    echo "The file not exist"
    exit
fi
file=$1
cat $file |
grep -v brand |
awk '
BEGIN{FS="\t"}
{lines[NR]=$0}
NF == 2 {
    exist[$1]++
}
END{
for (each in exist){
    if (exist[each]>1){
        print each
        }
    }
}
' $file > du.txt
