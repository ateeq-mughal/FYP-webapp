import rasterio, os
import pandas as pd
import numpy as np
import joblib


def band_scorer(path):
    """Get Path to 'Tiff' Folder and Name of Band: b2,b3,b4,b5,b6,b7,b8,b8a
    Return mean
    """
    # read all raster values
    with rasterio.open(path, "r") as ds:
        arr = ds.read()
    target_index_file = arr
    A = np.ravel(target_index_file)
    avg = A[~np.isnan(A)].mean()
    return avg


def classify(path):

    wv_tif = path
    folder = r"media\cropClassification\bands"
    src = rasterio.open(wv_tif)
    print(src.count)
    for band in range(1, src.count + 1):
        single_band = src.read(band)

        # get the output name
        out_name = os.path.basename(wv_tif)
        file, ext = os.path.splitext(out_name)
        name = file + "_" + "B" + str(band) + ".tif"
        out_img = os.path.join(folder, name)

        print(out_img + " done")

        # Copy the metadata
        out_meta = src.meta.copy()

        out_meta.update({"count": 1})

        # save the clipped raster to disk
        with rasterio.open(out_img, "w", **out_meta) as dest:
            dest.write(single_band, 1)

    FID = sorted(os.listdir("media/cropClassification/bands"))
    template_dict = {"B01": [], "B02": [], "B03": [], "B04": [], "NDVI": []}
    df = pd.DataFrame(template_dict)

    bands = ["B01", "B02", "B03", "B04"]
    FID = sorted(os.listdir(folder))
    for band in FID:
        bands = [0, 0, 0, 0, 0]
        for i in range(1, 5):
            l = path.split("/")
            print(l)
            image = (
                "media/cropClassification/bands/" + l[2][:-4] + "_B" + str(i) + ".tif"
            )
            bands[i - 1] = band_scorer(image)
        NDVI = (bands[3] - bands[0]) / (bands[3] + bands[0])
        bands[4] = NDVI
        df.loc[len(df.index)] = [bands[0], bands[1], bands[2], bands[3], bands[4]]

    loaded_rf = joblib.load("static/crop_classification.joblib")
    
    pred = loaded_rf.predict(df)

    return "Sugarcane" if pred[0] == "S" else "Canola"
