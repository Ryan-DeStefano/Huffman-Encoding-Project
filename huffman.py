import os.path
from dataclasses import dataclass
from typing import List, Union, TypeAlias, Optional, Any

HTree: TypeAlias = Union[None, 'HuffmanNode']


@dataclass
class HuffmanNode:
    char_ascii: int  # stored as an integer - the ASCII character code value
    freq: int  # the frequency associated with the node
    left: HTree = None  # Huffman tree (node) to the left
    right: HTree = None  # Huffman tree (node) to the right

    def __lt__(self, other: HTree) -> bool:
        return comes_before(self, other)


def comes_before(a: HuffmanNode, b: HuffmanNode) -> bool:
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    elif a.freq == b.freq:
        if a.char_ascii < b.char_ascii:
            return True
        else:
            return False
    else:
        return False


def combine(a: HuffmanNode, b: HuffmanNode) -> HuffmanNode:
    """Creates a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lower of the a and b char ASCII values"""
    if a.freq < b.freq:
        if a.char_ascii < b.char_ascii:
            return HuffmanNode(a.char_ascii, a.freq + b.freq, a, b)
        else:
            return HuffmanNode(b.char_ascii, a.freq + b.freq, a, b)
    elif a.freq == b.freq:
        if a.char_ascii < b.char_ascii:
            return HuffmanNode(a.char_ascii, a.freq + b.freq, a, b)
        else:
            return HuffmanNode(b.char_ascii, a.freq + b.freq, b, a)
    else:
        if a.char_ascii < b.char_ascii:
            return HuffmanNode(a.char_ascii, a.freq + b.freq, b, a)
        else:
            return HuffmanNode(b.char_ascii, a.freq + b.freq, b, a)


def cnt_freq(filename: str) -> List:
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""
    if os.path.isfile(filename) is False:
        raise FileNotFoundError
    with open(filename) as file:
        data = file.read()
    values = [0] * 256
    for char in data:
        values[ord(char)] = values[ord(char)] + 1
    return values


def huff_helper(huf_lis: List) -> None:
    "Helps deal with sorting issues not caught by python's built in sort function"
    for x in range(len(huf_lis) - 1):
        if comes_before(huf_lis[x], huf_lis[x + 1]) is False:
            huf_lis[x], huf_lis[x + 1] = huf_lis[x + 1], huf_lis[x]
            huff_helper(huf_lis)


def create_huff_tree(char_freq: List) -> Optional[HuffmanNode]:
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""
    if sum(char_freq) == 0:
        return None
    else:
        huf_lis = []
        i = 0
        for freq in char_freq:
            if freq != 0:
                huf_lis.append(HuffmanNode(i, freq))
            i += 1
        huf_lis.sort(key=lambda HuffmanNode: HuffmanNode.freq, reverse=False)
        huff_helper(huf_lis)
        while len(huf_lis) >= 2:
            new_node = combine(huf_lis[0], huf_lis[1])
            huf_lis.append(new_node)
            huf_lis = huf_lis[2:]
            huf_lis.sort(key=lambda HuffmanNode: HuffmanNode.freq, reverse=False)
            huff_helper(huf_lis)
        return huf_lis[0]


def create_code(node: Optional[HuffmanNode]) -> List:
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the array, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""
    py_list = [''] * 256
    create_code_helper(node, '', py_list)
    return py_list


def create_code_helper(node: HuffmanNode, code, py_list: List[Any]) -> None:
    if node.left is None and node.right is None:
        py_list[node.char_ascii] = code
    else:
        create_code_helper(node.left, code + "0", py_list)
        create_code_helper(node.right, code + "1", py_list)


def create_header(freqs: List) -> str:
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    header = ""
    count = 0
    for freq in freqs:
        if freq != 0:
            header = header + str(count) + ' ' + str(freq) + ' '
        count += 1
    header = header[0:len(header) - 1]
    return header


def huffman_encode(in_file: str, out_file: str) -> None:
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take note of special cases - empty file and file with only one unique character"""
    freqlist = cnt_freq(in_file)
    huff = create_huff_tree(freqlist)
    if huff is None:
        output = open(out_file, "w")
        output.close()
    else:
        code_list = create_code(huff)
        with open(in_file) as file:
            phrase = file.read()
        code = ''
        for char in phrase:
            code = code + code_list[ord(char)]
        header = create_header(freqlist)
        output = open(out_file, "w")
        output.write(header + "\n")
        output.write(code)
        output.close()