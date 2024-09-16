# YASS-Frontend
**Yet Another Stream Splitter (Generally for EMBY)**

![Main Branch Build CI](https://github.com/FacMata/YASS-Frontend/actions/workflows/main.yml/badge.svg)    ![Dev Branch Build CI](https://github.com/FacMata/YASS-Frontend/actions/workflows/dev.yml/badge.svg)

## 这是什么

### YASS

一个基于 [MisakaFxxk](https://github.com/MisakaFxxk) 的 [Go_stream](https://github.com/MisakaFxxk/Go_stream) 项目改进而来的，EMBY 视频流分离推送解决方案的程序组。



在 [MisakaFxxk](https://github.com/MisakaFxxk) 没有更新的前提下，它与 YASS-Frontend 可以作为原程序的后继者。



### YASS Frontend

YASS 项目的前端程序。其完成的工作是解析请求中的文件路径，以相对挂载目录的路径的方式传递给后端。



本程序在 [Go_stream](https://github.com/MisakaFxxk/Go_stream) 的基础上重排版了代码，合并了重复逻辑，引入了 Redis 缓存，实现了 程序--配置 分离，播放效率相比原版有一定提升。



**目前** 可以搭配原版后端使用，也可以搭配 [YASS-Backend](https://github.com/FacMata/YASS-Backend) 使用。



## 如何配置

#### 1. 下载最新 Release

下载到你的运行目录下即可，无需解压。

#### 2. 配置 `config.yaml`

```yaml
emby_url: "http(s)://<your_emby_server_addr>:<your_emby_server_port>/"
emby_key: "<your_emby_api_key>"
local_dir: "<your_local_dir>"
remote_api: "http://<your_stream_channel_addr>:<your_stream_channel_port>/<your_stream_channel_path>"
remote_domain: "<your_stream_channel_addr>"
remote_port: <your_stream_channel_port>
remote_token: "<your_inter-yass_api_key>"

cache:
  redis_host: "127.0.0.1"
  redis_port: 6379
  key_prefix: "emby_cache:"

app:
  host: "<listen_ip>"
  port: <listen_port>

```

此处 **目前** 可参考 [Go_stream](https://github.com/MisakaFxxk/Go_stream) 的相关配置进行操作。

#### 3. 运行程序

```shell
# sudo chmod +x <filename>
# ./<filename> config.yaml
```

持久化运行推荐使用 `SystemD System Service` 或者 `screen` 。



## 寻求交流

Email: [contact@facmata.net](mailto://contact@facmata.net)

Telegram Group: [YASS Talking](https://t.me/YASS_Talking)
