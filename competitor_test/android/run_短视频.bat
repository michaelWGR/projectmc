' ----------------------- 
' ----- 日志文件夹名 ----
' ----------------------- 
' name enum: 
' 	快手    ks
' 	跪了	orz
' 	faceU	fu
' ----------------------- 
set name=ks

' ----------------------- 
' ----- BEGIN APP进程 ---
' -----------------------

if %name%==ks (
    set app_zhubo=com.smile.gifmaker
    set app=com.smile.gifmaker
)

if %name%==orz (
    set app_zhubo=com.duowan.orz
    set app=com.duowan.orz
)

if %name%==fu (
    set app_zhubo=com.lemon.faceu
    set app=com.lemon.faceu
)


' ----------------------- 
' ----- END APP进程 -----
' -----------------------



' ----------------------- 
' ----- BEGIN 设备列表 --
' ----------------------- 
' zhubo=OPPO R9s
set zhubo1=4b09d00c
set zhubo2=9c9dda86
set zhubo3=84cad46c

' guankan=OPPO R9s
set guankan1=684dd6c4
set guankan2=4a8fd0a4
set guankan3=63e6d0b9
' ----------------------- 
' ----- END 设备列表 ----
' -----------------------



' ----------------------- 
' ----- BEGIN Run zhubo -
' -----------------------
set cmd_zhubo1=python run.py --collect-time 2 --log-path log/%name%/%zhubo1% --device-id %zhubo1% --package-name %app_zhubo%
set cmd_zhubo2=python run.py --collect-time 2 --log-path log/%name%/%zhubo2% --device-id %zhubo2% --package-name %app_zhubo%
set cmd_zhubo3=python run.py --collect-time 2 --log-path log/%name%/%zhubo3% --device-id %zhubo3% --package-name %app_zhubo%
start %cmd_zhubo1%
start %cmd_zhubo2%
start %cmd_zhubo3%
' ----------------------- 
' ----- END Run zhubo ---
' -----------------------



' ----------------------- 
' ----- BEGIN Run guankan
' -----------------------
set cmd_guankan1=python run.py --collect-time 2 --log-path log/%name%/%guankan1% --device-id %guankan1% --package-name %app%
set cmd_guankan2=python run.py --collect-time 2 --log-path log/%name%/%guankan2% --device-id %guankan2% --package-name %app%
set cmd_guankan3=python run.py --collect-time 2 --log-path log/%name%/%guankan3% --device-id %guankan3% --package-name %app%

start %cmd_guankan1%
start %cmd_guankan2%
start %cmd_guankan3%
' ----------------------- 
' ----- END Run guankan -
' -----------------------