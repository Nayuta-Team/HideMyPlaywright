# 🎭 [HideMyPlaywright](https://github.com/Nayuta-Team/HideMyPlaywright)

[中文简体](./README.zh.md) English

## Warning

* **Only partially patched for Chromium**, which means even if you patch it, you won't be able to hide the automation features of `Firefox` and `Webkit`.

## Usage

Open the terminal in the folder where `.playwright` is located and run this command.

```batch

>python setup.py <your playwright root directory>

example:
// When no arguments are provided, it will patch the `./.playwright` in the current directory by default
python setup.py

or
// Patch the `_/src/bin/Release/.playwright`
python setup.py _/src/bin/Release/.playwright
```

## Automated Processes

* [x] [CloudFare] All non-interactive passed through

* [ ] [Others] Unknown

## Patched Operations

* [ ] [`Runtime.enable`](https://chromedevtools.github.io/devtools-protocol/tot/Runtime/#method-enable)
  * [x] Removed `Runtime.enable` event
  * [x] Modified method for retrieving `_context(world)` property
    * [x] Enable JS environment isolation (utility)
    * [ ] Main JS environment (main)
    * [x] Reset on frame/navigation occurrences (reset)
