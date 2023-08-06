# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:50:03 2019

@author: danaukes
"""

import file_sorter.images as fui
import file_sorter.support as fus

#if __name__=='__main__':
#    aname = 'a.jpg'
#    bname = 'b.jpg'
#    cname = 'c.jpg'
#
#    ahash = fui.gen_p_hash(aname)
#    bhash = fui.gen_p_hash(bname)
#    chash = fui.gen_p_hash(cname)
#p1 = 'C:/Users/danaukes/Dropbox (Personal)/Camera Uploads'
path = 'C:/Users/danaukes/Dropbox (ASU)/idealab/presentations/2020-03-05 Research Talk/reduced/images-reduced'
compare_info = fus.scan_compare_dir(path, recursive=True,local_hashfile = 'hash.yaml',file_filter=fui.filter_img_filetype,hasher=fui.gen_p_hash_opt)
#compare_info.save('./','phash.yaml')
