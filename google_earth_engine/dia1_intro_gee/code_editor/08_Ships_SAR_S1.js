// Dibujar un rectangulo "geometry" en el área de interes 
// Landsat 8 Collection 2 Level 2 (Surface Reflectance)
// NOTA: La Collection 1 (C01/T1_SR) fue retirada por USGS/GEE. Se usa C02/T1_L2.
var l8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2");

// This example demonstrates the use of the QA_PIXEL band to mask
// clouds in surface reflectance (SR) data. Suitable for Landsat C02 L2 datasets.

// Function to cloud mask from the QA_PIXEL band of Landsat 8 C02 L2 data.
function maskL8sr(image) {
  // En C02 QA_PIXEL: bit 1 = dilated cloud, bit 2 = cirrus,
  // bit 3 = cloud, bit 4 = cloud shadow.
  var dilatedCloudBitMask = 1 << 1;
  var cirrusBitMask       = 1 << 2;
  var cloudsBitMask       = 1 << 3;
  var cloudShadowBitMask  = 1 << 4;

  // Get the pixel QA band.
  var qa = image.select('QA_PIXEL');

  // All flags should be zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(dilatedCloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0))
      .and(qa.bitwiseAnd(cloudsBitMask).eq(0))
      .and(qa.bitwiseAnd(cloudShadowBitMask).eq(0));

  // Apply the C02 scaling factors to the optical SR bands (reflectance 0-1).
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);

  // Return the scaled & masked image, keeping only the SR bands.
  return image.addBands(opticalBands, null, true)
      .updateMask(mask)
      .select("SR_B.*")
      .copyProperties(image, ["system:time_start"]);
}

// Map the function over one year of data.
var collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    .filterDate('2020-01-01', '2020-12-31')
    .map(maskL8sr);

var composite = collection.median();

// Display the results.

// Get the median over time, in each band, in each pixel (sin enmascarar nubes).
var median = l8.filterDate('2020-01-01', '2020-12-31')
    .map(maskL8sr)   // escalado + máscara para que coincida con composite
    .median();

// Visualization parameters (reflectancia 0-1: SWIR1 / NIR / Red).
var visParams = {bands: ['SR_B6', 'SR_B5', 'SR_B4'], min: 0, max: 0.3};

// Load or import the Hansen et al. forest change dataset.
var hansenImage = ee.Image('UMD/hansen/global_forest_change_2015');

// Select the land/water mask.
var datamask = hansenImage.select('datamask');

// Create a binary mask.
var mask = datamask.eq(1);

// Update the composite mask with the water mask.
var maskedComposite = median.updateMask(mask);
//Map.addLayer(maskedComposite, visParams, 'masked');

// Make a water image out of the mask.
var water = mask.not();
var land = mask.eq(1);

// Mask water with itself to mask all the zeros (non-water).
water = water.mask(water);
land = land.mask(land);

// Load the Sentinel-1 ImageCollection.
var sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD');

// Filter by metadata properties.
var vh_2019 = sentinel1
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filterDate("2019-04-01","2019-05-30");

var vhAscending = vh_2019.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));
var vhDescending = vh_2019.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));

var radar_2019 = vhAscending.select('VH').merge(vhDescending.select('VH')).max().mask(water);

// 2020
var vh_2020 = sentinel1
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filterDate("2020-04-01","2020-05-30");

var vhAscending = vh_2020.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'));
var vhDescending = vh_2020.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'));

var radar_2020 = vhAscending.select('VH').merge(vhDescending.select('VH')).max().mask(water);

// Map composite over the Channel
Map.centerObject(geometry, 12);
Map.addLayer(radar_2019, {min: -15, max: 0}, 'Radar Merge 2019');
Map.addLayer(radar_2020, {min: -15, max: 0}, 'Radar Merge 2020');

composite = composite.mask(land);
Map.addLayer(composite, {bands: ['SR_B5', 'SR_B4', 'SR_B3'], min: 0, max: 0.3}, 'Landsat composite');
