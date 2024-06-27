import heapq
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    if not text:
        return None

    # Calculate frequency of each character
    frequency = Counter(text)

    # Create a priority queue (min-heap)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    # Build the Huffman tree
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(freq=node1.freq + node2.freq, left=node1, right=node2)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text, codebook):
    return ''.join(codebook[char] for char in text)

def huffman_decode(encoded_text, root):
    decoded_text = []
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root
    return ''.join(decoded_text)

# Example usage
if __name__ == "__main__":
    text = "abracadabra"
    root = build_huffman_tree(text)
    codebook = generate_huffman_codes(root)
    encoded_text = huffman_encode(text, codebook)
    decoded_text = huffman_decode(encoded_text, root)

    print("Original text:", text)
    print("Encoded text:", encoded_text)
    print("Decoded text:", decoded_text)
    print("Huffman Codes:", codebook)
