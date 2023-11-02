import RasterHelpers.rasterProcessor as rp
ras_pro = rp.RasterProcessor()
ras_pro.set_data_path(r'H:\Python\Projects\YZRiver\Data\HDF')
ras_pro.set_out_path(r'H:\Python\Projects\YZRiver\Data\Test')
ras_pro.process('extract',filter='*.hdf')
