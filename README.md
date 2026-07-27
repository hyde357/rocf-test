---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: bed9e04a7fbdd413e715ac8d103dd66b_c859262f7b8611f180e15254006c9bbf
    ReservedCode1: TfLwojpVzKdBL9H2Kl5EwP/6b6zc/JiOtnW2DQIVpAF6SDD92kTETfRg6b2bRbjpmjHY4MJbLXEqmjBB4qX4MHX5yNBOJK1cc/V2b6nSiZd681NNvDJqTOQFlQj28QR5HkxDmiaJXDCLFnx6BnCCUWYUZE9EV8uMg1dBfDTKuLoLecXvJnQ7CJs/OkA=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: bed9e04a7fbdd413e715ac8d103dd66b_c859262f7b8611f180e15254006c9bbf
    ReservedCode2: TfLwojpVzKdBL9H2Kl5EwP/6b6zc/JiOtnW2DQIVpAF6SDD92kTETfRg6b2bRbjpmjHY4MJbLXEqmjBB4qX4MHX5yNBOJK1cc/V2b6nSiZd681NNvDJqTOQFlQj28QR5HkxDmiaJXDCLFnx6BnCCUWYUZE9EV8uMg1dBfDTKuLoLecXvJnQ7CJs/OkA=
---

# PsychoPy Project

基于 [PsychoPy](https://www.psychopy.org/) 的实验开发项目，支持本地开发与 Docker 部署。

## 目录结构

```
psychopy-project/
├── src/            # 实验代码
├── experiments/    # 实验定义文件 (.psyexp)
├── data/           # 实验数据
├── output/         # 结果输出
├── config/         # 配置文件
├── docker/         # Docker 相关配置
├── venv/           # 虚拟环境（本地）
└── requirements.txt
```

## 本地开发

```bash
cd psychopy-project
source venv/bin/activate
python src/your_experiment.py
```

## Docker 部署

```bash
cd psychopy-project/docker
docker compose up --build
```

## 依赖

- Python 3.11+
- PsychoPy 2026.1.3
- 详见 requirements.txt
*（内容由AI生成，仅供参考）*
