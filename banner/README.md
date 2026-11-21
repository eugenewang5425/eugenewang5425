# CRT Banner 源码

`make_banner.py` 生成绿色 CRT 终端动画，包含像素头像、打字、扫描线和开关机效果。动画展示及源码入口已从个人主页移除；此目录保留生成源码与使用方法。仓库根目录的 `banner_dark.gif` 与 `banner_light.gif` 是历史导出文件。

## 运行

在仓库根目录安装依赖并生成深、浅色版本：

```powershell
python -m pip install -r banner/requirements.txt
python banner/make_banner.py --theme dark
python banner/make_banner.py --theme light
```

生成结果在 `banner/out/`，仅供单独预览。

默认从 GitHub 下载配置中用户的头像；也可使用本地图片：

```powershell
python banner/make_banner.py --avatar C:/path/to/avatar.png --theme dark
```

脚本顶部的 `CONFIG` 控制用户名、显示文字与颜色；`--out` 可指定输出路径。`--user` 只改变下载头像的用户，终端内的文字仍由 `CONFIG` 控制。

`banner/_build/` 保存缓存与中间帧，`banner/out/` 保存生成结果，均不提交。脚本会复用已有终端帧；修改文字或头像时，请在一个新的源码副本中生成，避免复用旧缓存。依赖未锁定版本；本次只保留源码，未重新生成现有动图，也不承诺逐字节复现。

## 参考

视觉风格参考 [yetone 的个人主页](https://github.com/yetone)。终端帧由 [github-readme-terminal / gifos](https://github.com/x0rzavi/github-readme-terminal) 生成，CRT 合成与 GIF 编码使用 Pillow 和 NumPy。
