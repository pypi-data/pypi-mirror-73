#coding:utf8
from __future__ import print_function
from __future__ import unicode_literals
from LAC import LAC

print("###### test seg ##########")
lac = LAC(mode='seg')
print("seg result", " ".join(lac.run("我来自中山大学")))

lac.train(model_save_dir='my_seg_model', train_data="data/pkutrain_example.utf8",
          test_data='data/pku_test_gold.utf8', thread_num=20)
#lac.train(model_save_dir='my_seg_model', train_data="data/pkutrain_example.utf8")

print("seg after result", " ".join(lac.run("我来自中山大学")))

print("seg before custom", " ".join(lac.run("春天的花开秋天的风以及冬天的落阳")))
lac.load_customization('data/custom1.txt')
print("seg after custom", " ".join(lac.run("春天的花开秋天的风以及冬天的落阳")))


print("###### test lac ##########")
lac = LAC()
print("lac result", " ".join(lac.run("我来自中山大学")[0]))

lac.train(model_save_dir='my_lac_model', train_data="data/tag_train.txt",
          test_data='data/tag_test.txt', thread_num=20)

print("seg after result", " ".join(lac.run("我来自中山大学")[0]))

print("seg before custom", " ".join(lac.run("春天的花开秋天的风以及冬天的落阳")[0]))
lac.load_customization('data/custom1.txt')
print("seg after custom", " ".join(lac.run("春天的花开秋天的风以及冬天的落阳")[0]))

print("seg before custom", " ".join(lac.run("the shy有点小帅")[0]))
lac.load_customization('data/custom2.txt', '\t')
print("seg after custom", " ".join(lac.run("the shy有点小帅")[0]))

lac = LAC(mode='seg')
print(" ".join(lac.run("我来自中山大学")))
lac.load_model('my_seg_model')
print(" ".join(lac.run("我来自中山大学")))
lac.load_model('my_lac_model')
print(lac.run("我来自中山大学"))

lac = LAC()
print(" ".join(lac.run("我来自中山大学")[0]))
lac.load_model('my_seg_model')
print(" ".join(lac.run("我来自中山大学")[0]))
lac.load_model('my_lac_model')
print(" ".join(lac.run("我来自中山大学")[0]))

