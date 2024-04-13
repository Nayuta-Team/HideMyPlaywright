# 🎭 [HideMyPlaywright](https://github.com/Nayuta-Team/HideMyPlaywright) for Python

中文简体 [English](./README.en.md)

## 警告

* **只对 Chromium 的部分** 进行了修补, 这意味着即使你进行修补也无法隐藏 `Firefox` 和 `Webkit` 的自动程序特征

## 使用方法

在 `.playwright` 所在的文件夹打开终端

运行此命令

```batch

>python setup.py <你的playwright根目录>

example:
//当没有任何参数时, 会默认修补当前目录下的 `./.playwright`
python setup.py

或
//对 `_/src/bin/Release/.playwright` 进行修补
python setup.py _/src/bin/Release/.playwright
```

## 自动程序

* [x] [CloudFare] 非交互式全部通过

* [ ] [Others] 未知

## 修补的操作

* [ ] [`Runtime.enable`](https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-enable)
  * [x] 移除 `Runtime.enable` 事件
  * [x] 修改 `_context(world)` 属性的获取方法
    * [x] 启用JS环境隔离 (utility)
    * [ ] 主JS环境 (main)
    * [x] 在框架/导航时发生重置 (reset)
