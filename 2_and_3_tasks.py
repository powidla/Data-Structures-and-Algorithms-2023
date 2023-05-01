class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        
    def add(self, key, value):
        index = self.hash(key)
        bucket = self.table[index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return  # key already exists, do not add a duplicate
        bucket.append((key, value))
        
    def delete(self, key):
        index = self.hash(key)
        bucket = self.table[index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                del bucket[i]
                return
        
    def get(self, key):
        index = self.hash(key)
        bucket = self.table[index]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1]
        return None
        
    def hash(self, key):
        p = 31
        m = self.size
        h = 0
        for i in range(len(key)):
            h = (h * p + ord(key[i])) % m
        return h
    
class KMerIndex:
    def __init__(self, sequence, k):
        self.sequence = sequence
        self.k = k
        self.index = HashTable(len(sequence) - k + 1)
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i+k]
            self.index.add(kmer, i)
            
    def get(self, kmer):
        return self.index.get(kmer)
class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.filter = [False] * size
        
    def add(self, key):
        for seed in range(self.hash_count):
            index = self.hash(key, seed) % self.size
            self.filter[index] = True
            
    def query(self, key):
        for seed in range(self.hash_count):
            index = self.hash(key, seed) % self.size
            if not self.filter[index]:
                return False
        return True
        
    def build(self, sequence, k):
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i+k]
            self.add(kmer)
            
    def hash(self, key, seed):
        h = 0
        for char in key:
            h = (h * seed + ord(char)) % self.size
        return h
sequence = "ATGACATGGAATCAGCATGTTAG"
k = 3
bloom_filter = BloomFilter(100, 5)
bloom_filter.build(sequence, k)

print(bloom_filter.query("ATG"))  # Output: True
print(bloom_filter.query("CCC"))  # Output: False