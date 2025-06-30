from Flash import Flash

class FTL:
    def __init__(self, num_blocks, pages_per_block):
        self.flash = Flash(num_blocks, pages_per_block)
        self.mapping_table = {}

    def write(self, lpn, data):
        location = self.flash.find_free_page()
        if not location:
            print("No Free Page, Operating GC")
            self.gc()
            location = self.flash.find_free_page()
            if not location:
                print("GC Failed, There is no space left")
                return
            
        b, p = location
        if lpn in self.mapping_table:
            old_b, old_p = self.mapping_table[lpn]
            self.flash.invalidate_page(old_b, old_p)
        self.flash.write_page(b, p, data)
        self.mapping_table[lpn] = (b, p)
        print(f"Write LPN {lpn} -> PPN({b}, {p}) = {data}")


    def read(self, lpn):
        if lpn not in self.mapping_table:
            print(f"Read Fail : LPN {lpn} not found")
            return
        
        b, p = self.mapping_table[lpn]
        page = self.flash.read_page(b, p)
        if not page.valid:
            print(f"Read Fail : LPN {lpn} mapped to invalid page")
        else:
            print(f"Read LPN {lpn} from PPN ({b}, {p}) = {page.data}")

    def gc(self):
        max_invalid = -1
        target = -1
        for i, block in enumerate(self.flash.blocks):
            count = block.get_invalid_count()
            if count > max_invalid:
                max_invalid = count
                target = i

        if max_invalid <= 0:
            print("GC : No reclaimable blocks")
            return
        
        print(f"GC triggered on block {target}")


        for p_idx, page in enumerate(self.flash.blocks[target].pages):
            if page.valid:
                for lpn, (b,p) in self.mapping_table.items():
                    if (b,p) == (target, p_idx):
                        new_loc = self.flash.find_free_page()
                        if new_loc:
                            nb, np = new_loc
                            self.flash.write_page(nb, np, page.data)
                            self.mapping_table[lpn] = (nb, np)
                            print(f"Move LPN {lpn} ({target}, {p_idx}) -> ({nb}, {np})")
        self.flash.erase_block(target)
        print(f"Erase block {target}")

            
            