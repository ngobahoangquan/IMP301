import heapq
from collections import defaultdict, Counter
from PIL import Image
import numpy as np

class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    # Comparator for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

def frequency_analysis(image):
    # Convert image to a numpy array
    pixels = np.array(image).flatten()
    return Counter(pixels)

def build_huffman_tree(freq_dict):
    priority_queue = [HuffmanNode(value, freq) for value, freq in freq_dict.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_huffman_codes(node, prefix='', codebook={}):
    if node is not None:
        if node.value is not None:
            codebook[node.value] = prefix
        generate_huffman_codes(node.left, prefix + '0', codebook)
        generate_huffman_codes(node.right, prefix + '1', codebook)
    return codebook

def encode_image(image, codebook):
    pixels = np.array(image).flatten()
    encoded_data = ''.join([codebook[pixel] for pixel in pixels])
    return encoded_data

def decode_image(encoded_data, huffman_tree, shape):
    decoded_pixels = []
    node = huffman_tree
    for bit in encoded_data:
        if bit == '0':
            node = node.left
        else:
            node = node.right

        if node.value is not None:
            decoded_pixels.append(node.value)
            node = huffman_tree

    return np.array(decoded_pixels).reshape(shape)

# Example Usage
image_path = '../Assignment_2/faebcdf0351d4290bb89a488203c741a.png'
image = Image.open(image_path).convert('L')  # Convert to grayscale
shape = image.size

# Step 1: Frequency Analysis
freq_dict = frequency_analysis(image)

# Step 2: Build Huffman Tree
huffman_tree = build_huffman_tree(freq_dict)

# Step 3: Generate Huffman Codes
huffman_codes = generate_huffman_codes(huffman_tree)

# Step 4: Encode Image
encoded_data = encode_image(image, huffman_codes)

# Step 5: Decode Image
decoded_image_array = decode_image(encoded_data, huffman_tree, shape)
decoded_image = Image.fromarray(decoded_image_array.astype('uint8'))

# Save or display the decoded image
decoded_image.save('decoded_image.png')
decoded_image.show()
