# Font classification

## Abstract 

Optical character recognition is a critical task for  such as localization, mapping and obstacle detection. There has been a significant and growing interest in depth estimation from a single RGB image, due to the relatively low cost and size of monocular cameras. However, state-of-the-art single-view depth estimation algorithms are based on fairly complex deep neural networks that are too slow for real-time inference on an embedded platform, for instance, mounted on a micro aerial vehicle. In this project, I address the problem of fast font classification. I propose an efficient and lightweight network architecture. 

## Problem statement

Nowadays, the fraud detection is very popular issue in deep learning world, because it is a value technique for large demand. For instance, the bank transaction needs to proof the id, or some test needs to verify the id first. In order to find the fraud in the Id, there are several way to approach.
Currently, the text detection is the very popular topic. However, there are seldom article talks about font classification. In the fraud detection, the font type continuous is the important feature to distinguish the fake id. Therefore, this article will focus on the font classification.

## Related Work
First, using the synthetic dataset on training text task is common approach, because training needs lots of data and label this data needs lots of time. Therefore, inspired by SyntheText, this project use the synthetic data to training network. However, the original project use lots of natural images, which are too complex to training, so I only collected the driver lisences from each state. 

Second, according to "Character-independent font identification" , the challenge of font classification is that the font are countless and the font different is very small, for instance,
![](image/font.png)
Therefore, they provide the idea that train the model which can recognize the font different and base on subnet which learning the similar feature 

## Methodology 
### Dataset Generation
In order to simulate the background image which use the license, I used the inpainting algorithm to remove the text in the background, then paint the text on it. As the following picture:
![](image/image1.jpg)
### Architecture 
In order to run on the light resource demand environment, I decided to run on the light computing environment. After studying mobilenet, efficentnet, tinynet, I decided to use the mobilenet V3 to be the network architecture, because it seems it do the best in classification task.
![](image/model.png)


## Experiments
### the random image + random color char:
I found this is too difficult for the network to learning the feature map of the font. As the problem statement describe, which the different font has little pixel different, so the first model cannot train. So I decide to make the model recognize from the simple text to the complex condition
### the white background + black char (easiest):
I trained 1000 for four font for the model. The model shows the high accuracy on this simple task.
### the dark char + white background
I trained 10000 for four font with the dark char, which means each RGB channel's value under 50. At this point the model performs well 
![](image/0b.png) 
![](image/1b.png)
### the dark char + color background
Finally, I trained the 30000 for four fonts with dark char and color background.
![](image/0.png) 
![](image/1.png)
## Results

Overall, the accuracy of ArialFamily is 96% on test dataset. It seems the model conquer this problem. And the FPS is XX. Therefore, ArialFamily classification is finished.

## Examples 
![](sample/0.png)
predict: arial
![](sample/1.png)
predict: arialbd
![](sample/3.png)
predict: arialbi
![](sample/4.png)
predict: arialli
## Reference:
Mobilenet V3 :https://github.com/kuan-wang/pytorch-mobilenet-v3  
Character-independent font identification : https://arxiv.org/pdf/2001.08893.pdf  
SynthText: https://github.com/ankush-me/SynthText
