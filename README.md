# Automatic-Mode-Switching-Utility-for-ASUS-TUF-Laptops
It monitors running applications and checks the whitelist to determine the required performance level. When high-performance software or games are detected, it automatically switches to Turbo Mode. Otherwise, it enables Silent or Balanced Mode to reduce power consumption and noise, improving efficiency and user experience.

## Usage

Create a whitelist file with one high-performance app per line:

```
blender
eldenring
```

Run the utility:

```
python mode_switcher.py --whitelist /path/to/whitelist.txt --dry-run
```
