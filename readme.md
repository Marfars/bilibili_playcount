刷b站播放量，原神up主激励计划

# docker启动
1. 安装docker
2. 执行指令
```docker
docker network create my-network
docker run --network my-network --name redis -d redis redis-server --requirepass 123456
docker run --network my-network --env DB_CONN=redis://:123456@redis:6379/0 -p 5010:5010 jhao104/proxy_pool
```

# proxy启动
1. 运行 `/proxy_pool/start.sh` 启动代理池（Windows 可使用 git bash 运行 sh 脚本儿，或者手动执行里面的两条儿命令）

# 准备venv环境，仅第一次需要

1. terminal依次输入指令
```shell
python3.12 -m venv env
# windows
env\Scripts\activate
# mac
source env/bin/activate

pip install jupyterlab
pip install ipykernel
python -m ipykernel install --user --name=env_name --display-name "Python (proxy)"
```

# 安装requirements

1. 进入requirements所在目录，执行
```shell
pip install -r requirements.txt
```

# 在bofang.ipynb目录下启动jupyter notebook，需要提前激活虚拟环境