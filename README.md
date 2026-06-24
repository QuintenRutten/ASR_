# Audio Augmentation for Finetuned Whisper on Non-Native English Child Speech Recognition

## Abstract

ASR systems like Whisper often struggle with child speech compared to adult speech, because these systems are predominantly trained on adult speech. This problem becomes even bigger when using non-native speech data. To make these systems more effective for children with different accents, it is important to investigate how we can reduce the gap and increase model performance on non-native child speech. In this study we investigate two augmentation strategies, speed perturbation, and SpecAugment, to improve whisper model performance on non-native child speech. In addition to this, we investigate if combining these augmentation techniques leads to additional gain. Our results show that speed perturbation slightly reduces WER on non-native child speech. Combining both SpecAugment and speed perturbation leads to the best performing model with a difference of 0.8 in WER compared to just finetuning without augmentation. These findings indicate that applying augmentation strategies can indeed help to improve whisper model performance on non-native child speech. Future work should focus on incorporating more augmentation strategies.

## Codebase

We followed the paper of Jain et al. [1] for our code and hyperparameter setup.
The code is adapted from the whisper finetuning event for performing the ASR finetuning experiments with child speech. The original training and finetuning can be followed from the following link: https://github.com/huggingface/community-events/tree/main/whisper-fine-tuning-event. The finetuning and loading models notebooks in this repository are based on the notebooks from this event, with only minor adjustments made to accommodate for our data and hardware.

## Models
The finetuned models used in our study can be found here: https://huggingface.co/Kwimp/models

## references

[1] Jain, Rishabh & Barcovschi, Andrei & Yiwere, Mariam & Corcoran, Peter & Cucu, Horia. (2024). Exploring Native and Non-Native English Child Speech Recognition With Whisper. IEEE Access. PP. 1-1. 10.1109/ACCESS.2024.3378738. 
