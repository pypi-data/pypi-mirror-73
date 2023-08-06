export
case "$1" in
  start)
        echo "Starting __file__"
        echo `date +'%Y-%m-%d %H:%M:%S'` "__file__ restart!" >> __path__/console.log
        cd __path__ 
        nohup __python_path__ ./__file__ &
        ;;
  stop)
        echo "Stoping __file__"
	ps -ef |grep __file__ |grep -v grep | awk '{print " kill -9 " $2}' |sh
	sleep 2
        ;;
  restart)
        $0 stop
        $0 start
        ;;
  *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0
