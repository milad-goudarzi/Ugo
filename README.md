# Ugo
### Educational Robot

![IMG_6814](https://user-images.githubusercontent.com/20543988/189480615-e75f3fa7-6783-45c6-8d2f-a92192cd4bed.JPG)

Ugo is an educational robot, which makes learning a new language more fun. I was in charge of the speech recognition part and I used deepspeech Speech-To-Text engine from Mozilla: https://github.com/mozilla/DeepSpeech

The reason I chose DS is that DS is pretrained on the Mozilla common voices dataset: https://commonvoice.mozilla.org/en

The dataset consists of 15,234 validated hours in 96 languages. Each entry in the dataset consists of a unique MP3 and corresponding text file. Many of the 20,817 recorded hours in the dataset also include demographic metadata like age, sex, and accent that can help train the accuracy of speech recognition engines.

Also, using DS, we can output a model, which can be run on low power devices such as Raspberry Pi 4, which was also my case.

I fine-tuned this pretrained model with our own dataset, which consisted of only 1000 samples that were recorded by our team members. I made a program to record audio in the desired format for DS and subsequently, added some noise to them to have a better generalization of the model. Afterwards, I created the files which were needed for DS fine-tuning by preprocessing.ipynb notebook and next, trained the model on the Colab using deepspeech_finetune.ipynb, which is based on a notebook I found in Kaggle website and modified it based on my needs: https://www.kaggle.com/code/chamodsr/deepspeech-finetune-sl-accent
