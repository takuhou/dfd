# dfd

## 画像の撮影

* レンズぼかし画像の撮影は、[Googleカメラ](https://support.google.com/googlecamera/)などを用いてください。また、撮影したレンズぼかし画像からRGB画像+デプスマップ画像の取り出すために[depthy](http://depthy.me/)を利用してください。
* 取り出したRGB画像+デプスマップ画像を元にdfd画像作成プログラムが動きます。

## install

```
pip install pipenv
```

## exec dfd program

```
pipenv run python dfd.py
```


## 設計図

以下が装置の概念図と設計図です。

![概念図](https://user-images.githubusercontent.com/4945177/37301247-619c9780-266b-11e8-86d4-785cdeb01d3f.png)

![設計図](https://user-images.githubusercontent.com/4945177/37301149-2067bf74-266b-11e8-92c5-e3748fb4d96f.png)

## 構築手順

1. 図面をダンボールや画用紙、厚紙に印刷してください。
2. 灰色の枠に沿って図面を切り取ってください。
3. 黒線に沿って切り込みを入れてください。切り込みには、ハーフミラーとミラーを設置します。
4. 黒点線に沿って折ってください。
5. 各接点をテープ等で貼りつけてください。
6. 装置にスマートフォンを設置してください。

## 完成図

![完成図](https://user-images.githubusercontent.com/4945177/37301343-a6a4e422-266b-11e8-9bd4-9daa62428f22.jpg)
