<img src="https://raw.githubusercontent.com/jtl125/CHIPy8/master/chipy8/icon.png" width="60" align="right">

# CHIPy8

CHIPy8 is a simple python interpreter for CHIP8. It currently lacks most functions from interpreters such as interactive file loading, save states, debugging mode, etc. 

To install simply type on the terminal

```
pip install chipy8
```

And load and run any _.ch8_ file with the command 

```
chipy8 file/to/rom.ch8
```

Alternatively you can download the binary located on the releases tab (only working for GNU/Linux at the moment). To execute first you must give it permission by typing

```
chmod +x CHIPy8
```

And then execute either by double-clicking or through the command line. When launched this way you will be greeted by a black screen, drag and drop any `.ch8`, `.chip8` or `.c8` romfile to load and run it.

### Future development

- Add simple toolbar for file loading and reseting.
- Add customization options as well as the ability to save option presets.
- Support for SUPER-CHIP and XO-CHIP
- Implement a debugging mode.

### Thanks

The interpreter was done following the [guide to making a CHIP-8 emulator](https://tobiasvl.github.io/blog/write-a-chip-8-emulator) by Tobias V. Langhoff as well as inspiration from [Yet Another (Super) Chip 8 Emulator](https://tobiasvl.github.io/blog/write-a-chip-8-emulator) project by Craig Thomas

### Notes

The key mapping to the emulator is 

        PAD             KEYBOARD  
    1  2  3  C         1  2  3  4
    4  5  6  D   -->   q  w  e  r
    7  8  9  E   -->   a  s  d  f
    A  0  B  F         z  x  c  v
