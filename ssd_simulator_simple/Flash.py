from Block import Block

class Flash:
    def __init__(self, num_blocks, pages_per_block):
        self.blocks = [Block(pages_per_block) for _ in range(num_blocks)]
        self.pages_per_block = pages_per_block

    def find_free_page(self):
        for b_idx, block in enumerate(self.blocks):
            if block.has_free_page():
                p_idx = block.get_free_page_index()
                return b_idx, p_idx
            
        return None
    
    def read_page(self, b, p):
        return self.blocks[b].pages[p]
    
    def write_page(self, b, p, data):
        self.blocks[b].pages[p].write(data)

    def invalidate_page(self, b, p):
        self.blocks[b].pages[p].invalidate()

    def erase_block(self, b_idx):
        self.blocks[b_idx].erase()

    def get_block_info(self, b_idx):
        block = self.blocks[b_idx]
        return [(p.valid, p.data) for p in block.pages], block.erase_count
    
    
