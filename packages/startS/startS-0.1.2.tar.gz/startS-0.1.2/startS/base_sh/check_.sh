
echo "####################begin check####################"
        #根据目录查看是否已启动
        if [ -z  "$(ps -ef |grep __file__ |grep -v grep)" ];then
                echo "__file__ is not run!"g
                sh __path__/__sh__ start &
                echo `date +'%Y-%m-%d %H:%M:%S'` "__file__ restart!" >> __path__/check/check.log
        fi
echo "####################end check####################"
echo ""

