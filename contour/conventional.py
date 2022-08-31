import cv2


def processConventionalContouring(name):
    image = cv2.imread(name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 30, 300)
    _, cnt, _= cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    coins = image.copy()
    
    cv2.drawContours(coins, cnt, -1, (0, 0, 255), 2)
    cv2.imwrite('media/conventional/output.png', coins)