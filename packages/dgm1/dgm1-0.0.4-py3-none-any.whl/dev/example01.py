from dgm1.dgm1_nrw import DGM1NRW


def at_a_glance():
    # create an instance of the class DGM1XYZ
    dgm1 = DGM1NRW('~/dgm1', '~/example/area.shp')

    # create a shapefile with polygons (2x2 km²) representing dem-tiles
    dgm1.create_shapefile()

    # download all xyz-files intersecting with the region and save them as tif-files
    dgm1.download(n_cores=11)

    # resample the original 1 meter resolution to 2, 5, and 10 meters
    dgm1.resample(2)
    dgm1.resample(5)
    dgm1.resample(10)

    # compose the tif-files into a GDAL Virtual Format with of original resolution (1 meter)
    # dgm1.create_vrt('~/example/dgm1/dgm1_area_01m.vrt', pixel_size=1)
    dgm1.create_vrt('~/example/dgm1/dgm1_area_02m.vrt', pixel_size=2)
    dgm1.create_vrt('~/example/dgm1/dgm1_area_05m.vrt', pixel_size=5)
    dgm1.create_vrt('~/example/dgm1/dgm1_area_10m.vrt', pixel_size=10)

    # dgm1.mosaic('~/example/dgm1/dgm1_area_01m.tif', pixel_size=1)
    dgm1.mosaic('~/example/dgm1/dgm1_area_02m.tif', pixel_size=2)
    dgm1.mosaic('~/example/dgm1/dgm1_area_05m.tif', pixel_size=5)
    dgm1.mosaic('~/example/dgm1/dgm1_area_10m.tif', pixel_size=10)


def create_shapefile():
    dgm1 = DGM1NRW('~/dgm1', '~/example/area.shp')
    dgm1.create_shapefile()


def gz_filenames_intersecting_region():
    dgm1 = DGM1NRW('~/dgm1', '~/example/area.shp')
    print(dgm1.gz_filenames_intersecting_region())


def download_all():
    dgm1 = DGM1NRW('~/dgm1')
    dgm1.download(n_cores=40)


def download_region():
    dgm1 = DGM1NRW('~/dgm1', '~/example/area.shp')
    dgm1.download(n_cores=40)


def resample(pixel_size):
    dgm1 = DGM1NRW('~/dgm1', '~/example/area.shp')
    dgm1.resample(pixel_size=pixel_size)


def mosaic():
    dgm1 = DGM1NRW('~/dgm1', '~/example/area.shp')
    dgm1.mosaic('~/example/dgm1/dgm1_area_02m_clip.tif', pixel_size=2, extent='clip')
    dgm1.mosaic('~/example/dgm1/dgm1_area_02m_region.tif', pixel_size=2, extent='region')
    dgm1.mosaic('~/example/dgm1/dgm1_area_02m_rasters.tif', pixel_size=2, extent='rasters')
    # dgm1.mosaic('~/example/dgm1/dgm1_area_02m_region_env.img', pixel_size=2, format='HFA')


def rename():
    import os
    import glob
    for f0 in list(glob.glob('/media/roehrig/geodata/nrwdaten/gis/original/dgm/dgm1/dgm1_nrw_01m_tif/*_2_nw.tif')):
        f1 = f0.replace('.tif', '_01m.tif')
        print(f0, f1)
        os.rename(f0, f1)


if __name__ == '__main__':
    pass
    at_a_glance()
    # create_shapefile()
    # gz_filenames_intersecting_region()
    # download_region()
    # download_all()
    # resample(2)
    # resample(5)
    # resample(10)
    # xyz_to_tif()
    # mosaic()
    # html()