import cv2


def process(name):
    image = cv2.imread(name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blurred, 30, 300)
    # (cnt, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _, cnt, _= cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    coins = image.copy()
    # ctr = np.array(cnt).reshape((-1,1,2)).astype(np.int32)
    # cv2.drawContours(coins, cnt, 0, (0, 255, 0), -1)
    cv2.drawContours(coins, cnt, -1, (0, 0, 255), 2)
    cv2.imwrite('media/output.png', coins)