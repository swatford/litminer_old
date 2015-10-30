from model.mbr.descriptor import Descriptor

__author__ = 'swatford'

def handle_descriptor_record(_,desc):
        d = Descriptor(desc)
        d.save()
        print(d.uid)
        return True