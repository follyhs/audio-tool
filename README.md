## 环境配置
- 安装conda 环境:
 	bash Miniconda3-latest-Linux-x86_64.sh
- 拷贝环境：
	把pyhton/robot 拷贝到miniconda3/envs/
- 激活环境：
	conda activate robot	



#### 音频私有化测试工具
1. 性能测试，效果测试工具
2. 如下提供使用说明手册
使用环境：python3

audio-diff
###执行diff工具
1.进入audio-diff目录，
   1.配置start.sh
       私有化公司的url
    2.配置audio_query.py
     #私有化公司accessKey
    3.配置audio_request.py
      #私有化公司accessKey

2.注意：每次运行都需修改prefix对应的值（在start.sh中， 保证每次请求btid唯一)
3.执行的结果会在对应的diff-result中
  每次执行时不会自动清空上次生成的结果，需手动清除，执行命令： >diff-result
4.执行start.sh脚本，命令：sh start.sh


audio-performance
##执行性能工具
1.进入audio-performance，配置audio_request.py
   #私有化公司accessKey
       accesskey=
 2.配置start.sh
     私有化的opurl
     qps：1s的并发数
     count：总共的请求数

 3.执行start.sh脚本
    在mysql数据库saas表中查看性能指标：
   （注意点：
     1.如需多次运行性能工具，每次运行需修改audio_request.py中btid的前缀（btid的位置靠后)，执行sql语句中 where btid like ‘xxxxx%需做相应的改变
     2.finish_time1和finish_time2的取值一定要在请求数据的时间段内）
 统计请求的平均耗时
#select AVG((UNIX_TIMESTAMP(finish_time) - UNIX_TIMESTAMP(start_time))) as time from saas_audio_req_list where btid like 'tool%';
统计请求的实时率：1s可以处理多少时长的音频
#select sum(unix_timestamp(finish_time) - unix_timestamp(start_time)) / sum(length) from saas_audio_req_list where  btid like 'tool%';
吞吐量：每秒的处理的请求数 
#select  count(*) /(TIMESTAMPDIFF(second,'finish_time1','finish_time2')) as res from saas_audio_req_list  where  finish_time between 'finish_time1' and 'fininsh_time2' and  btid like 'tool-%'
              
自己选择请求数据时间段内某一个时间段
finish_time1:取值的开始时间
finish_time2:取值的结束时间


## 执行case
1.启动mock服务 
在audio-mock/mock_start.sh 中修改 数据库信息
执行audio-mock/mock_start.sh
2.在audio-case/start.sh 修改url(主接口)， callback（mock服务的ip） 
执行audio-case/start.sh


