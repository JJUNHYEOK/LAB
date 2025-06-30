from FTL import FTL

class Simulator:
    def __init__(self):
        self.ftl = FTL(num_blocks=4, pages_per_block=4)

    def run(self):
        print("SSD Simulation on Working")
        print()

        self.ftl.write(0, "A")
        self.ftl.write(1, "B")
        self.ftl.write(2, "C")
        self.ftl.write(3, "D")
        self.ftl.write(4, "E")   # 공간 부족 발생 예상

        self.ftl.read(1)
        self.ftl.write(1, "B-updated")
        self.ftl.write(0, "A-updated")
        self.ftl.write(2, "C-updated")  # GC 예상

        self.ftl.read(0)
        self.print_flash_state()

    def print_flash_state(self):
        print("\n=== Flash State ===")
        for b_idx, block in enumerate(self.ftl.flash.blocks):
            pages, count = self.ftl.flash.get_block_info(b_idx)
            print(f"Block {b_idx} | Erased {count} times")
            for p_idx, (valid, data) in enumerate(pages):
                state = 'V' if valid else 'I'
                print(f"  Page {p_idx}: {state} | {data}")
        print("====================\n")