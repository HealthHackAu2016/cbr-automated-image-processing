# Automated Image Processing

Solution to a problem pitched by Normal Warthmann at the 2016 Canberra HealthHack. 
Solution by group: seedid:
Norman Warthmann
Thomas Hamer
Allen Huang
Joseph Meltzer
Manal Mohania
William Shen


# Problem Description

Images will be taken of seed samples, along with the seed bag, a ruler, and a 24 colour sample card. From these images, the seeds within the sample must be separated and analysed. The analysis should include measurements of the length and width of each seed, and summary statistics provided. 


# Step one: Image Filtering

In order to standardise and aid image segmentation, all images will be normalised to a certain brightness. The pure white square on the colour card will be detected, and the entire image's brightness will be adjusted until the white square matches a pre-determined brightness level. 


# Step two: Image Scaling

Different photographs all have varying scales, depending on camera position and resolution. The 24 colour card is isolated and its length measured, and then a scale factor is calculated and stored, to be used in calculations at the end. 

# Step three: Seed Detection

The seeds within the image are all detected, and each individual is isolated into a separate image. ........

# Step four: Seed Measuring

The individual images are processed, and the length and width of the seeds inside are determined. These metrics are used to work out if the image contained a single seed or not, and information from images that contained multiple seeds is deleted. 

# Step five: Statistics

With the data collected from single seed images, tables and histograms are produced, and displayed to the user. 