basedir=$(dirname "$0")
cwd=$(pwd)
script_path="$basedir"/video_delay.py

app=$1
actor_ext=${2:-"avi"}
viewer_ext=${3:-"avi"}
frame_rate=${4:-"60"}
times=${5:-"3"}
actor_prefix="$app"_ios_videodelay_actor
viewer_prefix="$app"_ios_videodelay_viewer
csv_prefix="$app"_ios_videodelay

for ((i=1; i<=times; i ++))
do
    actor_video_name="$actor_prefix"_0"$i"."$actor_ext"
    viewer_video_name="$viewer_prefix"_0"$i"."$viewer_ext"
    actor_video_path="$cwd"/"$actor_video_name"
    viewer_video_path="$cwd"/"$viewer_video_name"
    csv_name="$csv_prefix"_0"$i".csv
    csv_path="$cwd"/"$csv_name"

    echo "$actor_video_name $viewer_video_name $csv_name"
    cmd="python $script_path -sr $frame_rate -tr $frame_rate $actor_video_path $viewer_video_path $csv_path"
    $cmd 1>>/dev/null
    if [ "$?" -ne 0 ]; then echo "video_delay failed"; exit 1; fi
done