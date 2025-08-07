# Minecraft Audio Resource Pack Generator
## 我的世界音频资源包生成器 v2.0.0

[![Minecraft版本](https://img.shields.io/badge/Minecraft-1.6.1--1.21.6-green.svg)](https://minecraft.net/)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org/)

> 一个功能强大的Minecraft音频资源包生成工具，支持自动音频格式转换、多线程处理、智能配置管理和完整的资源包生成流程

### 项目简介

本工具可以帮助您快速生成Minecraft音频资源包，具备以下核心功能：
- **多格式音频支持**: 转换 MP3/WAV 到 OGG 格式
- **多线程处理**: 并发的音频转换
- **完整资源包生成**: 自动生成 pack.mcmeta、sounds.json 等


---
## 使用方法
### 快速开始

#### 步骤1：准备音频文件
将需要生成资源包的音频文件放入项目目录下的 `audios` 文件夹中（如不存在会自动创建）

#### 步骤2：运行生成器
```bash
python main.py
```

#### 步骤3：配置资源包信息
程序首次运行会创建 `config.json` 配置文件，您可以选择：

**交互式配置** - 按照界面提示输入：
- **资源包名称** (默认: "我的音频资源包")
- **命名空间** (默认: "custom_sounds") - 只能包含小写字母、数字和下划线
- **Minecraft版本** - 从15个支持的版本范围中选择
- **资源包描述** (默认: "自定义音频资源包")

**使用已有配置** - 如果配置文件已存在且完整，可以直接使用

#### 步骤4：音频处理与转换
程序会自动进行以下操作：
- 检查FFmpeg可用性（用于MP3/WAV转换）
- 验证音频文件名格式（只允许小写字母、数字、下划线）
- 多线程并发转换音频文件到OGG格式
- 生成完整的资源包目录结构

#### 步骤5：获取生成的资源包
1. 在 `resource_pack` 文件夹中找到生成的资源包文件夹和ZIP文件
2. 将ZIP文件复制到Minecraft游戏目录下的 `resourcepacks` 文件夹
3. 在游戏中的资源包设置中启用该资源包

### 在游戏中使用
启用资源包后，使用以下命令播放自定义音频：
```
/playsound minecraft:<音频文件名> master @p
```
例如：如果您有音频文件 `background_music.ogg`，则使用：
```
/playsound minecraft:background_music master @p
```
你可以在材质包内的README.md(\resource_pack\测试音效包)查看，程序自动生成的命令

```markdown
## 可用音频列表
- `ghost_jiao` - 使用命令: `/playsound minecraft:ghost_jiao master @p`
- `face_logo` - 使用命令: `/playsound minecraft:face_logo master @p`
- `ghost2_look` - 使用命令: `/playsound minecraft:ghost2_look master @p`
- `happy_sound` - 使用命令: `/playsound minecraft:happy_sound master @p`
- `gutou` - 使用命令: `/playsound minecraft:gutou master @p`
- `hit_logo` - 使用命令: `/playsound minecraft:hit_logo master @p`
- `ghost_look` - 使用命令: `/playsound minecraft:ghost_look master @p`
- `loop_badend` - 使用命令: `/playsound minecraft:loop_badend master @p`
- `horror_background` - 使用命令: `/playsound minecraft:horror_background master @p`
```
---


##  高级配置

### config.json 配置详解

程序首次运行会生成 `config.json` 配置文件，您可以手动编辑以实现高级功能：

```json
{
  "pack_name": "我的音频资源包",
  "namespace": "custom_sounds",
  "minecraft_version": "1.21.6",
  "description": "自定义音频资源包",
  "author": "资源包制作者",
  "supported_formats": [".ogg", ".wav", ".mp3"],
  "auto_convert": true,
  "output_zip": true,
  "conversion_settings": {
    "quality": "high",
    "bitrate": "128k",
    "sample_rate": 44100,
    "max_workers": 4
  }
}
```

### 配置参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `pack_name` | string | "我的音频资源包" | 资源包显示名称 |
| `namespace` | string | "custom_sounds" | 音频命名空间（影响播放命令） |
| `minecraft_version` | string | "1.21.6" | 目标Minecraft版本 |
| `description` | string | "自定义音频资源包" | 资源包描述 |
| `author` | string | "资源包制作者" | 作者信息 |
| `supported_formats` | array | [".ogg", ".wav", ".mp3"] | 支持的音频格式 |
| `auto_convert` | boolean | true | 是否自动转换非OGG格式 |
| `output_zip` | boolean | true | 是否生成ZIP压缩包 |

### 音频转换设置

| 参数 | 选项 | 说明 |
|------|------|------|
| `quality` | "high"/"medium"/"low" | 音频压缩质量 |
| `bitrate` | "128k"/"192k"/"256k" | 音频比特率 |
| `sample_rate` | 44100/48000/22050 | 采样率 |
| `max_workers` | 1-8 | 并发转换线程数 |

### 性能调优建议

**高质量设置**（适合音乐类音频）：
```json
"conversion_settings": {
  "quality": "high",
  "bitrate": "192k",
  "sample_rate": 48000,
  "max_workers": 2
}
```

**平衡设置**（推荐）：
```json
"conversion_settings": {
  "quality": "medium",
  "bitrate": "128k",
  "sample_rate": 44100,
  "max_workers": 4
}
```

**快速转换**（适合大量音效）：
```json
"conversion_settings": {
  "quality": "low",
  "bitrate": "96k",
  "sample_rate": 22050,
  "max_workers": 6
}
```

## 系统要求

### 必需依赖
- **Python 3.6 或更高版本**
- **FFmpeg** - 用于音频格式转换和处理（仅在需要转换MP3/WAV文件时必需）

### FFmpeg 安装指南

> **重要提示**: 如果您只使用 `.ogg` 格式的音频文件，可以跳过FFmpeg安装。程序会自动检测FFmpeg可用性，如未安装则仅处理OGG文件。

#### Windows 用户
1. 访问 [FFmpeg官网](https://ffmpeg.org/download.html) 下载Windows版本
2. 解压到任意目录（如 `C:\ffmpeg`）
3. 将FFmpeg的bin目录添加到系统PATH环境变量中
4. 在命令提示符中运行 `ffmpeg -version` 验证安装

#### macOS 用户
使用Homebrew安装：
```bash
brew install ffmpeg
```

#### Linux 用户
Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

CentOS/RHEL:
```bash
sudo yum install ffmpeg
```

---

## 重要注意事项

### 文件命名规范（严格要求）
- **音频文件名只能包含小写英文字母、数字和下划线**
- **避免出现大写字母、中文字符、空格或特殊符号！**
- **比如**：
  - √ `background_music.ogg`
  - √ `sound_effect_01.mp3`
  - √ `boss_battle.wav`
  - × `Background-Music.mp3`
  - × `音乐文件.ogg`
  - × `Sound Effect.wav`

### 支持的音频格式
- **`.ogg`** - 推荐格式，Minecraft原生支持，无需转换
- **`.mp3`** - 常用格式，自动转换为OGG（需要FFmpeg）
- **`.wav`** - 无损格式，自动转换为OGG（需要FFmpeg）

###  音频转换设置
程序支持自定义转换参数（在 `config.json` 中配置）：
- **质量等级**: high/medium/low (默认: high)
- **比特率**: 默认 128k
- **采样率**: 默认 44100Hz
- **并发线程数**: 默认 4个

### 文件大小建议
- 单个音频文件建议不超过 **10MB**
- 整个资源包建议不超过 **100MB** 以确保游戏性能
- 对于背景音乐，建议使用较低的比特率以减小文件大小

### Minecraft版本兼容性
程序自动根据选择的Minecraft版本设置正确的 `pack_format` 值：
- 1.6.1-1.8.8: pack_format 1
- 1.9-1.10.2: pack_format 2
- 1.11-1.12.2: pack_format 3
- ...
- 1.21.6: pack_format 55 (最新)

新版本资源包向下兼容，但建议选择与您的游戏版本匹配的设置。

---

## 项目结构

```
Minecraft-Audio-Resource-Pack-Generator/
├── main.py                     # 主程序文件
├── config.json                 # 配置文件（自动生成）
├── audios/                     # 音频文件存放目录
│   ├── background_music.ogg    # 示例：背景音乐
│   ├── sound_effect.mp3        # 示例：音效文件
│   └── boss_battle.wav         # 示例：Boss战斗音乐
├── resource_pack/              # 生成的资源包输出目录
│   ├── 我的音频资源包/          # 资源包文件夹
│   │   ├── pack.mcmeta         # 资源包元数据
│   │   ├── README.md           # 使用说明
│   │   └── assets/
│   │       └── minecraft/
│   │           ├── sounds.json # 音频定义文件
│   │           └── sounds/
│   │               └── custom_sounds/  # 音频文件目录
│   │                   ├── background_music.ogg
│   │                   ├── sound_effect.ogg
│   │                   └── boss_battle.ogg
│   └── 我的音频资源包.zip       # 压缩包（可直接使用）
└── README.md                   # 项目说明文档
```

### 生成的文件说明
- **pack.mcmeta**: 包含资源包版本信息和描述
- **sounds.json**: 定义所有音频文件的播放参数
- **README.md**: 包含使用方法和可用音频列表
- **音频文件**: 转换后的OGG格式音频文件

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

### 贡献指南
1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b TianKong-y/Minecraft-Audio-Resource-Pack-Generator`)
3. 提交您的更改 (`git commit -m 'Add some Minecraft-Audio-Resource-Pack-Generator'`)
4. 推送到分支 (`git push origin TianKong-y/Minecraft-Audio-Resource-Pack-Generator`)
5. 开启一个Pull Request

---

## 联系方式

- 原作者：bilibili@TianKong_y
- 二次开发者：Thexiaoyu
- 问题反馈：请在GitHub Issues中提交

---

**如果这个工具对您有帮助，请给个⭐Star支持一下！**
