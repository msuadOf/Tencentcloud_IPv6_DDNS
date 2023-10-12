# Tencentcloud_IPv6_DDNS
自动更新本机ipv6 通过DNS 解析到公网域名

以下测试环境为ubuntu22.04，环境默认安装python3.10

申请域名相关请参考腾讯云https://cloud.tencent.com/
申请完域名，要新建一个API密钥
![image](https://github.com/smilecaozheng/Tencentcloud_IPv6_DDNS/assets/23375339/9f3a4a1a-7fb2-4281-a7be-b287dff5e2fb)



# 修改python文件中的secretid和key以及域名等相关信息，并上传到你的服务器
![image](https://github.com/smilecaozheng/Tencentcloud_IPv6_DDNS/assets/23375339/ee502a50-afe7-471b-8b29-e4593ec4ac7c)


1.安装crontab：
```
sudo apt install cron
```
2.设置crontab为开机启动：
加入开机自动启动：
```
sudo systemctl enable cron   
```
或者
```
chkconfig –level 35 cron on
```
3.安装腾讯云API_SDK
```
pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python
```
3.以root用户编辑定时任务
```
crontab -e
```
粘贴以下内容：路径选择上传源码路径
*/10 * * * * python3 /home/klipper/DDNS_v3.py > /home/klipper/DDNS_v3.log
每10分钟运行 输出覆盖文件DDNS.log

查看任务
```
crontab -l
```
4.列出root  用户的 list
```
crontab -u root -l  
```
-u 后面是可以选择用户

【crontab的注意事项】
服务相关的命令
```
sudo systemctl enable cron  # 开机自启服务
sudo systemctl restart cron # 重启服务
sudo systemctl start cron   # 开启服务
sudo systemctl stop cron    # 停止服务
```
