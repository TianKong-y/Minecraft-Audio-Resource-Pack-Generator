#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minecraft音频资源包生成器 v2.0.0
作者: 改进版 powered by bilibili@TianKong_y
二次更新：By Thexiaoyu
支持Minecraft 1.6.1 - 1.21.6
"""

import os
import json
import shutil
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class MinecraftAudioPackGenerator:
    """Minecraft音频资源包生成器"""
    
    VERSION_MAP = {
        "1.6.1-1.8.8": 1,
        "1.9-1.10.2": 2,
        "1.11-1.12.2": 3,
        "1.13-1.14.4": 4,
        "1.15-1.16.1": 5,
        "1.16.2-1.16.5": 6,
        "1.17-1.17.1": 7,
        "1.18-1.18.2": 8,
        "1.19-1.19.2": 9,
        "1.19.3": 12,
        "1.19.4-1.19.4": 13,
        "1.20-1.20.1": 15,
        "1.20.2": 18,
        "1.20.3-1.20.4": 22,
        "1.20.5-1.20.6": 32,
        "1.21-1.21.1": 34,
        "1.21.2-1.21.5": 41,
        "1.21.6": 55  # 最新稳定版本
    }
    
    def __init__(self):
        self.config = {} 
        self.base_path = Path.cwd() # 使用Path(__file__).parent会造成编译的exe出现temp目录路径问题
        self.config_file = self.base_path / "config.json"
        self.audios_folder = self.base_path / "audios"
        self.output_folder = self.base_path / "resource_pack"
        
    def load_config(self) -> bool:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                print(" 已加载配置文件")
                return True
            except Exception as e:
                print(f" 配置文件加载失败: {e}")
                return False
        return False
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            "pack_name": "我的音频资源包",
            "namespace": "custom_sounds",
            "minecraft_version": "1.21.6",
            "description": "自定义音频资源包",
            "author": "资源包制作者",
            "supported_formats": [".ogg", ".wav", ".mp3"],
            "auto_convert": True,
            "output_zip": True,
            "conversion_settings": {
                "quality": "high",
                "bitrate": "128k",
                "sample_rate": 44100,
                "max_workers": 4
            }
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            print(" 已创建默认配置文件 config.json")
            self.config = default_config
        except Exception as e:
            print(f" 创建配置文件失败: {e}")
    
    def validate_namespace(self, namespace: str) -> bool:
        """验证命名空间格式"""
        import re
        return bool(re.match(r'^[a-z0-9_]+$', namespace))
    
    def get_pack_format(self, version_key: str) -> int:
        """获取对应版本的pack_format"""
        return self.VERSION_MAP.get(version_key, 55)  # 默认最新版本
    
    def setup_interactive_config(self):
        """交互式配置设置"""
        print("\n" + "="*50)
        print("Minecraft音频资源包生成器 v2.0.0")
        print("="*50)
        
        required_keys = ["pack_name", "namespace", "minecraft_version", "description"]
        if all(key in self.config and self.config[key] for key in required_keys):
            print(" 检测到完整配置文件，使用已有配置:")
            print(f"  - 资源包名称: {self.config['pack_name']}")
            print(f"  - 命名空间: {self.config['namespace']}")  
            print(f"  - Minecraft版本: {self.config['minecraft_version']}")
            print(f"  - 描述: {self.config['description']}")
            
            use_config = input("\n是否使用此配置？(Y/n): ").strip().lower()
            if use_config != 'n':
                print(" 使用已有配置")
                return
        
        print("\n请配置资源包信息:")
        
        default_name = self.config.get("pack_name", "我的音频资源包")
        pack_name = input(f"请输入资源包名称 (默认: {default_name}): ").strip()
        if not pack_name:
            pack_name = default_name
        
        default_namespace = self.config.get("namespace", "custom_sounds")
        while True:
            namespace = input(f"请输入命名空间 (默认: {default_namespace}): ").strip()
            if not namespace:
                namespace = default_namespace
            
            if self.validate_namespace(namespace):
                break
            print(" 命名空间只能包含小写字母、数字和下划线")
        
        print("\n支持的Minecraft版本:")
        for i, version in enumerate(self.VERSION_MAP.keys(), 1):
            format_num = self.VERSION_MAP[version]
            print(f"{i:2d}. {version:<20} (pack_format: {format_num})")
        
        default_version = self.config.get("minecraft_version", "1.21.6")
        version_input = input(f"\n请选择版本编号或直接输入 (默认: {default_version}): ").strip()
        
        if version_input.isdigit():
            version_list = list(self.VERSION_MAP.keys())
            version_index = int(version_input) - 1
            if 0 <= version_index < len(version_list):
                minecraft_version = version_list[version_index]
            else:
                minecraft_version = default_version
        elif version_input in self.VERSION_MAP:
            minecraft_version = version_input
        elif not version_input:
            minecraft_version = default_version
        else:
            minecraft_version = default_version
        
        default_desc = self.config.get("description", "自定义音频资源包")
        description = input(f"请输入资源包描述 (默认: {default_desc}): ").strip()
        if not description:
            description = default_desc
        
        self.config.update({
            "pack_name": pack_name,
            "namespace": namespace,
            "minecraft_version": minecraft_version,
            "description": description
        })
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(" 配置已保存")
        except Exception as e:
            print(f" 保存配置失败: {e}")
    
    def create_directories(self, pack_path: Path):
        """创建资源包目录结构"""
        directories = [
            pack_path,
            pack_path / "assets" / "minecraft" / "sounds" / self.config["namespace"]
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def check_ffmpeg_availability(self) -> bool:
        """检查ffmpeg是否可用"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
        except Exception:
            return False

    def convert_single_audio(self, file_path: Path, target_dir: Path) -> Optional[Path]:
        """转换单个音频文件为ogg格式"""
        if file_path.suffix.lower() == '.ogg':
            target_path = target_dir / file_path.name
            shutil.copy2(file_path, target_path)
            return target_path
        
        if not self.config.get("auto_convert", False):
            return None
        
        try:
            conversion_settings = self.config.get("conversion_settings", {})
            quality = conversion_settings.get("quality", "high")
            bitrate = conversion_settings.get("bitrate", "128k")
            sample_rate = conversion_settings.get("sample_rate", 44100)
            
            ogg_filename = file_path.stem + '.ogg'
            ogg_path = target_dir / ogg_filename
            
            cmd = [
                'ffmpeg', '-i', str(file_path),
                '-acodec', 'libvorbis',
                '-ab', bitrate,
                '-ar', str(sample_rate),
                '-loglevel', 'error',
                '-y',  
                str(ogg_path)
            ]
            
            if quality == "high":
                cmd.extend(['-q:a', '2'])  # 高质量
            elif quality == "medium":
                cmd.extend(['-q:a', '4'])  # 中等质量
            else:
                cmd.extend(['-q:a', '6'])  # 低质量
            
            if sys.platform == 'win32':
                result = subprocess.run(
                    cmd,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    timeout=60,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    encoding='utf-8',
                    errors='ignore'
                )
            else:
                # Unix/Linux系统
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            
            return ogg_path
            
        except subprocess.TimeoutExpired:
            print(f" 转换超时: {file_path.name}")
            return None
        except subprocess.CalledProcessError as e:
            try:
                if hasattr(e, 'stderr') and e.stderr:
                    error_msg = str(e.stderr).strip()
                else:
                    error_msg = f"转换进程返回错误代码: {e.returncode}"
            except (UnicodeDecodeError, AttributeError):
                error_msg = f"编码错误 (返回代码: {getattr(e, 'returncode', 'unknown')})"
            print(f" 转换失败: {file_path.name} - {error_msg}")
            return None
        except FileNotFoundError:
            print(f" 未找到ffmpeg，无法转换 {file_path.name}")
            print("请安装ffmpeg: https://ffmpeg.org/download.html")
            return None
        except Exception as e:
            print(f" 转换出错: {file_path.name} - {str(e)}")
            return None

    async def convert_audio_files_async(self, audio_files: List[Path], target_dir: Path) -> List[str]:
        """异步批量转换音频文件"""
        max_workers = self.config.get("conversion_settings", {}).get("max_workers", 4)
        successful_files = []
        
        need_conversion = any(f.suffix.lower() != '.ogg' for f in audio_files)
        
        if need_conversion and self.config.get("auto_convert", False):
            if not self.check_ffmpeg_availability():
                print("  警告: 未找到ffmpeg，将跳过音频转换")
                print("   如需转换MP3/WAV文件，请安装ffmpeg: https://ffmpeg.org/download.html")
                # 只处理OGG文件
                audio_files = [f for f in audio_files if f.suffix.lower() == '.ogg']
                if not audio_files:
                    return []
        
        print(f"🔄 开始处理音频文件 (使用 {max_workers} 个并发线程)...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(self.convert_single_audio, file_path, target_dir): file_path
                for file_path in audio_files
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result_path = future.result()
                    if result_path:
                        successful_files.append(file_path.stem)
                        print(f" 已处理: {file_path.name}")
                    else:
                        print(f" 处理失败: {file_path.name}")
                except Exception as e:
                    print(f" 处理文件时出错 {file_path.name}: {str(e)}")
        
        return successful_files
    
    async def process_audio_files(self) -> List[str]:
        """处理音频文件"""
        if not self.audios_folder.exists():
            self.audios_folder.mkdir()
            print(f" 已创建 {self.audios_folder} 文件夹，请将音频文件放入其中")
            return []
        
        supported_formats = self.config.get("supported_formats", [".ogg", ".wav", ".mp3"])
        
        audio_files_to_process = []
        for file_path in self.audios_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                stem = file_path.stem
                if not self.validate_namespace(stem):
                    print(f" 跳过文件 {file_path.name}: 文件名只能包含小写字母、数字和下划线")
                    continue
                audio_files_to_process.append(file_path)
        
        if not audio_files_to_process:
            print(" 未找到有效的音频文件")
            return []
        
        pack_path = self.output_folder / self.config["pack_name"]
        target_path = pack_path / "assets" / "minecraft" / "sounds" / self.config["namespace"]
        target_path.mkdir(parents=True, exist_ok=True)
        
        successful_files = await self.convert_audio_files_async(audio_files_to_process, target_path)
        
        print(f" 成功处理 {len(successful_files)} 个音频文件")
        return successful_files
    
    def create_pack_mcmeta(self, pack_path: Path):
        """创建pack.mcmeta文件"""
        pack_format = self.get_pack_format(self.config["minecraft_version"])
        
        mcmeta_data = {
            "pack": {
                "pack_format": pack_format,
                "description": self.config["description"]
            }
        }
        
        if pack_format >= 18:
            mcmeta_data["pack"]["supported_formats"] = {
                "min_inclusive": pack_format,
                "max_inclusive": 55  # 当前最新
            }
        
        mcmeta_path = pack_path / "pack.mcmeta"
        with open(mcmeta_path, 'w', encoding='utf-8') as f:
            json.dump(mcmeta_data, f, ensure_ascii=False, indent=2)
    
    def create_sounds_json(self, pack_path: Path, audio_files: List[str]):
        """创建sounds.json文件"""
        sounds_data = {}
        namespace = self.config["namespace"]
        
        for audio_name in audio_files:
            sounds_data[audio_name] = {
                "sounds": [
                    {
                        "name": f"{namespace}/{audio_name}",
                        "volume": 1.0,
                        "pitch": 1.0
                    }
                ]
            }
        
        sounds_path = pack_path / "assets" / "minecraft" / "sounds.json"
        with open(sounds_path, 'w', encoding='utf-8') as f:
            json.dump(sounds_data, f, ensure_ascii=False, indent=2)
    
    def create_readme(self, pack_path: Path, audio_files: List[str]):
        """创建使用说明文件"""
        readme_content = f"""# {self.config['pack_name']}

## 资源包信息
- **名称**: {self.config['pack_name']}
- **命名空间**: {self.config['namespace']}
- **支持版本**: Minecraft {self.config['minecraft_version']}
- **描述**: {self.config['description']}

## 使用方法
在游戏中使用以下命令播放音频:

```
/playsound minecraft:<音频名称> <播放类型> <目标玩家> [坐标] [音量] [音调]
```

## 可用音频列表
"""
        
        for audio_name in audio_files:
            readme_content += f"- `{audio_name}` - 使用命令: `/playsound minecraft:{audio_name} master @p`\n"
        
        readme_content += f"""
## 安装方法
1. 将此文件夹压缩为ZIP文件
2. 将ZIP文件放入Minecraft的resourcepacks文件夹
3. 在游戏设置中启用此资源包

生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_path = pack_path / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def create_zip_package(self, pack_path: Path):
        """创建ZIP压缩包"""
        if not self.config.get("output_zip", True):
            return
        
        try:
            zip_path = pack_path.with_suffix('.zip')
            shutil.make_archive(str(pack_path), 'zip', str(pack_path))
            print(f" 已创建ZIP文件: {zip_path}")
        except Exception as e:
            print(f" 创建ZIP文件失败: {e}")
    
    async def generate_pack(self):
        """生成资源包"""
        print("\n开始生成资源包...")
        
        pack_path = self.output_folder / self.config["pack_name"]
        if pack_path.exists():
            shutil.rmtree(pack_path)
        
        self.create_directories(pack_path)
        print(f" 已创建目录结构")
        
        audio_files = await self.process_audio_files()
        if not audio_files:
            print(" 未找到有效的音频文件")
            return False
        
        print(f" 已处理 {len(audio_files)} 个音频文件")
        
        self.create_pack_mcmeta(pack_path)
        self.create_sounds_json(pack_path, audio_files)
        self.create_readme(pack_path, audio_files)
        print(" 已创建配置文件")
        
        self.create_zip_package(pack_path)
        
        print(f"\n 资源包生成完成!")
        print(f" 输出位置: {pack_path}")
        print(f" 包含音频: {len(audio_files)} 个")
        print(f" 支持版本: Minecraft {self.config['minecraft_version']}")
        
        return True

async def main():
    """主函数"""
    generator = MinecraftAudioPackGenerator()
    
    if not generator.load_config():
        generator.create_default_config()
    
    generator.setup_interactive_config()
    
    success = await generator.generate_pack()
    
    if success:
        input("\n按Enter键退出...")
    else:
        input("\n生成失败，按Enter键退出...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n程序出现错误: {e}")
        input("按Enter键退出...")
