from struct import unpack
import sys

extab = True

if extab == False:
    section_names = [".init", ".text", ".ctors", ".dtors", ".rodata", ".data", ".sdata", ".sdata2"]
else:
    section_names = [".init", "extab", "extabindex", ".text", ".ctors", ".dtors",
          ".bin", ".rodata", ".data", ".sdata"] #s/bss/2 is all one blob

with open(sys.argv[1], "rb") as f:
    sections = []
    text_offs = unpack(">7I", f.read(0x1C))
    data_offs = unpack(">11I", f.read(0x2C))
    text_addr = unpack(">7I", f.read(0x1C))
    data_addr = unpack(">11I", f.read(0x2C))
    text_size = unpack(">7I", f.read(0x1C))
    data_size = unpack(">11I", f.read(0x2C))
    bss_addr, bss_size, entrypoint = unpack(">3I", f.read(12))
    for i in range(7):
        if text_offs[i] != 0:
            sections.append([text_offs[i], text_addr[i], text_size[i], 0])
    for i in range(11):
        if data_offs[i] != 0:
            sections.append([data_offs[i], data_addr[i], data_size[i], 1])
    sections.sort(key=lambda x: x[1])
    #assert len(sections) == 10
    '''for section in sections:
        print("%08X %08X %08X" % (section[1], section[0], section[2]))
    assert (bss_addr + bss_size) <= sections[9][1] #ends before sdata2'''
    for i in range(len(sections)):
        start = sections[i][1]
        end = start + sections[i][2] #size
        start1 = sections[i][0]
        end1 = start1 + sections[i][2]
        print("%s  %08x %08x %08X %08x" % (section_names[i].rjust(17), start, start + (end1 - start1), end1 - start1, 0))
    print("%08X %08X %08X %08X" % (bss_addr, bss_size, bss_addr + bss_size, entrypoint))
    '''print("%s%08X to %08X" % (section_names[8].ljust(12), bss_addr, sections[8][1]))
    print("%s%08X to %08X" % (section_names[9].ljust(12), sections[8][1], sections[8][1] + sections[8][2]))
    print("%s%08X to %08X" % (section_names[10].ljust(12), sections[8][1] + sections[8][2], bss_addr + bss_size))
    print("%s%08X to %08X" % (section_names[11].ljust(12), sections[9][1], sections[9][1] + sections[9][2]))'''