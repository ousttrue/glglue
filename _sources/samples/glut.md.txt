# glut

* require glut.dll or freeglut.dll
* ビルド済み <https://www.transmissionzero.co.uk/software/freeglut-devel/>

pyOpenGL の freeglut の探索名が `freeglut64.vc14.dll` とかだった。
わかりにくいのでお勧めできない・・・。

`site-packages\OpenGL\platform\win32.py` の `def GLUT()` で決めているポイ？

```{gitinclude} HEAD examples/glut_sample.py
:language: python
:caption:
```
