from Page import Page

class Block:
    def __init__(self, pages_per_block):
        self.pages = [Page() for _ in range(pages_per_block)]
        self.erase_count = 0

    def erase(self):
        self.pages = [Page() for _ in range(self.pages)]
        self.erase_count += 1

    def get_invalid_count(self):
        return sum(1 for page in self.pages if page.data and not page.valid)
    
    def has_free_page(self):
        return any(page.is_free() for page in self.pages)
    
    def get_free_page_index(self):
        for i, page in enumerate(self.pages):
            if page.is_free():
                return i
            
        return None
    

    