import numpy as np
import torch
from torch.utils.data import Dataset

np.random.seed(12345)

class Word2vecDataset(Dataset):
    def __init__(self, inputFileName, side_num = 0, neg_num = 5, sentences_count = 1000000):
        # self.data = data
        # self.window_size = window_size
        self.sentences_count = sentences_count
        self.neg_num = neg_num
        self.side_num = side_num
        self.input_file = open(inputFileName, encoding="utf8")
        self.sample_size=64*1000
        self.data = []
        self.weights=[]
        self.choices = []
        self.idx = 0

    def __len__(self):
        return self.sentences_count

    def __getitem__(self, idx):
        # no shuffle
        while True:
            if self.idx%self.sample_size==0:
                self.data = []
                self.idx = 0
                for i in range(self.sample_size):
                    line = self.input_file.readline().strip('\n')
                    if not line:
                        self.input_file.seek(0, 0)
                        line = self.input_file.readline().strip('\n')
                    if len(line) > 1 and len(line.split(' ')) == self.neg_num+3:
                        self.data.append(line)
                self.weights=[float(x.split(' ')[-1]) for x in self.data]
                self.choices = np.random.choice(a=self.data, size=self.sample_size, replace=True, p=np.array(self.weights)/sum(self.weights))

            # print(self.data)
            line = self.choices[self.idx%self.sample_size]
            words = [x for x in line.split(' ')[:-1]]
            assert len(words) == self.neg_num+2, str(words)
            assert len(words[0].split('_')) == self.side_num+1, str(words)
            self.idx += 1
            return [words[0],words[1],words[2:]]


    @staticmethod
    def collate(batches):
        all_u = [batch[0] for batch in batches if len(batch) > 0]
        all_u = [list(map(int,x.split('_'))) for x in all_u]
        all_v = [batch[1] for batch in batches if len(batch) > 0]
        all_v = [list(map(int,x.split('_'))) for x in all_v]
        all_neg_v = [batch[2] for batch in batches if len(batch) > 0]
        all_neg_v = [[list(map(int,x.split('_'))) for x in xx] for xx in all_neg_v]
        return torch.LongTensor(all_u), torch.LongTensor(all_v), torch.LongTensor(all_neg_v)
