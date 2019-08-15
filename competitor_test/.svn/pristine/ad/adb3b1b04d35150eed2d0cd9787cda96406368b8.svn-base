## 概览
combine.py 作用为把n副A图与m副B图合成。合成的效果为B图居中位于A图的n副C图。

## 命令格式
```shell
python combine.py base_images_format over_images_format result_images_format
```
## 例子
把 path1 下所有格式为 image%05d.jpg(image00001.jpg) 的图片与 path2 下所有格式为 test%d.jpg(test1.jpg) 的图片合成格式为 result_images_%05d.jpg(result_images_00001.jpg) 的图片病置于 path3下

```shell
python combine.py /path1/image%05d.jpg /path2/test%d.jpg /path3/result_images_%05d.jpg
```
## 注意
### 1. 编号问题
假设输入格式为 image%05d.jpg 那么一定会从image00001.jpg开始编号

所以如果有 :

```
A: base_00001 ~ base_00009

B: over_00001 over_00002 over_00004 over_00005
```

那么会生成 :

```
C:
result_00001(A:base_00001 B:over_00001)
result_00002(A:base_00002 B:over_00002)
result_00003(A:base_00003 B:over_00001)
result_00004(A:base_00004 B:over_00002)
result_00005(A:base_00005 B:over_00001)
result_00006(A:base_00006 B:over_00002)
result_00007(A:base_00007 B:over_00001)
result_00008(A:base_00008 B:over_00002)
result_00009(A:base_00009 B:over_00001)
```

即如果找不到输入图片中间编号断了的话，会忽略后面的图片，所以只会在over_00001 over_00002之间循环。**所以需要保证好输入图片的编号连续性**

### 2. 找不到图片（第一张）
如果第一张开始就匹配不到给出的格式，就会抛出错误

### 3. 分辨率问题
默认认为 over 的分辨率应该是远远小于 base 的。如果出现 over 分辨率大于 base 则会抛错

### 4. 格式问题
如果是要匹配00001这样的数字记得要使用 %05d 而不是 %5d 这在 python 里面解析出来的格式不一样



