################################
# simple flask app run
################################
ps ux|grep python|grep run_app|grep -v grep|awk '{print $2}'|xargs kill -9
nohup python run_app.py &
