def count_seeds1(croplocation):
    # setting up
    image = cv2.imread(croplocation, 0)
    h, w = image.shape[:2]
    diff = (3, 3, 3)
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(image, mask, (0,0), (255,255,255), diff, diff)
    image = cv2.Canny(image, 100, 300)

    # scan image and count
    ricecount = 0
    oldlinecount = 0
    for y in range(0, h):
        oldc = 0
        linecount = 0
        start = 0
        for x in range(0, w):
            c = image[y, x] < 128;
            if c == 1 and oldc == 0:
                start = x
            if c == 0 and oldc == 1 and (x - start) > 10:
                linecount += 1
            oldc = c
        if oldlinecount != linecount:
            if linecount < oldlinecount:
                ricecount += oldlinecount - linecount
            oldlinecount = linecount
    return ricecount


def count_seeds2(croplocation):
    # using watershed algorithm
    image = cv2.imread(croplocation)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert and apply Otsu threshold filter
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # noise removal and sure background area
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # find sure foreground area and unknown region
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # marker labelling, add labels, mark region
    ret, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown == 255] = 0

    # apply watershed
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [0, 0, 255]

    show_img("watershed filter", image)
    return


def count_seeds3(croplocation):
    image = cv2.imread(croplocation, 0)
    image = cv2.medianBlur(image, 3)
    bw = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
    bw = cv2.dilate(cv2.erode(bw, kernel), kernel)
    return np.round_(np.sum(bw == 0) / 3015.0)