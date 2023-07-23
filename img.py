import cv2
import cv2 as cv
import numpy as np
import requests
import imutils
import matplotlib.pyplot as plt

url = "http://192.168.1.6:8080/shot.jpg"


def get_contours(img, original_img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 80000:
            # print(area)
            cv.drawContours(original_img, cnt, -1, (0, 255, 0), 2)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            ax = approx.item(0)
            ay = approx.item(1)
            bx = approx.item(2)
            by = approx.item(3)
            cx = approx.item(4)
            cy = approx.item(5)
            dx = approx.item(6)
            dy = approx.item(7)

            width, height = 630, 630

            pts1 = np.float32([[bx, by], [ax, ay], [cx, cy], [dx, dy]])
            pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

            matrix = cv.getPerspectiveTransform(pts1, pts2)
            img_perspective = cv.warpPerspective(original_img, matrix, (width, height))
            contours = cv.cvtColor(img_perspective, cv.COLOR_BGR2GRAY)
            cv.imshow('contour', contours)
            for x in range(0, 630):
                for y in range(0, 630):
                    if contours[x][y] < 100:
                        contours[x][y] = 0
                    else:
                        contours[x][y] = 255
            cv.imshow('contour', contours)
            image_differentiator(arr,contours)
            # cell = contours[0:70,0:70]
            # plt.imshow(cell , cmap= 'gray')
            # plt.show()

            # crop = 10
            #
            # for y in range(1, 9):
            #     for x in range(1, 9):
            #         plt.imshow(contours[y * 70 - 70 + crop:y * 70 - crop, x * 70 - 70 + crop:x * 70 - crop],
            #                    cmap='gray')
            #         plt.show()

def image_differentiator(grid,Img):
    drop_loc = 'C://Users//rajly//sudokuSOLVER//data//'
    crop_val= 10

    listNum = []
    for i in range (0,9):
        for j in range (0,9):
            if grid[i][j] not in listNum:
                print(grid[i][j])
                listNum.append(grid[i][j])
                J = j + 1
                I = i + 1
                cell = Img[I * 70 - 70 + crop_val: I * 70 - crop_val, j * 70 - 70 + crop_val: j * 70 - crop_val]
                cv.imwrite(drop_loc + str(grid[i][j]) + '//IMG_{}.png'.format((i + 1) * (j + 1)), cell)


while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv.imdecode(img_arr, -1)
    img = imutils.resize(img, width=900, height=900)

    gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 3)
    canny = cv.Canny(blur, 50, 50)
    copy = img.copy()

    arr = [[3,0,4,6,1,0,0,0,5],
           [7,0,8,0,0,0,3,0,6],
           [0,0,0,9,0,3,4,0,0],
           [8,0,7,0,0,0,5,1,0],
           [0,2,0,7,0,5,0,4,0],
           [6,0,0,0,9,1,0,0,2],
           [4,8,0,3,5,2,0,0,7],
           [0,0,0,0,0,0,9,0,0],
           [1,0,6,0,0,9,2,8,0]]


    get_contours(canny, copy)

    cv.imshow('webcam', copy)
    if cv.waitKey(1) & 0xff == ord('q'):
        break

cv.destroyAllWindows()