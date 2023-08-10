from machine import Pin
from segmentdisplays import segdisplays

def main():
    segdisp = segdisplays()
    segdisp.waitreps = 20
    segdisp.waitonpaint = 0.01
    try:
        print("circuit test...")
        segdisp.backnumberOneSegonly(0x01 << 7)
        segdisp.backfloatOneSegonly(0x01 << 7)
        segdisp.forwardfloatOneSegonly(0x01 << 7)
        segdisp.forwardnumberOneSegonly(0x01 << 7)

        segdisp.showbacknumber()
        segdisp.showbackfloat()
        segdisp.showforwardfloat()
        segdisp.showforwardnumber()

        segdisp.backnumberOneSegonly(0x01 << 6)
        segdisp.backfloatOneSegonly(0x01 << 6)
        segdisp.forwardfloatOneSegonly(0x01 << 6)
        segdisp.forwardnumberOneSegonly(0x01 << 6)
    finally:
        print("test finished")

if __name__ == '__main__':
	main()