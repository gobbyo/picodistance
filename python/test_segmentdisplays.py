from machine import Pin
from segmentdisplays import segdisplays

def main():
    segdisp = segdisplays()
    segdisp.waitreps = 10
    segdisp.waitonpaint = 0.01
    try:
        print("circuit test...")
        showbacknumberOneSegonly(segdisp, 0x01 << 7)
        showbackfloatOneSegonly(segdisp, 0x01 << 7)
        showforwardfloatOneSegonly(segdisp, 0x01 << 7)
        showforwardnumberOneSegonly(segdisp, 0x01 << 7)

        showbacknumber(segdisp)
        showbackfloat(segdisp)
        showforwardfloat(segdisp)
        showforwardnumber(segdisp)

        showbacknumberOneSegonly(segdisp, 0x01 << 6)
        showbackfloatOneSegonly(segdisp, 0x01 << 6)
        showforwardfloatOneSegonly(segdisp, 0x01 << 6)
        showforwardnumberOneSegonly(segdisp, 0x01 << 6)
    finally:
        print("test finished")

if __name__ == '__main__':
	main()