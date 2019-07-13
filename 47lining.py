
import math
import json
import sys

class batchClient(object):

    def get_color(self, batch_element):
        if batch_element[-1] == 'S' or batch_element[-1]== 'C':
            return 'Black'
        if batch_element[-1] == 'D' or batch_element[-1] == 'H':
            return 'Red'
        return ''

    def get_rank(self, batch_element):
        if batch_element[0] == 'A':
            return 1
        if len(batch_element) == 3:
            return int(batch_element[0] + batch_element[1])
        if len(batch_element) == 2 and batch_element[0].isdigit():
            return int(batch_element[0])
        if batch_element[0] in ['J', 'Q', 'K']:
            return 10
        return 0
    
    def get_suit(self, batch_element):
        return batch_element[-1]

    def waste_metric(self, batch):
        sum = 0
        for first, second in zip(batch, batch[1:]):
            if self.get_suit(first)==self.get_suit(second):
                sum = sum + math.fabs(self.get_rank(first) - self.get_rank(second))
            elif self.get_color(first) == self.get_color(second):
                sum = sum + 2 * (math.fabs(self.get_rank(first) - self.get_rank(second)))
            elif self.get_color(first) != self.get_color(second):
                sum = sum + 3 * (math.fabs(self.get_rank(first) - self.get_rank(second)))
        return sum

    def is_valid(self, line):
        valid_initial = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K"]
        ten = "10"
        valid_end = ["C","H", "S", "D"]
    
        if len(line) == 2 and line[0] in valid_initial and line[-1] in valid_end:
            return True
        if len(line)==3 and ten in line and line[-1] in valid_end:
            return True
        
        return False
    
    def valid_batch(self, batch):
        if len(batch) <> 52:
            return False
        for element in batch: 
            if self.is_valid(element):
                continue
            else:
                return False
        return True
    
    def read_file(self, batch_file):
        read_lines = []
        with open(batch_file) as file:
            for line in file:
                if line.startswith('"'):
                    line = line.strip('"')
                    read_lines.append(line)
                    print'Line is ' + line
        return read_lines


def main():
    print 'starting process batch file is ' + str(sys.argv[1])
    batch_client = batchClient()
    batch_file = sys.argv[1]
    batch = []
    with open(batch_file) as f:
        for line in f:
            line = line.strip().strip(',')
            if line.startswith('"'):
                line = line.strip('"')
                batch.append(line)           

    if not batch_client.valid_batch(batch):
        print'is-invalid-batch JSON-FILE ' + str(sys.argv[1])
    if batch_client.valid_batch(batch):
        waste_metric = batch_client.waste_metric(batch)
        print 'waste_metric JSON-FILE ' + str(waste_metric)


main()

     



        